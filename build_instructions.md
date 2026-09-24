# Build Instructions

The following instructions show how to build the program into a single `.exe`
file that can be run to install the software.

1. Install the required modules from [`requirements.txt`](requirements.txt) if
   you haven't already.
2. Open a terminal in the root directory.
3. Keep `src/assets/manual.md` and `src/assets/psh-logo.png` in the package.
   Help displays the bundled manual inside the app; no PDF conversion is required.
4. Install NSIS if you haven't already, and add the install location to your
   system's PATH variable.
5. Run the build command:
   ```sh
   pyinstaller -p src --add-data="src;." -y -w --icon=src/assets/icon.ico --name=open-mcr src/main_gui.py; makensis installer.nsi
   ```
