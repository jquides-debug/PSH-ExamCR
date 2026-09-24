param(
    [string]$Python = "$PSScriptRoot\.venv\Scripts\python.exe",
    [string]$MakeNsis = "makensis.exe"
)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & $Python -m PyInstaller --noconfirm --windowed --name PSH-ExamCR --paths src --add-data 'src/assets;assets' --add-data 'license.txt;.' --add-data 'readme.md;.' --icon src/assets/icon.ico src/main_gui.py
    if ($LASTEXITCODE -ne 0) { throw 'Application packaging failed.' }
    & $MakeNsis installer.nsi
    if ($LASTEXITCODE -ne 0) { throw 'Installer compilation failed.' }
    Get-FileHash -LiteralPath dist/PSH-ExamCR-Setup.exe -Algorithm SHA256
} finally {
    Pop-Location
}
