#!/bin/bash
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Packaging application for macOS (.app)..."
# Note: This must be run on a macOS machine to generate a .app bundle
pyinstaller --noconfirm --onefile --windowed --name "DiscordCustomRP" --clean main.py

echo ""
echo "Packaging complete! Check the 'dist' folder."
