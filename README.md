<div align="center">

# 🛡️ SyncGuard
**Your Personal Local Cloud & Secure Backup Utility**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-Project-green.svg)](https://www.djangoproject.com/)
[![Security](https://img.shields.io/badge/Encryption-E2E-orange.svg)]()

<p>Automate securely backing up and monitoring local files to a centralized server. Complete with tracking, integrity verification, and a web dashboard.</p>

</div>

---

## 🌟 The Vision

In a world where data privacy is paramount, **SyncGuard** gives you full control. It's not just a backup script—it's a localized, self-hosted cloud sync solution that ensures your data never leaves your network unencrypted.

### *Why SyncGuard?*
- **Absolute Privacy:** End-to-end encryption means only you can read your files.
- **Immediate Sync:** Files are processed the second you drop them in the folder.
- **Visual Control:** A brilliant Django web dashboard gives you bird's-eye visibility.

---

## 🏗️ Architecture

SyncGuard works in a highly coordinated three-part harmony:

1. **💻 The Monitor Client (`monitor_client.py`):** Sits on your local machine. Watches the `Local_Files/` directory. Encrypts and transmits changes on the fly.
2. **📡 The Server Node (`server_node.py`):** The steadfast receiver. Verifies MD5 checksums, handles TCP packets, and stores encrypted backups securely in `Cloud_Backup/`. 
3. **🌐 The Web Dashboard (`sync_project/`):** The command center. A secure Django web interface to monitor sync statuses and securely fetch and decrypt files.

---

## 🔥 Key Features

- **⚡ Real-Time Monitoring:** Instant detection of file creations, modifications, and deletions.
- **🔐 End-to-End Encryption:** Custom cipher applied to both filenames and contents before transmission.
- **✅ Integrity Verification:** Complete MD5 hashing ensures zero corruption across TCP packets.
- **📊 Centralized Web UI:** Django dashboard tracking every operation in real-time.
- **📥 Secure Retrieval:** Authorized users can download backups which automatically decrypt upon retrieval.

---

## 🚀 Getting Started

Ready to spin up your secure cloud? Follow these three simple steps:

*Note: Ensure your Python virtual environment (`venv`) is activated.*

### Step 1: Launch the Command Center (Dashboard)
```bash
cd sync_project
python manage.py runserver
```
> 🌐 Access the dashboard at `http://127.0.0.1:8000/` and log in with your credentials.

### Step 2: Ignite the Server Node
```bash
# Open a new terminal
python server_node.py
```
> 📡 Listens on `127.0.0.1:11111` and secures incoming files to `Cloud_Backup/`.

### Step 3: Start the Syncer (Client)
```bash
# Open a new terminal
python monitor_client.py
```
> 👀 Actively monitors the `Local_Files/` directory and synchronizes changes to the server instantly.

---

<div align="center">
  <i>Built with security and simplicity in mind.</i>
</div>
