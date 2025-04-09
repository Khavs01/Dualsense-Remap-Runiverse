# DualSense PS5 Controller Mapper for Runiverse

A Python application that allows you to use your PlayStation 5 DualSense controller to play Runiverse (https://game.runiverse.world/) on PC by mapping controller inputs to keyboard and mouse actions.

## Features

- Map DualSense controller buttons to keyboard keys
- Use the right analog stick as a mouse with adjustable sensitivity
- Use the left analog stick for WASD movement
- Automatic reconnection if controller is disconnected
- Simple GUI with status information and control mapping
- Configurable sensitivity and acceleration settings

## Requirements

- Windows 10/11
- Python 3.8 or higher
- PlayStation 5 DualSense controller
- USB connection or Bluetooth adapter

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

## Controls

| Controller Input | PC Action |
|-----------------|-----------|
| Left Stick      | WASD Movement |
| Right Stick     | Mouse Movement |
| R2 Trigger      | Left Mouse Click |
| X Button        | Key 3 |
| Square Button   | Key 2 |
| Triangle Button | Key 1 |
| Circle Button   | Key 4 |
| L2 Trigger      | Key E |

## Configuration

You can adjust the following settings in the code:

- `MOUSE_SENSITIVITY`: Base mouse sensitivity (default: 18)
- `MOUSE_ACCELERATION`: Mouse acceleration factor (default: 1.4)
- `STICK_DEADZONE`: Minimum stick movement to register input (default: 0.15)
- `MOUSE_SMOOTHING`: Mouse movement smoothing factor (default: 0.8)
- `MOUSE_MIN_MOVE`: Minimum mouse movement to register (default: 0.1)

## Troubleshooting

- **Controller not detected**: Make sure your controller is connected via USB or Bluetooth and recognized by Windows
- **High latency**: Try reducing the `MOUSE_SMOOTHING` value
- **Too sensitive/not sensitive enough**: Adjust the `MOUSE_SENSITIVITY` value

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created for the Runiverse gaming community
- [Pygame](https://www.pygame.org/) for controller input handling
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for keyboard and mouse simulation 