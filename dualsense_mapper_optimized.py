import pygame
import pyautogui
import time
from threading import Thread
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser
import io
import base64

# Initializing debug logs
debug_log = []
def add_log(message):
    global debug_log
    debug_log.append(f"{time.strftime('%H:%M:%S')}: {message}")
    print(f"DEBUG: {message}")
    if len(debug_log) > 100:
        debug_log = debug_log[-100:]

# Load the base64 image from file
def load_base64_image():
    try:
        # First, try to load using PyInstaller path (if packaged)
        if hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, 'image_base64.txt')
            add_log(f"Looking for base64 image at: {path}")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    add_log("Loaded base64 image from PyInstaller path")
                    return f.read()
        
        # If not packaged, try the development path
        path = os.path.join(os.path.abspath("."), 'image_base64.txt')
        add_log(f"Looking for base64 image at: {path}")
        if os.path.exists(path):
            with open(path, 'r') as f:
                add_log("Loaded base64 image from development path")
                return f.read()
                
        add_log("Base64 image file not found in any location")
        return None
    except Exception as e:
        add_log(f"Error loading base64 from file: {e}")
        return None

# DualSense image embedded as base64
DUALSENSE_IMAGE_BASE64 = load_base64_image()

# Function to get the image from embedded data
def get_embedded_image():
    """Returns the DualSense image from embedded base64 data"""
    try:
        if not DUALSENSE_IMAGE_BASE64:
            add_log("No embedded image data available")
            return load_image_from_file()
            
        # Decode base64 to bytes
        image_data = base64.b64decode(DUALSENSE_IMAGE_BASE64)
        # Create an image object from bytes
        image = Image.open(io.BytesIO(image_data))
        add_log("Successfully loaded embedded image")
        return image
    except Exception as e:
        add_log(f"Error loading embedded image: {e}")
        # Fall back to file-based loading if embedded fails
        return load_image_from_file()

# Fallback function to load image from file
def load_image_from_file():
    """Fallback to load image from file if embedded fails"""
    try:
        image_path = resource_path("Dualsense-PS5.png")
        add_log(f"Attempting to load image from file: {image_path}")
        image = Image.open(image_path)
        add_log("Successfully loaded image from file")
        return image
    except Exception as e:
        add_log(f"Error loading image from file: {e}")
        return None

# Function to get the correct file path
def resource_path(relative_path):
    """Returns the correct path for files in packaged or development environments"""
    try:
        if hasattr(sys, '_MEIPASS'):
            # Temporary path used by PyInstaller
            base_path = sys._MEIPASS
            add_log(f"Using PyInstaller path: {base_path}")
        else:
            # Normal relative path when running the script directly
            base_path = os.path.abspath(".")
            add_log(f"Using development path: {base_path}")
        
        full_path = os.path.join(base_path, relative_path)
        add_log(f"Full resource path: {full_path}")
        add_log(f"Resource exists: {os.path.exists(full_path)}")
        return full_path
    except Exception as e:
        add_log(f"Error in resource_path: {e}")
        return relative_path

# PyAutoGUI safety configuration
pyautogui.FAILSAFE = False  # Disable mouse failsafe
pyautogui.PAUSE = 0.001

# Security settings
MAX_MOUSE_SPEED = 150  # Maximum pixels per frame
INPUT_RATE_LIMIT = 0.016  # ~60fps
EMERGENCY_STOP_COMBO = False
last_input_time = 0

# Sensitivity settings
MOUSE_SENSITIVITY = 36  # Current sensitivity
MOUSE_ACCELERATION = 1.4
STICK_DEADZONE = 0.15
STICK_SENSITIVITY = 0.8

# Mouse smoothing settings
MOUSE_SMOOTHING = 0.8
MOUSE_MIN_MOVE = 0.1

# Global variables for control
running = True
controller_status = "Initializing..."
button_overlays = {}
init_timeout = 15  # Timeout in seconds for initialization

def show_security_warning():
    """Shows security information to the user"""
    messagebox.showinfo("Security Information", 
        "Important Security Information:\n\n" +
        "1. Press L1 + R1 + L2 + R2 for emergency stop\n" +
        "2. The program only works with the Runiverse game\n" +
        "3. All inputs are rate-limited for safety\n\n" +
        "By clicking OK, you acknowledge these safety measures."
    )

def emergency_stop(root, reason="Emergency stop activated"):
    """Safely stops all program operations"""
    global running
    running = False
    
    # Release all held keys
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')
    pyautogui.mouseUp()
    
    messagebox.showwarning("Emergency Stop", f"Program stopped: {reason}")
    root.destroy()
    sys.exit(0)

def validate_mouse_movement(x_move, y_move):
    """Validates and limits mouse movement"""
    if abs(x_move) > MAX_MOUSE_SPEED or abs(y_move) > MAX_MOUSE_SPEED:
        return x_move * (MAX_MOUSE_SPEED / abs(x_move)), y_move * (MAX_MOUSE_SPEED / abs(y_move))
    return x_move, y_move

def rate_limit_check():
    """Checks if input rate is within limits"""
    global last_input_time
    current_time = time.time()
    if current_time - last_input_time < INPUT_RATE_LIMIT:
        return False
    last_input_time = current_time
    return True

def create_button_overlay(canvas, x, y, width, height, tag, color='#00ff00', opacity='gray50'):
    """Creates a semi-transparent button overlay"""
    overlay = canvas.create_oval(
        x, y, x + width, y + height,
        fill='',
        outline=color,
        width=2,
        tags=tag
    )
    
    button_overlays[tag] = {
        'id': overlay,
        'active': False,
        'color': color,
        'opacity': opacity
    }
    return overlay

def update_button_state(canvas, tag, active):
    """Updates the visual state of a button"""
    if tag in button_overlays:
        overlay = button_overlays[tag]
        canvas.itemconfig(
            overlay['id'],
            fill=overlay['color'] if active else '',
            outline=overlay['color'],
            width=2,
            state='normal'
        )
        overlay['active'] = active
        canvas.update_idletasks()

def copy_to_clipboard(root, text):
    """Copy text to clipboard and show brief confirmation"""
    root.clipboard_clear()
    root.clipboard_append(text)
    
    # Create brief confirmation popup that auto-dismisses
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.geometry(f"+{root.winfo_pointerx()+10}+{root.winfo_pointery()+10}")
    popup.config(bg='#3a3a3a')
    
    label = tk.Label(popup, text="Copied to clipboard!", bg='#3a3a3a', fg='white', 
                     padx=10, pady=5, font=("Arial", 9))
    label.pack()
    
    # Auto-dismiss after 1 second
    popup.after(1000, popup.destroy)

def create_status_window():
    """Creates a status window with DualSense image"""
    root = tk.Tk()
    root.title("DualSense Controller")
    
    # Configure theme with purple background
    root.configure(bg='#8c468c')
    style = ttk.Style()
    style.configure('TFrame', background='#8c468c')
    style.configure('TLabel', background='#8c468c', foreground='#ffffff')
    style.configure('TButton', background='#8c468c', foreground='#ffffff')
    style.configure('TLabelframe', background='#8c468c', foreground='#ffffff')
    style.configure('TLabelframe.Label', background='#8c468c', foreground='#ffffff')
    
    # Custom style for Quit button
    quit_button_style = {
        'background': '#752770',
        'foreground': '#ffffff',
        'activebackground': '#8c468c',
        'activeforeground': '#ffffff',
        'relief': 'raised',
        'borderwidth': 2,
        'padx': 20,
        'pady': 5,
        'font': ('Arial', 10, 'bold')
    }
    
    def quit_app(root):
        """Function to properly close the program"""
        global running
        running = False
        root.destroy()
    
    # Configure window size
    window_width = 800
    window_height = 900
    
    # Center window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Create main frame
    main_frame = ttk.Frame(root, padding=10, style='TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Status label frame
    top_frame = ttk.Frame(main_frame, style='TFrame')
    top_frame.pack(fill=tk.X, pady=5)
    
    status_label = ttk.Label(top_frame, text="Status: Initializing...", font=("Arial", 10, "bold"))
    status_label.pack(side=tk.LEFT, pady=5)
    
    # Frame for the image
    image_frame = ttk.Frame(main_frame)
    image_frame.pack(fill=tk.BOTH, expand=False)
    
    # Load DualSense image directly from embedded data
    add_log("Attempting to load embedded DualSense image")
    try:
        # Try to load the embedded image first
        image = get_embedded_image()
        
        if image:
            add_log("Processing the loaded image")
            image_width = int(window_width * 0.6)
            wpercent = image_width / float(image.size[0])
            hsize = int(float(image.size[1]) * float(wpercent))
            image = image.resize((image_width, hsize), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Create canvas for image and overlays
            canvas = tk.Canvas(image_frame, width=image.width, height=image.height, bg='#734373', highlightthickness=0)
            canvas.pack(pady=5)
            
            # Display the DualSense image
            canvas.create_image(0, 0, image=photo, anchor="nw")
            canvas._image = photo
        else:
            raise Exception("Failed to load image from any source")
    except Exception as e:
        add_log(f"Error processing image: {e}")
        # Fallback to a blank canvas if image loading fails
        canvas = tk.Canvas(image_frame, width=480, height=300, bg='#734373', highlightthickness=0)
        canvas.pack(pady=5)
        canvas.create_text(240, 150, text="Image not found", fill="white", font=("Arial", 14))
    
    # Frame for button mappings
    mappings_frame = ttk.LabelFrame(main_frame, text="Button Mappings", padding=10, style='TLabelframe')
    mappings_frame.pack(fill=tk.X, expand=False, pady=10)
    
    # Grid for mappings in 3 columns
    mappings = [
        ("Left Analog", "WASD Movement"),
        ("Right Analog", "Mouse Movement"),
        ("L1", "Enter (Chat/Confirm)"),
        ("D-Pad Left", "R (Mount/Unmount)"),
        ("D-Pad Right", "M (Map)"),
        ("D-Pad Down", "C (Character)"),
        ("D-Pad Up", "I (Inventory)"),
        ("L2", "E (Interact)"),
        ("R2", "Left Click"),
        ("X (Blue)", "Key 3"),
        ("Circle (Red)", "Key 4"),
        ("Square (Pink)", "Key 2"),
        ("Triangle (Green)", "Key 1")
    ]
    
    # Create three columns for better organization
    col_size = len(mappings) // 3 + (1 if len(mappings) % 3 else 0)
    for i, (button, action) in enumerate(mappings):
        row = i % col_size
        col = i // col_size * 2
        
        ttk.Label(mappings_frame, text=button + ":", font=("Arial", 9, "bold")).grid(
            row=row, column=col, sticky="e", padx=5, pady=2
        )
        ttk.Label(mappings_frame, text=action, font=("Arial", 9)).grid(
            row=row, column=col+1, sticky="w", padx=5, pady=2
        )
    
    # Quit button
    quit_button = tk.Button(main_frame, text="Quit", command=lambda: quit_app(root), **quit_button_style)
    quit_button.pack(pady=5)
    
    # Add shadow effect to quit button
    def on_enter(e):
        quit_button['background'] = '#8c468c'
    
    def on_leave(e):
        quit_button['background'] = '#752770'
    
    quit_button.bind("<Enter>", on_enter)
    quit_button.bind("<Leave>", on_leave)
    
    # Developer info frame
    dev_frame = ttk.Frame(main_frame, style='TFrame')
    dev_frame.pack(fill=tk.X, pady=10)
    
    # Developer info with hyperlinks
    dev_info = [
        ("© 2025 DualSense Mapper for Runiverse", None),
        ("Follow on X: @KhavsNFT", "https://x.com/KhavsNFT"),
        ("Donations (ETH/RON/MemeCoin/NFT):", None),
    ]
    
    for text, link in dev_info:
        if link:
            label = ttk.Label(dev_frame, text=text, font=("Arial", 9), foreground='#00aaff', cursor="hand2")
            label.bind("<Button-1>", lambda e, url=link: webbrowser.open_new(url))
        else:
            label = ttk.Label(dev_frame, text=text, font=("Arial", 9), foreground='#ffffff')
        label.pack(anchor='center')
    
    # Address frame with copy button
    address_frame = ttk.Frame(dev_frame)
    address_frame.pack(anchor='center')
    
    eth_address = "0xf15304c1Be1c784Dd032343e81d6CEAbe3f00856"
    address_label = ttk.Label(address_frame, text=eth_address, font=("Arial", 9), foreground='#ffffff')
    address_label.pack(side=tk.LEFT, padx=(0, 5))
    
    # Copy button style
    copy_button_style = {
        'background': '#333333',
        'foreground': '#ffffff',
        'activebackground': '#444444',
        'activeforeground': '#ffffff',
        'relief': 'flat',
        'borderwidth': 0,
        'padx': 5,
        'pady': 0,
        'font': ('Arial', 8),
        'width': 2,
        'height': 1
    }
    
    # Create copy button with symbol
    copy_button = tk.Button(address_frame, text="📋", command=lambda: copy_to_clipboard(root, eth_address), **copy_button_style)
    copy_button.pack(side=tk.LEFT)
    
    # Make the address itself clickable too
    address_label.bind("<Button-1>", lambda e: copy_to_clipboard(root, eth_address))
    address_label.config(cursor="hand2")
    
    # Create button overlays with fixed positions
    create_button_overlay(canvas, 364, 199, 20, 20, "button_x", '#1e90ff', 'gray25')  # X (blue)
    create_button_overlay(canvas, 394, 169, 20, 20, "button_circle", '#ff4444', 'gray25')  # Circle (red)
    create_button_overlay(canvas, 333, 170, 20, 20, "button_square", '#ff69b4', 'gray25')  # Square (pink)
    create_button_overlay(canvas, 366, 136, 20, 20, "button_triangle", '#90ee90', 'gray25')  # Triangle (green)
    
    create_button_overlay(canvas, 116, 167, 20, 20, "dpad_right", '#00ff00', 'gray25')  # Right - Map
    create_button_overlay(canvas, 75, 170, 20, 20, "dpad_left", '#00ff00', 'gray25')   # Left - Mount
    create_button_overlay(canvas, 95, 148, 20, 20, "dpad_up", '#00ff00', 'gray25')     # Up - Inventory
    create_button_overlay(canvas, 96, 187, 20, 20, "dpad_down", '#00ff00', 'gray25')   # Down - Character
    
    create_button_overlay(canvas, 153, 221, 30, 30, "stick_left", '#00ff00', 'gray25')  # Left analog
    create_button_overlay(canvas, 291, 222, 30, 30, "stick_right", '#00ff00', 'gray25')  # Right analog
    
    create_button_overlay(canvas, 37, 55, 20, 20, "button_l1", '#00aaff', 'gray25')  # L1 - Enter/Chat
    create_button_overlay(canvas, 421, 60, 20, 20, "button_r1", '#00aaff', 'gray25')  # R1
    create_button_overlay(canvas, 38, 26, 20, 20, "button_l2", '#00aaff', 'gray25')   # L2 - Interact
    create_button_overlay(canvas, 422, 28, 20, 20, "button_r2", '#00aaff', 'gray25')   # R2 - Left Click
    
    def update_status():
        status_label.config(text=f"Status: {controller_status}")
        if running:
            root.after(100, update_status)
    
    update_status()
    root.protocol("WM_DELETE_WINDOW", lambda: quit_app(root))
    return root, canvas

def apply_mouse_acceleration(value):
    """Applies smooth acceleration to mouse movement"""
    if abs(value) < 0.3:
        return value * 0.4
    elif abs(value) < 0.6:
        return value * 0.7
    return (abs(value) ** MOUSE_ACCELERATION) * (1 if value >= 0 else -1)

def show_debug_info():
    """Shows debug information to help diagnose issues"""
    try:
        # Coletar informações do sistema
        system_info = [
            f"Python version: {sys.version}",
            f"Pygame installed: {'Yes' if 'pygame' in sys.modules else 'No'}",
            f"PyAutoGUI installed: {'Yes' if 'pyautogui' in sys.modules else 'No'}",
            f"Working directory: {os.getcwd()}",
            f"Has image file: {'Yes' if os.path.exists('Dualsense-PS5.png') else 'No'}",
            f"Debug log: {debug_log}"
        ]
        
        # Display in messagebox
        messagebox.showinfo("Debug Information", "\n".join(system_info))
    except Exception as e:
        messagebox.showerror("Error showing debug info", str(e))

def handle_controller(canvas):
    global controller_status, running, EMERGENCY_STOP_COMBO, init_timeout
    
    try:
        controller_status = "Initializing DualSense controller..."
        add_log("Starting controller initialization")
        
        try:
            add_log("Initializing pygame")
            pygame.init()
            add_log("Pygame initialized successfully")
        except Exception as e:
            add_log(f"Pygame initialization error: {e}")
            controller_status = f"Error initializing pygame: {e}"
            return
        
        try:
            add_log("Initializing pygame joystick")
            pygame.joystick.init()
            add_log("Pygame joystick initialized successfully")
        except Exception as e:
            add_log(f"Pygame joystick initialization error: {e}")
            controller_status = f"Error initializing joystick: {e}"
            return
        
        add_log(f"Joystick count: {pygame.joystick.get_count()}")
        while pygame.joystick.get_count() == 0 and running:
            controller_status = "Waiting for controller connection..."
            pygame.joystick.quit()
            add_log("Reinitializing joystick module")
            pygame.joystick.init()
            add_log(f"New joystick count: {pygame.joystick.get_count()}")
            time.sleep(1)
        
        if not running:
            add_log("Program terminated while waiting for controller")
            return
        
        add_log("Joystick detected, initializing controller")
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        
        add_log(f"Controller name: {joystick.get_name()}")
        if "DualSense" not in joystick.get_name():
            add_log(f"Warning: Controller detected is not DualSense: {joystick.get_name()}")
        
        controller_status = f"Connected: {joystick.get_name()}"
        
        # Button mapping
        BUTTON_X = 0
        BUTTON_SQUARE = 2
        BUTTON_TRIANGLE = 3
        BUTTON_CIRCLE = 1
        BUTTON_L1 = 9
        BUTTON_R1 = 10
        
        # Trigger thresholds for emergency stop
        L2_THRESHOLD = 0.5
        R2_THRESHOLD = 0.5
        
        # Emergency stop state
        emergency_buttons = {
            'L1': False,
            'R1': False,
            'L2': False,
            'R2': False
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
            'target_y': 0.0,
            'last_update': time.time()
        }
        
        last_update = time.time()
        
        while running:
            try:
                if not rate_limit_check():
                    continue
                
                current_time = time.time()
                delta_time = current_time - last_update
                last_update = current_time
                
                for event in pygame.event.get():
                    # Check for emergency stop combo
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == BUTTON_L1:
                            emergency_buttons['L1'] = True
                        elif event.button == BUTTON_R1:
                            emergency_buttons['R1'] = True
                    
                    elif event.type == pygame.JOYBUTTONUP:
                        if event.button == BUTTON_L1:
                            emergency_buttons['L1'] = False
                        elif event.button == BUTTON_R1:
                            emergency_buttons['R1'] = False
                    
                    elif event.type == pygame.JOYAXISMOTION:
                        if event.axis == 4:  # L2
                            emergency_buttons['L2'] = event.value > L2_THRESHOLD
                        elif event.axis == 5:  # R2
                            emergency_buttons['R2'] = event.value > R2_THRESHOLD
                    
                    # Check if all emergency buttons are pressed
                    if all(emergency_buttons.values()):
                        emergency_stop(root, "Emergency stop combo activated (L1 + R1 + L2 + R2)")
                        return
                    
                    # Normal input handling
                    if event.type == pygame.JOYAXISMOTION:
                        # Left analog (axis 0 and 1)
                        if event.axis == 0:  # X axis
                            if abs(event.value) > STICK_DEADZONE:
                                if event.value < 0 and not key_states['a']:
                                    pyautogui.keyDown('a')
                                    key_states['a'] = True
                                    canvas.after(1, lambda: update_button_state(canvas, "stick_left", True))
                                elif event.value > 0 and not key_states['d']:
                                    pyautogui.keyDown('d')
                                    key_states['d'] = True
                                    canvas.after(1, lambda: update_button_state(canvas, "stick_left", True))
                            else:
                                if key_states['a']:
                                    pyautogui.keyUp('a')
                                    key_states['a'] = False
                                if key_states['d']:
                                    pyautogui.keyUp('d')
                                    key_states['d'] = False
                                canvas.after(1, lambda: update_button_state(canvas, "stick_left", False))
                        
                        elif event.axis == 1:  # Y axis
                            if abs(event.value) > STICK_DEADZONE:
                                if event.value < 0 and not key_states['w']:
                                    pyautogui.keyDown('w')
                                    key_states['w'] = True
                                    canvas.after(1, lambda: update_button_state(canvas, "stick_left", True))
                                elif event.value > 0 and not key_states['s']:
                                    pyautogui.keyDown('s')
                                    key_states['s'] = True
                                    canvas.after(1, lambda: update_button_state(canvas, "stick_left", True))
                            else:
                                if key_states['w']:
                                    pyautogui.keyUp('w')
                                    key_states['w'] = False
                                if key_states['s']:
                                    pyautogui.keyUp('s')
                                    key_states['s'] = False
                                canvas.after(1, lambda: update_button_state(canvas, "stick_left", False))
                        
                        # Right analog (axis 2 and 3)
                        elif event.axis == 2:  # Right X axis
                            if abs(event.value) > STICK_DEADZONE:
                                mouse_state['x'] = event.value * STICK_SENSITIVITY
                                canvas.after(1, lambda: update_button_state(canvas, "stick_right", True))
                            else:
                                mouse_state['x'] = 0.0
                                canvas.after(1, lambda: update_button_state(canvas, "stick_right", False))
                        
                        elif event.axis == 3:  # Right Y axis
                            if abs(event.value) > STICK_DEADZONE:
                                mouse_state['y'] = event.value * STICK_SENSITIVITY
                                canvas.after(1, lambda: update_button_state(canvas, "stick_right", True))
                            else:
                                mouse_state['y'] = 0.0
                                canvas.after(1, lambda: update_button_state(canvas, "stick_right", False))
                        
                        # Triggers (axis 4 and 5)
                        elif event.axis == 4:  # L2
                            if event.value > 0.5:
                                pyautogui.press('e')
                                canvas.after(1, lambda: update_button_state(canvas, "button_l2", True))
                            else:
                                canvas.after(1, lambda: update_button_state(canvas, "button_l2", False))
                        elif event.axis == 5:  # R2
                            if event.value > 0.5:
                                canvas.after(1, lambda: update_button_state(canvas, "button_r2", True))
                                pyautogui.mouseDown(button='left')
                            else:
                                canvas.after(1, lambda: update_button_state(canvas, "button_r2", False))
                                pyautogui.mouseUp(button='left')
                    
                    elif event.type == pygame.JOYBUTTONDOWN:
                        if event.button == BUTTON_X:
                            pyautogui.press('3')
                            canvas.after(1, lambda: update_button_state(canvas, "button_x", True))
                        elif event.button == BUTTON_SQUARE:
                            pyautogui.press('2')
                            canvas.after(1, lambda: update_button_state(canvas, "button_square", True))
                        elif event.button == BUTTON_TRIANGLE:
                            pyautogui.press('1')
                            canvas.after(1, lambda: update_button_state(canvas, "button_triangle", True))
                        elif event.button == BUTTON_CIRCLE:
                            pyautogui.press('4')
                            canvas.after(1, lambda: update_button_state(canvas, "button_circle", True))
                        elif event.button == BUTTON_L1:
                            pyautogui.press('enter')
                            canvas.after(1, lambda: update_button_state(canvas, "button_l1", True))
                        elif event.button == BUTTON_R1:
                            canvas.after(1, lambda: update_button_state(canvas, "button_r1", True))
                        # D-Pad handlers
                        elif event.button == 11:  # D-Pad Up
                            pyautogui.press('i')
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_up", True))
                        elif event.button == 12:  # D-Pad Down
                            pyautogui.press('c')
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_down", True))
                        elif event.button == 13:  # D-Pad Left
                            pyautogui.press('r')
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_left", True))
                        elif event.button == 14:  # D-Pad Right
                            pyautogui.press('m')
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_right", True))
                    
                    elif event.type == pygame.JOYBUTTONUP:
                        if event.button == BUTTON_X:
                            canvas.after(1, lambda: update_button_state(canvas, "button_x", False))
                        elif event.button == BUTTON_SQUARE:
                            canvas.after(1, lambda: update_button_state(canvas, "button_square", False))
                        elif event.button == BUTTON_TRIANGLE:
                            canvas.after(1, lambda: update_button_state(canvas, "button_triangle", False))
                        elif event.button == BUTTON_CIRCLE:
                            canvas.after(1, lambda: update_button_state(canvas, "button_circle", False))
                        elif event.button == BUTTON_L1:
                            canvas.after(1, lambda: update_button_state(canvas, "button_l1", False))
                        elif event.button == BUTTON_R1:
                            canvas.after(1, lambda: update_button_state(canvas, "button_r1", False))
                        elif event.button == 11:  # D-Pad Up
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_up", False))
                        elif event.button == 12:  # D-Pad Down
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_down", False))
                        elif event.button == 13:  # D-Pad Left
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_left", False))
                        elif event.button == 14:  # D-Pad Right
                            canvas.after(1, lambda: update_button_state(canvas, "dpad_right", False))
                    
                    elif event.type == pygame.JOYDEVICEREMOVED:
                        controller_status = "Controller disconnected. Reconnecting..."
                        # Release all keys before reconnecting
                        for key in key_states:
                            if key_states[key]:
                                pyautogui.keyUp(key)
                                key_states[key] = False
                        
                        # Reset all button overlays
                        for tag in button_overlays:
                            canvas.after(1, lambda t=tag: update_button_state(canvas, t, False))
                        
                        pygame.joystick.quit()
                        pygame.joystick.init()
                        while pygame.joystick.get_count() == 0 and running:
                            time.sleep(1)
                        if running:
                            joystick = pygame.joystick.Joystick(0)
                            joystick.init()
                            if "DualSense" not in joystick.get_name():
                                emergency_stop(root, "Unsupported controller detected after reconnection")
                                return
                            controller_status = "Controller reconnected!"
                
                # Mouse movement with validation and smoothing
                if abs(mouse_state['x']) > MOUSE_MIN_MOVE or abs(mouse_state['y']) > MOUSE_MIN_MOVE:
                    # Apply acceleration and sensitivity
                    x_move = apply_mouse_acceleration(mouse_state['x']) * MOUSE_SENSITIVITY
                    y_move = apply_mouse_acceleration(mouse_state['y']) * MOUSE_SENSITIVITY
                    
                    # Validate movement
                    x_move, y_move = validate_mouse_movement(x_move, y_move)
                    
                    # Apply time-based smoothing
                    x_move *= delta_time * 60  # Normalize to 60 FPS
                    y_move *= delta_time * 60
                    
                    # Move mouse
                    try:
                        pyautogui.moveRel(int(x_move), int(y_move))
                    except ValueError:
                        pass  # Ignore invalid movements
                
                time.sleep(0.001)  # Small sleep to prevent CPU overuse
                
            except Exception as e:
                controller_status = f"Error: {e}"
                time.sleep(1)
                
    except Exception as e:
        add_log(f"Critical error in handle_controller: {e}")
        emergency_stop(root, f"Critical error: {e}")

if __name__ == "__main__":
    try:
        add_log("Program starting")
        root, canvas = create_status_window()
        
        # Add debug button to main window
        debug_button_style = {
            'background': '#555555',
            'foreground': '#ffffff',
            'activebackground': '#777777',
            'activeforeground': '#ffffff',
            'relief': 'raised',
            'borderwidth': 2,
            'padx': 10,
            'pady': 3,
            'font': ('Arial', 8)
        }
        
        debug_frame = ttk.Frame(root)
        debug_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        debug_button = tk.Button(debug_frame, text="Debug Info", command=show_debug_info, **debug_button_style)
        debug_button.pack(side=tk.RIGHT, padx=10)
        
        show_security_warning()
        add_log("Starting controller thread")
        controller_thread = Thread(target=handle_controller, args=(canvas,))
        controller_thread.daemon = True
        controller_thread.start()
        add_log("Main GUI loop starting")
        root.mainloop()
    except Exception as e:
        add_log(f"Critical error in main: {e}")
        print(f"Critical error: {e}")
    finally:
        add_log("Program shutdown")
        pygame.quit()
        sys.exit(0)