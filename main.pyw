from controller import *
import threading
import pystray
from PIL import Image
from pystray import MenuItem, Icon
import pygame
import sys
import mouse
import keyboard
import vkeyboard
from notiefier import *
import settings
import time
running = True


def exit_action(icon, item):
    icon.stop()
    global running
    running = False




def main():
    pygame.init()
    pygame.joystick.init()


    while pygame.joystick.get_count() < 1:
        time.sleep(3)

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick name: ", joystick.get_name())
    start_notifications("Joystick connected", f"Joystick connected, name: {joystick.get_name()}")

    controller1 = Controller(joystick)
    global running 
    c1_active = True
    icon_image=Image.open(settings.PROGRAM_ICON)
    icon_image_off=Image.open(settings.PROGRAM_ICON_OFF)
    icon = Icon("test_icon",icon_image , "Controller driver", menu=pystray.Menu(
        MenuItem("Exit", exit_action)
    ))

    threading.Thread(target=icon.run, daemon=True).start()
    ######################################################################################
    try:
        while running:

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            if c1_active != controller1.active:
                if controller1.active == True:
                    icon.icon=icon_image
                elif controller1.active == False:
                    icon.icon=icon_image_off

                c1_active = controller1.active
                

            controller1.check_events(events)  
            controller1.mouse()
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()