import ctypes
import threading
import pystray
from PIL import Image
from pystray import MenuItem, Icon


# Function to exit the application
def exit_action(icon, item):
    icon.stop()


# Main function
def main():


    # Load your custom icon
    icon_image = Image.open("python.ico")  # Replace with your icon's filename or path

    # Create a system tray icon
    icon = Icon("test_icon", icon_image, "My Hidden App", menu=pystray.Menu(
        MenuItem("Exit", exit_action)
    ))

    # Run the icon in a separate thread
    threading.Thread(target=icon.run, daemon=True).start()

    # Keep the script running
    while True:
        pass  # Replace with your logic

if __name__ == "__main__":
    main()