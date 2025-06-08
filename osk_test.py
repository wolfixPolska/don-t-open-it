from pywinauto import Application
import time

# Start the On-Screen Keyboard
app = Application().start('osk.exe')

# Give the OSK some time to open
time.sleep(2)

# Access the On-Screen Keyboard window
osk_window = app.window(title='On-Screen Keyboard')

# Click a button (you need to know the button's name or control ID)
osk_window.Button('A').click()  # Click the 'A' key
osk_window.Button('B').click()  # Click the 'B' key

# Close the On-Screen Keyboard
osk_window.close()