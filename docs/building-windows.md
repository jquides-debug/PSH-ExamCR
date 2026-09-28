# Windows packaging (maintainers only)

Staff installation and usage instructions are in [readme.md](../readme.md).

The Windows package is built with 64-bit Python 3.14 and PyInstaller. The tested
packaging dependencies are pinned in `requirements/windows.txt`; the older
upstream `requirements.txt` is not used for this build.

1. Create a virtual environment with 64-bit Python 3.14:
   `python -m venv .venv`
2. Install the packaging dependencies:
   `.\.venv\Scripts\python.exe -m pip install -r requirements/windows.txt`
3. Obtain NSIS from https://nsis.sourceforge.io/Download and make `makensis.exe`
   available, or pass its path to the script.
4. Run:

   ```powershell
   .\scripts\build-windows.ps1 -MakeNsis '.\downloads\nsis-3.11\makensis.exe'
   ```

The deliverables are `dist/PSH-ExamCR-Setup.exe` and its checksum file,
`dist/SHA256SUMS.txt`. Upload both as assets on a GitHub release so the README's
latest-installer link points directly to the download. The `dist/PSH-ExamCR` folder is the
standalone application bundle; its executable requires the accompanying
`_internal` directory. The installer includes the runtime, PSH logo, help guide,
the three user-facing input templates from `src/assets/templates`,
original software license, and README attribution. Keep the template filenames
unchanged: the Templates window uses them to save copies for users. The user guide
is bundled from `docs/user-guide.md`; design references and local examinee data
are not included. Generated PyInstaller specifications are written under `build/`.

The installer installs for the current user, adds Start menu shortcuts, and
registers an uninstaller in Windows Settings. Keep scans and exported results
outside the installation folder. Close the app before updating or uninstalling.

Before distributing a build, verify startup from outside the project directory,
process a sample batch, and check installation and uninstallation on a test PC.
The build script does not sign the executable or installer.
