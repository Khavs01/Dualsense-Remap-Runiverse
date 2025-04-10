# Project Structure

This document explains the structure of the DualSense Controller Mapper project for Runiverse.

## File Structure

```
dualsense-mapper/
├── .github/                    # GitHub specific files
│   └── workflows/              # GitHub Actions workflows
│       └── build.yml          # Workflow to build executable on release
├── dualsense_mapper_optimized.py  # Main application code
├── dualsense_mapper_backup_working.py  # Backup of working version
├── Dualsense-PS5.png          # Controller image for GUI
├── image_base64.txt           # Base64-encoded image data for embedding
├── requirements.txt           # Python dependencies
├── build.bat                  # Script to build the executable
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
└── PROJECT_STRUCTURE.md       # This file
```

## Key Components

### Main Application (`dualsense_mapper_optimized.py`)

The main application file contains:

- Controller input handling using Pygame
- Keyboard and mouse simulation using PyAutoGUI
- Simple GUI interface using Tkinter
- Mouse acceleration and smoothing algorithms
- Visual feedback system with button overlays
- Controller reconnection handling
- Developer information and donation options
- Clipboard functionality for ETH address copying

### Backup File (`dualsense_mapper_backup_working.py`)

A backup of the last known working version of the application, maintained for safety.

### Build Script (`build.bat`)

A Windows batch script that:

1. Installs required dependencies
2. Converts the controller image to base64 for embedding
3. Builds the executable using PyInstaller with proper options
4. Places the executable in the `dist` folder
5. Tests the executable after building

### Image Files

- `Dualsense-PS5.png`: Original image of the DualSense controller used in the GUI
- `image_base64.txt`: Base64-encoded version of the image for embedding in the executable

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
- `pillow`: For image handling in the GUI
- `pyinstaller`: For creating the executable

## Configuration

The application has several configurable parameters:

- `MOUSE_SENSITIVITY`: Controls the base mouse movement speed
- `MOUSE_ACCELERATION`: Controls how much the mouse speed increases with movement
- `STICK_DEADZONE`: Minimum stick movement to register input
- `MOUSE_SMOOTHING`: Controls how smooth the mouse movement is
- `MOUSE_MIN_MOVE`: Minimum mouse movement to register

These can be adjusted in the main application file to suit different preferences.

## User Interface Features

- Real-time visual feedback for controller inputs
- Status information and connection state
- Button mapping display for easy reference
- Developer contact information
- Donation address with copy-to-clipboard functionality
- Emergency stop combination (L1+R1+L2+R2)

## Building and Distribution

The project can be built into a standalone executable using the included build script, which handles:

1. Installing dependencies from `requirements.txt`
2. Preparing resources (images, etc.) for embedding
3. Configuring PyInstaller to create a single-file executable
4. Placing the built executable in the `dist` folder

This allows end-users to run the application without installing Python or any dependencies. 