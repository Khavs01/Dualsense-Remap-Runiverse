@echo off
echo Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

echo Checking image files...
if not exist "Dualsense-PS5.png" (
  echo ERROR: Dualsense-PS5.png not found in current directory!
  echo Please make sure the image file is in the same directory as this script.
  pause
  exit /b 1
)

echo Converting image to base64...
python encode_image.py

if not exist "image_base64.txt" (
  echo ERROR: Failed to create base64 image file!
  pause
  exit /b 1
)

echo Building executable with embedded image...
pyinstaller --onefile ^
           --noconsole ^
           --clean ^
           --icon=NONE ^
           --name="DualSense-Runiverse" ^
           --add-data "image_base64.txt;." ^
           --hidden-import=PIL ^
           --hidden-import=PIL._tkinter_finder ^
           --hidden-import=PIL.Image ^
           --hidden-import=PIL.ImageTk ^
           --hidden-import=webbrowser ^
           --hidden-import=pygame ^
           dualsense_mapper_optimized.py

rem Verify that executable was created
echo Verifying build...
if not exist "dist\DualSense-Runiverse.exe" (
  echo ERROR: Build failed - executable not created!
  pause
  exit /b 1
)

echo Done! The executable is in the dist folder.
echo.
echo Testing the executable...
timeout /t 2 >nul
start "" "dist\DualSense-Runiverse.exe"
pause