#!/usr/bin/env python3
import socket
import os
import sys
import django
import json
import hashlib

# Add the sync_project directory to Python's path so it can find 'sync_project.settings'
sys.path.append(os.path.join(os.path.dirname(__file__), 'sync_project'))

# Setup Django environment so we can use the models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sync_project.settings')
django.setup()

from dashboard.models import SyncLog

# Using Caesar Cipher Decryption
SECRET_KEY = 5
def caesar_decrypt(text, shift=SECRET_KEY):
    decrypted = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            decrypted += chr((ord(char) - start - shift) % 26 + start)
        else:
            decrypted += char
    return decrypted

def log_to_db(orig_name, enc_name, size, status="Success"):
    # Creating a new instance of our model object[cite: 2, 3]
    new_log = SyncLog(
        original_name=orig_name, 
        encrypted_name=enc_name,
        file_size=size,
        status=status
    )
    new_log.save() 
    print(f"Database updated for {enc_name} with status {status}")

def start_server():
    host = '127.0.0.1'
    port = 11111
    backup_dir = 'Cloud_Backup'
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir) # [cite: 5]
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # [cite: 4]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    
    print(f"Server is listening for files on {host}:{port}...")
    
    while True:
        conn, addr = s.accept() # [cite: 4]
        print(f"Connected by {addr}")
        
        # Receive JSON metadata
        meta_data = conn.recv(1024).decode().strip()
        if not meta_data:
            conn.close()
            continue
            
        try:
            meta = json.loads(meta_data)
        except:
            print("Invalid metadata received.")
            conn.close()
            continue
            
        action = meta.get("action")
        file_name = meta.get("filename")
        expected_hash = meta.get("checksum", "")
        original_name = caesar_decrypt(file_name)
        
        file_path = os.path.join(backup_dir, file_name)
        
        if action == "DELETE":
            print(f"Deleting file: {file_name} (Original: {original_name})")
            if os.path.exists(file_path):
                os.remove(file_path)
            log_to_db(original_name, file_name, 0, "Deleted")
            conn.close()
            continue

        print(f"Receiving file: {file_name} (Original: {original_name})")
        
        # Open file and write binary data
        with open(file_path, 'wb') as f:
            while True:
                data = conn.recv(1024) # [cite: 4]
                if not data:
                    break
                f.write(data)
                
        # Verify Integrity
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            
        status = "Success"
        if file_hash != expected_hash:
            print(f"WARNING: Checksum mismatch for {file_name}! File may be corrupted.")
            status = "Corrupted (Checksum Mismatch)"
        else:
            print(f"Integrity verified for {file_name}!")
        
        # ADDED: Get metadata and log to Django Database
        f_size = os.path.getsize(file_path)
        
        log_to_db(original_name, file_name, f_size, status)
        
        print(f"File {file_name} received, saved, and logged to database.")
        conn.close()
        
if __name__ == "__main__":
    start_server()