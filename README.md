# SyncGuard
Personal "Local Cloud" utility that automates securely backing up and monitoring local files to a centralized server, complete with a web dashboard for tracking and downloading files.

## Features

- **Real-Time File Monitoring:** Automatically observes the `Local_Files/` directory for new creations, content modifications, and file deletions.
- **End-to-End Encryption:** Encrypts both file names and their internal contents (using a Caesar Cipher) before they ever leave the client over the network.
- **Integrity Verification (Checksums):** Crafts a JSON metadata header with MD5 hashing to guarantee files are not corrupted during TCP packet transmission.
- **Django Web Dashboard:** Provides a centralized web-based UI (`http://127.0.0.1:8000/`) to track all operations, statuses, and file sizes.
- **Secure Access & Retrieval:** The dashboard is protected behind a login page. Authorized users can securely download backups, dynamically decrypting the files back into their original readable state upon download.

## Project Structure

- `monitor_client.py`: The client script that tracks the local directory, encrypts data, and sends JSON headers / payloads over TCP sockets.
- `server_node.py`: The server script that listens for connections, verifies MD5 checksum hashes, writes encrypted data to `Cloud_Backup/`, and updates the Django backend.
- `sync_project/`: The Django web application containing the `dashboard` UI, database models, and secure download views.

## How to Run

Note: Ensure your Python virtual environment (`venv`) is activated.

**1. Start the Django Web Server (Dashboard)**
```bash
cd sync_project
python manage.py runserver
```
*Access the dashboard at `http://127.0.0.1:8000/` and log in with your credentials.*

**2. Start the Backup Server Node**
```bash
python server_node.py
```
*Listens on `127.0.0.1:11111` and saves encrypted backups securely to the `Cloud_Backup/` directory.*

**3. Start the Local Monitor Client**
```bash
python monitor_client.py
```
*Monitors the `Local_Files/` directory and synchronizes changes to the server instantly.*
