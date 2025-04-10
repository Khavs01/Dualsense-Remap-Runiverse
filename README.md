# DualSense PS5 Controller Mapper for Runiverse Game

A Python application that allows you to use your PlayStation 5 DualSense controller to play Runiverse (https://game.runiverse.world/) on PC by mapping controller inputs to keyboard and mouse actions.

## Features

- Map DualSense controller buttons to keyboard keys and mouse actions
- Use the right analog stick as a mouse with adjustable sensitivity
- Use the left analog stick for WASD movement
- Visual feedback for button presses
- Automatic reconnection if controller is disconnected
- Clean and simple GUI with status information and control mapping
- Configurable sensitivity and acceleration settings

## Requirements

- Windows 10/11
- Python 3.8 or higher
- PlayStation 5 DualSense controller
- USB connection

## Installation

1. Clone this repository:
```
git clone https://github.com/Khavs01/Dualsense-Remap-Runiverse.git
cd Dualsense-Remap-Runiverse
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python dualsense_mapper_optimized.py
```

## Running the Executable

If you prefer to run the pre-built executable from the `dist` folder:

1. Download the latest release or clone the repository
2. Navigate to the `dist` folder
3. Run `DualSense-Runiverse.exe`

### Windows Security Alert

When running the executable for the first time, you will likely see a Windows Defender SmartScreen warning message stating "Windows protected your PC" because the application is from an unverified publisher:

![Windows Defender Warning](https://raw.githubusercontent.com/Khavs01/Dualsense-Remap-Runiverse/master/windows_protect_unknown_publisher.png)

**This is normal and expected** for applications without a code signing certificate. To run the application:

1. Click on "More info" to expand the dialog
2. Click "Run anyway" to proceed with running the application
3. You only need to do this once; Windows will remember your choice for future use

**Why does this happen?** 
This warning appears because the executable is not digitally signed with a certificate from a trusted certificate authority. Obtaining such certificates requires payment and verification, which is typically done by commercial software but often not by free, open-source tools like this one.

**Removing the Warning**
The only way to completely remove this warning is to purchase a code signing certificate, which costs between $200-$400 per year. As this is an open-source project provided for free, this expense is currently not feasible. If you'd like to sponsor a code signing certificate to improve the user experience for everyone, you can contribute using the ETH address in the Donations section below.

**Is it safe?**
The application's complete source code is available in this repository for review. The executable is built directly from this source code without modifications.

If you have concerns, you can:
- Review the source code and build the executable yourself using the instructions in the "Building the Executable" section
- Run the Python script directly instead of using the pre-built executable
- Use an antivirus tool to scan the executable before running it

## Controls

| Controller Input | PC Action |
|-----------------|-----------|
| Left Stick      | WASD Movement |
| Right Stick     | Mouse Movement |
| L1 Button       | Enter (Chat/Confirm) |
| L2 Trigger      | E (Interact) |
| R2 Trigger      | Left Mouse Click |
| X Button        | Key 3 |
| Square Button   | Key 2 |
| Triangle Button | Key 1 |
| Circle Button   | Key 4 |
| D-Pad Up        | I (Inventory) |
| D-Pad Down      | C (Character) |
| D-Pad Left      | R (Mount/Unmount) |
| D-Pad Right     | M (Map) |

## Configuration

You can adjust the following settings in the code:

- `MOUSE_SENSITIVITY`: Base mouse sensitivity (default: 36)
- `MOUSE_ACCELERATION`: Mouse acceleration factor (default: 1.4)
- `STICK_DEADZONE`: Minimum stick movement to register input (default: 0.15)
- `MOUSE_SMOOTHING`: Mouse movement smoothing factor (default: 0.8)
- `MOUSE_MIN_MOVE`: Minimum mouse movement to register (default: 0.1)

## Features Details

### Visual Feedback
- Real-time visual indicators for button presses
- Color-coded button overlays
- Status window showing controller connection state

## Troubleshooting

- **Controller not detected**: Make sure your controller is connected via USB or Bluetooth and recognized by Windows
- **High latency**: Try reducing the `MOUSE_SMOOTHING` value
- **Too sensitive/not sensitive enough**: Adjust the `MOUSE_SENSITIVITY` value
- **Emergency stop**: Press L1 + R1 + L2 + R2 simultaneously to force close the application

## Building the Executable

To create a standalone executable:

1. Install PyInstaller:
```
pip install pyinstaller
```

2. Run the build script:
```
.\build.bat
```

3. The executable will be created in the `dist` folder

## Developer Information

### Contact
- Developer: Khavs
- Follow on X/Twitter: [@KhavsNFT](https://x.com/KhavsNFT)

### Donations
If you find this tool useful, consider supporting the developer:

- ETH/RON/MemeCoin/NFT: `0xf15304c1Be1c784Dd032343e81d6CEAbe3f00856`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created for the Runiverse gaming community
- [Pygame](https://www.pygame.org/) for controller input handling
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for keyboard and mouse simulation
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the graphical interface 