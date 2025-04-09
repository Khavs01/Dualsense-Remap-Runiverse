# Project Structure

This document explains the structure of the DualSense Controller Mapper project for Runiverse.

## File Structure

```
dualsense-mapper/
├── .github/                    # GitHub specific files
│   └── workflows/              # GitHub Actions workflows
│       └── build.yml           # Workflow to build executable on release
├── dualsense_mapper_optimized.py  # Main application code
├── requirements.txt            # Python dependencies
├── build.bat                   # Script to build the executable
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
└── PROJECT_STRUCTURE.md        # This file
```

## Key Components

### Main Application (`dualsense_mapper_optimized.py`)

The main application file contains:

- Controller input handling using Pygame
- Keyboard and mouse simulation using PyAutoGUI
- GUI interface using Tkinter
- Mouse acceleration and smoothing algorithms

### Build Script (`build.bat`)

A Windows batch script that:

1. Installs required dependencies
2. Builds the executable using PyInstaller
3. Places the executable in the `dist` folder

### GitHub Actions Workflow (`.github/workflows/build.yml`)

Automates the build process when a new release is published:

1. Sets up a Windows environment
2. Installs dependencies
3. Builds the executable
4. Creates a ZIP archive
5. Uploads the archive to the release

## Dependencies

The project relies on the following main libraries:

- `pygame`: For controller input handling
- `pyautogui`: For keyboard and mouse simulation
- `tkinter`: For the GUI (comes with Python)
- `pyinstaller`: For creating the executable

## Configuration

The application has several configurable parameters:

- `MOUSE_SENSITIVITY`: Controls the base mouse movement speed
- `MOUSE_ACCELERATION`: Controls how much the mouse speed increases with movement
- `STICK_DEADZONE`: Minimum stick movement to register input
- `MOUSE_SMOOTHING`: Controls how smooth the mouse movement is
- `MOUSE_MIN_MOVE`: Minimum mouse movement to register

These can be adjusted in the main application file to suit different preferences. 