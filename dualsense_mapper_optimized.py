"""
DualSense PS5 Controller Mapper for Runiverse
-------------------------------------------
This application maps PlayStation 5 DualSense controller inputs to keyboard and mouse actions
for playing Runiverse (https://game.runiverse.world/).
"""

import pygame
import pyautogui
import time
from threading import Thread
import sys
import tkinter as tk
from tkinter import ttk

# PyAutoGUI safety configuration
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.001  # Minimum delay

# Sensitivity settings
MOUSE_SENSITIVITY = 18
MOUSE_ACCELERATION = 1.4
STICK_DEADZONE = 0.15
STICK_SENSITIVITY = 0.8

# Debounce settings
DEBOUNCE_TIME = 0.05

# Mouse smoothing settings
MOUSE_SMOOTHING = 0.8
MOUSE_MIN_MOVE = 0.1

# Global variables for control
running = True
controller_status = "Initializing..."

def create_status_window():
    """Creates a simple status window"""
    root = tk.Tk()
    root.title("DualSense Controller")
    root.geometry("350x260")
    root.resizable(False, False)
    
    # Status frame
    status_frame = ttk.Frame(root, padding=10)
    status_frame.pack(fill=tk.BOTH, expand=True)
    
    # Status label
    status_label = ttk.Label(status_frame, text="Status: Initializing...", font=("Arial", 10, "bold"))
    status_label.pack(pady=10)
    
    # Separator
    ttk.Separator(status_frame).pack(fill=tk.X, pady=5)
    
    # Instructions frame
    instructions_frame = ttk.LabelFrame(status_frame, text="Controls", padding=10)
    instructions_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Instructions
    instructions = [
        ("Left Stick", "WASD Movement"),
        ("Right Stick", "Mouse Movement"),
        ("R2 Trigger", "Left Mouse Click"),
        ("X Button", "Key 3"),
        ("Square Button", "Key 2"),
        ("Triangle Button", "Key 1"),
        ("Circle Button", "Key 4")
    ]
    
    for i, (control, action) in enumerate(instructions):
        ttk.Label(instructions_frame, text=control, font=("Arial", 9, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(instructions_frame, text="→", font=("Arial", 9)).grid(row=i, column=1, padx=5, pady=2)
        ttk.Label(instructions_frame, text=action, font=("Arial", 9)).grid(row=i, column=2, sticky="w", padx=5, pady=2)
    
    # Quit button
    quit_button = ttk.Button(status_frame, text="Quit", command=lambda: quit_app(root))
    quit_button.pack(pady=10)
    
    def quit_app(root):
        global running
        running = False
        root.destroy()
    
    def update_status():
        status_label.config(text=f"Status: {controller_status}")
        if running:
            root.after(100, update_status)
    
    update_status()
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", lambda: quit_app(root))
    
    return root

def apply_mouse_acceleration(value):
    """Applies smooth acceleration to mouse movement"""
    if abs(value) < 0.3:
        return value * 0.4  # Reduced for more precise small movements
    elif abs(value) < 0.6:
        return value * 0.7  # Middle range for smoother transition
    # Using power operation without math module
    return (abs(value) ** MOUSE_ACCELERATION) * (1 if value >= 0 else -1)

def handle_controller():
    global controller_status
    
    controller_status = "Initializing DualSense controller..."
    
    pygame.init()
    pygame.joystick.init()
    
    while pygame.joystick.get_count() == 0 and running:
        controller_status = "Waiting for controller connection..."
        pygame.joystick.quit()
        pygame.joystick.init()
        time.sleep(1)
    
    if not running:
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    controller_status = f"Connected: {joystick.get_name()}"
    
    # Button mapping
    BUTTON_X = 0
    BUTTON_SQUARE = 2
    BUTTON_TRIANGLE = 3
    BUTTON_CIRCLE = 1
    
    # Button states
    button_states = {
        BUTTON_X: False,
        BUTTON_SQUARE: False,
        BUTTON_TRIANGLE: False,
        BUTTON_CIRCLE: False
    }
    
    # Axis states
    axis_states = {
        0: 0.0,  # Left X axis
        1: 0.0,  # Left Y axis
        2: 0.0,  # Right X axis
        3: 0.0   # Right Y axis
    }
    
    # Key states
    key_states = {
        'w': False,
        'a': False,
        's': False,
        'd': False
    }
    
    # Mouse state
    mouse_state = {
        'x': 0.0,
        'y': 0.0,
        'target_x': 0.0,
        'target_y': 0.0
    }
    
    last_update = time.time()
    
    while running:
        try:
            current_time = time.time()
            delta_time = current_time - last_update
            last_update = current_time
            
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    axis_states[event.axis] = event.value
                    
                    # Left analog (axis 0 and 1)
                    if event.axis == 0:  # X axis
                        if abs(event.value) > STICK_DEADZONE:
                            if event.value < 0 and not key_states['a']:
                                pyautogui.keyDown('a')
                                key_states['a'] = True
                            elif event.value > 0 and not key_states['d']:
                                pyautogui.keyDown('d')
                                key_states['d'] = True
                        else:
                            if key_states['a']:
                                pyautogui.keyUp('a')
                                key_states['a'] = False
                            if key_states['d']:
                                pyautogui.keyUp('d')
                                key_states['d'] = False
                    
                    elif event.axis == 1:  # Y axis
                        if abs(event.value) > STICK_DEADZONE:
                            if event.value < 0 and not key_states['w']:
                                pyautogui.keyDown('w')
                                key_states['w'] = True
                            elif event.value > 0 and not key_states['s']:
                                pyautogui.keyDown('s')
                                key_states['s'] = True
                        else:
                            if key_states['w']:
                                pyautogui.keyUp('w')
                                key_states['w'] = False
                            if key_states['s']:
                                pyautogui.keyUp('s')
                                key_states['s'] = False
                    
                    # Right analog (axis 2 and 3)
                    elif event.axis == 2:  # Right X axis
                        if abs(event.value) > STICK_DEADZONE:
                            mouse_state['target_x'] = event.value
                        else:
                            mouse_state['target_x'] = 0.0
                    
                    elif event.axis == 3:  # Right Y axis
                        if abs(event.value) > STICK_DEADZONE:
                            mouse_state['target_y'] = event.value
                        else:
                            mouse_state['target_y'] = 0.0
                    
                    # Triggers (axis 4 and 5)
                    elif event.axis == 4:  # L2
                        if event.value > 0.5:
                            pyautogui.press('e')
                    
                    elif event.axis == 5:  # R2
                        if event.value > 0.5:
                            pyautogui.click()
                
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == BUTTON_X:
                        pyautogui.press('3')
                    elif event.button == BUTTON_SQUARE:
                        pyautogui.press('2')
                    elif event.button == BUTTON_TRIANGLE:
                        pyautogui.press('1')
                    elif event.button == BUTTON_CIRCLE:
                        pyautogui.press('4')
                
                elif event.type == pygame.JOYDEVICEREMOVED:
                    controller_status = "Controller disconnected. Reconnecting..."
                    # Release all keys before reconnecting
                    for key in key_states:
                        if key_states[key]:
                            pyautogui.keyUp(key)
                            key_states[key] = False
                    
                    pygame.joystick.quit()
                    pygame.joystick.init()
                    while pygame.joystick.get_count() == 0 and running:
                        time.sleep(1)
                    if running:
                        joystick = pygame.joystick.Joystick(0)
                        joystick.init()
                        controller_status = "Controller reconnected!"
            
            # Smooth mouse update
            mouse_state['x'] += (mouse_state['target_x'] - mouse_state['x']) * MOUSE_SMOOTHING
            mouse_state['y'] += (mouse_state['target_y'] - mouse_state['y']) * MOUSE_SMOOTHING
            
            # Apply acceleration and sensitivity
            if abs(mouse_state['x']) > MOUSE_MIN_MOVE or abs(mouse_state['y']) > MOUSE_MIN_MOVE:
                x_move = apply_mouse_acceleration(mouse_state['x']) * MOUSE_SENSITIVITY * delta_time * 120
                y_move = apply_mouse_acceleration(mouse_state['y']) * MOUSE_SENSITIVITY * delta_time * 120
                pyautogui.moveRel(x_move, y_move)
            
            time.sleep(0.001)
            
        except Exception as e:
            controller_status = f"Error: {e}"
            time.sleep(1)

if __name__ == "__main__":
    # Create the status window
    root = create_status_window()
    
    # Start the controller thread
    controller_thread = Thread(target=handle_controller)
    controller_thread.daemon = True
    controller_thread.start()
    
    # Run the main window
    root.mainloop()
    
    # Cleanup
    pygame.quit()
    sys.exit(0) 