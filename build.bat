@echo off
echo Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

echo Building executable...
pyinstaller --onefile ^
           --noconsole ^
           --clean ^
           --icon=NONE ^
           --name="DualSense-Runiverse" ^
           --add-data "Dualsense-PS5.png;." ^
           --hidden-import=PIL ^
           --hidden-import=PIL._tkinter_finder ^
           --hidden-import=PIL.Image ^
           --hidden-import=PIL.ImageTk ^
           --hidden-import=webbrowser ^
           --hidden-import=pygame ^
           dualsense_mapper_optimized.py

echo Done! The executable is in the dist folder.
echo.
echo Testing the executable...
timeout /t 2 >nul
start "" "dist\DualSense-Runiverse.exe"
pause 