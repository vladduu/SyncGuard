#!/usr/bin/env python3
import socket
import os
import time

# Using Caesar Cipher Encryption
SECRET_KEY = 5
def caesar_encrypt(text, shift=SECRET_KEY):
    encrypted = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - start + shift) % 26 + start)
        else:
            encrypted += char
    return encrypted 

class SyncClient:
    def __init__(self, source_dir, host='127.0.0.1', port=11111):
        self.source_dir = source_dir
        self.host = host
        self.port = port
        
        if not os.path.exists(self.source_dir):
            os.makedirs(self.source_dir, exist_ok=True)
            try:
                os.chmod(self.source_dir, 0o777) # Lab 8: Managing folder access
            except PermissionError:
                print(f"Warning: Could not set permissions on {self.source_dir}")
            
        #To keep track of already synced files
        self.synced_files = set()
        
    def send_file(self, filename):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))

            # Encrypt and send the filename
            encrypted_name = caesar_encrypt(filename)
            s.send(encrypted_name.encode('utf-8'))
            time.sleep(0.1)

            file_path = os.path.join(self.source_dir, filename)
            with open(file_path, 'r') as f:
                content = f.read()
                # Encrypt the entire content of the file
                encrypted_content = caesar_encrypt(content)
                s.sendall(encrypted_content.encode('utf-8'))
            
            print(f"Sent fully encrypted file: {encrypted_name}")
            s.close()
            return True
        except Exception as e:
            print(f"Encryption/Transfer Error: {e}")
            return False
        
    def monitor(self):
        self.file_tracker = {}
        print(f"Monitoring '{self.source_dir}' for new files and modified content...")
        while True:
            # List all current items
            try:
                current_files = os.listdir(self.source_dir)
            except OSError:
                continue

            for filename in current_files:
                file_path = os.path.join(self.source_dir, filename)
                
                # Skip if it's a directory or unchanged file
                if not os.path.isfile(file_path):
                    continue
                
                mtime = os.path.getmtime(file_path)
                
                if filename not in self.file_tracker or mtime > self.file_tracker[filename]:
                    action = "New file" if filename not in self.file_tracker else "Modification"
                    print(f"[{action}] detected: {filename}")
                    
                    if self.send_file(filename):
                        # Update the tracker with the latest timestamp
                        self.file_tracker[filename] = mtime
            
            time.sleep(1)
                
if __name__ == "__main__":
    client = SyncClient(source_dir='Local_Files')
    client.monitor()