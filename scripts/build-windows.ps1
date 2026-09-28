param(
    [string]$Python = "$PSScriptRoot\..\.venv\Scripts\python.exe",
    [string]$MakeNsis = "makensis.exe"
)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Push-Location $projectRoot
try {
    & $Python -m PyInstaller --noconfirm --windowed --name PSH-ExamCR --specpath "$projectRoot\build" --paths "$projectRoot\src" --add-data "$projectRoot\src\assets;assets" --add-data "$projectRoot\docs\user-guide.md;docs" --add-data "$projectRoot\license.txt;." --add-data "$projectRoot\readme.md;." --icon "$projectRoot\src\assets\branding\icon.ico" "$projectRoot\src\main_gui.py"
    if ($LASTEXITCODE -ne 0) { throw 'Application packaging failed.' }
    & $MakeNsis "/DPROJECT_ROOT=$projectRoot" "$projectRoot\packaging\windows\installer.nsi"
    if ($LASTEXITCODE -ne 0) { throw 'Installer compilation failed.' }
    $installerHash = Get-FileHash -LiteralPath dist/PSH-ExamCR-Setup.exe -Algorithm SHA256
    "$($installerHash.Hash.ToLowerInvariant())  PSH-ExamCR-Setup.exe" |
        Set-Content -LiteralPath dist/SHA256SUMS.txt -Encoding ascii
    $installerHash
} finally {
    Pop-Location
}
