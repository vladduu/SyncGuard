#!/usr/bin/env python3
import socket
import os

def start_server():
    
    # Setup
    host = '127.0.0.1'
    port = 11111
    backup_dir = 'Cloud_Backup'
    
    # Creating backup directory
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    
    print(f"Server is listening for files on {host}:{port}...")
    
    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        
        # Receive file name
        file_name = conn.recv(1024).decode()
        print(f"Receiving file: {file_name}")
        
        # Open file and write binary data
        file_path = os.path.join(backup_dir, file_name)
        with open(file_path, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        
        print(f"File {file_name} received and saved to {backup_dir}.")
        conn.close()
        
if __name__ == "__main__":
    start_server()