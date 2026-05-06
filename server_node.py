#!/usr/bin/env python3
import socket
import os
import django

# Setup Django environment so we can use the models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sync_project.settings')
django.setup()

from dashboard.models import SyncLog

def log_to_db(orig_name, enc_name, size):
    # Creating a new instance of our model object[cite: 2, 3]
    new_log = SyncLog(
        original_name=orig_name, # Note: You'll need to send the original name or decrypt it here
        encrypted_name=enc_name,
        file_size=size
    )
    new_log.save() # Saving the entry to the database[cite: 2]
    print(f"Database updated for {enc_name}")

def start_server():
    host = '127.0.0.1'
    port = 11111
    backup_dir = 'Cloud_Backup'
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)[cite: 5]
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)[cite: 4]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    
    print(f"Server is listening for files on {host}:{port}...")
    
    while True:
        conn, addr = s.accept()[cite: 4]
        print(f"Connected by {addr}")
        
        # Receive encrypted file name
        file_name = conn.recv(1024).decode()
        print(f"Receiving file: {file_name}")
        
        # Open file and write binary data[cite: 1, 5]
        file_path = os.path.join(backup_dir, file_name)
        with open(file_path, 'wb') as f:
            while True:
                data = conn.recv(1024)[cite: 4]
                if not data:
                    break
                f.write(data)
        
        # ADDED: Get metadata and log to Django Database
        f_size = os.path.getsize(file_path)
        # For this lab, we use the encrypted name for both fields unless you send the original name separately
        log_to_db("Unknown (Encrypted)", file_name, f_size)
        
        print(f"File {file_name} received, saved, and logged to database.")
        conn.close()
        
if __name__ == "__main__":
    start_server()