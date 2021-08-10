# Senren_Tokei
You need to obtain the voice files by yourself, and format them into .wav files.

Put them in /resources/ and run the script.

To make an .exe file:
```
pyinstaller -F senrentokei.py --hiddenimport pystray._win32 -i "ICONPATH" -w
```
You will still need the /resources/ folder after generated the .exe file.
