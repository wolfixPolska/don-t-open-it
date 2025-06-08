import win32gui
import ctypes
user32 = ctypes.windll.user32

# Function to get the window title
def get_window_title(hwnd):
    length = win32gui.GetWindowTextLength(hwnd)
    return win32gui.GetWindowText(hwnd)

# Function to check if a window is a valid application window (not a system window)
def is_valid_window(hwnd):
    # Check if the window is a top-level window and not a system dialog
    # Ignore windows without titles (like invisible or system windows)
    return win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != ""

# Function to get all application windows in the stack
def get_app_window_stack():
    hwnd_list = []

    # Enumerate all windows
    def enum_windows(hwnd, lparam):
        if is_valid_window(hwnd):
            hwnd_list.append(hwnd)

    # Enum all windows
    win32gui.EnumWindows(enum_windows, None)

    return hwnd_list

# Function to print only the top 3 app windows in the stack
def set_active_window(hwnd):
    # Bring the window to the foreground
    user32.SetForegroundWindow(hwnd)
