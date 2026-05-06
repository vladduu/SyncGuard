#!/usr/bin/env python3
import socket
import os
import time
import json
import hashlib

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
        
    def send_file(self, filename, action="SYNC"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))

            encrypted_name = caesar_encrypt(filename)
            
            if action == "DELETE":
                meta = json.dumps({"action": "DELETE", "filename": encrypted_name})
                s.send(meta.ljust(1024).encode('utf-8'))
                print(f"Sent delete command for: {filename}")
                s.close()
                return True

            # Process file content explicitly
            file_path = os.path.join(self.source_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Encrypt the entire content of the file
            encrypted_content = caesar_encrypt(content)
            
            # Generate Checksum on the encrypted data (since server verifies the saved encrypted data)
            file_hash = hashlib.md5(encrypted_content.encode('utf-8')).hexdigest()
            
            # Send metadata header padded to exactly 1024 bytes
            meta = json.dumps({
                "action": "SYNC", 
                "filename": encrypted_name, 
                "checksum": file_hash
            })
            s.send(meta.ljust(1024).encode('utf-8'))
            
            # small delay before content
            time.sleep(0.1)

            # Send the file data
            s.sendall(encrypted_content.encode('utf-8'))
            
            print(f"Sent encrypted file with checksum: {encrypted_name}")
            s.close()
            return True
        except Exception as e:
            print(f"Transfer Error: {e}")
            return False
        
    def monitor(self):
        self.file_tracker = {}
        print(f"Monitoring '{self.source_dir}' for new files, modifications, and deletions...")
        while True:
            try:
                current_files = set(os.listdir(self.source_dir))
            except OSError:
                continue

            # Check for DELETED files
            tracked_files = set(self.file_tracker.keys())
            deleted_files = tracked_files - current_files
            for deleted in deleted_files:
                print(f"[Deleted] detected: {deleted}")
                if self.send_file(deleted, action="DELETE"):
                    del self.file_tracker[deleted]

            # Check for NEW or MODIFIED files
            for filename in current_files:
                file_path = os.path.join(self.source_dir, filename)
                if not os.path.isfile(file_path):
                    continue
                
                mtime = os.path.getmtime(file_path)
                
                if filename not in self.file_tracker or mtime > self.file_tracker[filename]:
                    action_msg = "New file" if filename not in self.file_tracker else "Modification"
                    print(f"[{action_msg}] detected: {filename}")
                    
                    if self.send_file(filename, action="SYNC"):
                        self.file_tracker[filename] = mtime
            
            time.sleep(1)
                
if __name__ == "__main__":
    client = SyncClient(source_dir='Local_Files')
    client.monitor()