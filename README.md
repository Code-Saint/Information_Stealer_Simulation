# 🕵️‍♂️ Information Stealer Simulation

## 🔍 Overview

This project simulates a **credential and data exfiltration tool**, commonly referred to as an "information stealer". Built purely for **ethical research and red team training**, the tool mimics the behavior of real-world malware by collecting sensitive data from the local system and preparing it for exfiltration.

It is designed to demonstrate how system compromise can lead to loss of critical data such as browser-saved credentials, clipboard contents, IP address, and system info.

> ⚠️ This tool is intended strictly for **educational, ethical hacking, and internal testing purposes only**. Do not deploy it on unauthorized systems.

---

## 💡 Features

- 🔑 Extract saved passwords from **Google Chrome** using AES-GCM & Windows DPAPI decryption
- 🖥️ Gather detailed **system information** (OS, hostname, IP, MAC)
- 🌐 Capture **public IP address** from external services
- 📋 Retrieve **clipboard contents**
- 💾 Store all stolen data locally in structured format for simulation

---

## ⚙️ Technologies Used

- Python 3.x
- `sqlite3`, `os`, `json`, `base64`, `win32crypt`, `Cryptodome`, `requests`
- Windows-only implementation due to DPAPI & Chrome path structures

---

## 🛠 How It Works

1. **Chrome Credential Extraction:**
   - Reads Chrome's `Login Data` SQLite DB
   - Decrypts passwords using AES-GCM & Windows Data Protection API (DPAPI)

2. **System & Network Info Collection:**
   - Collects OS version, IP addresses, MAC address, hostname, etc.

3. **Clipboard Data Theft:**
   - Captures any current text stored in clipboard

4. **Storage:**
   - All data is saved to a local file inside `/stolen_data/` folder for review

---

## 🚀 Usage

### Install Dependencies:
```bash
pip install -r requirements.txt


