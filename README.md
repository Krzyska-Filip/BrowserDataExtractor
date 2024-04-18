# BrowserDataExtractor

This Python script automaticly extracts decryption keys and browser data from Google Chrome and Microsoft Edge on Windows systems. 

Data is stored in sqlite database which can be manualy opened using programs like [sqlitebrowser](https://github.com/sqlitebrowser/sqlitebrowser).

Data includes:
* Bookmarks
* Browsing History
* Saved Credentials
* Visited Links

This script was created as a demonstration created for the academic group PUTRequest as part of Rubber Duck project.

### Required modules
```
#pip install pywin32
from win32crypt import CryptUnprotectData
#pip install pycryptodomex
from Cryptodome.Cipher import AES
```

### Execution
```
 python3 .\browser.py
```

### How to add more browsers:

`browsers` representing the typical paths where Chrome and Edge (or any other browser) store their user data within the 'LOCALAPPDATA' directory. You can simply insert a new to a dictionary.

```
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
```
