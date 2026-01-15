@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Packaging application for Windows (.exe)...
pyinstaller --noconfirm --onefile --windowed --name "DiscordCustomRP" --clean main.py

echo.
echo Packaging complete! Check the 'dist' folder.
pause
