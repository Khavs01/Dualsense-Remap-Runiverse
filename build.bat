@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Building executable...
pyinstaller --onefile --noconsole --icon=NONE --hidden-import=pkg_resources.py2_warn --hidden-import=pkg_resources.markers --hidden-import=pkg_resources.extern dualsense_mapper_optimized.py

echo Done! The executable is in the dist folder.
pause 