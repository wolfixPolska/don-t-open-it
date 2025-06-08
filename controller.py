import pygame
import sys
import multiprocessing
import mouse
from time import sleep
import keyboard
from vkeyboard import start_vk
from notiefier import *
from settings import *



class Controller:
    def __init__(self,controller:pygame.joystick.JoystickType):
        self.k_process = multiprocessing.Process(target=start_vk)

        self.show_keyboard = False
        self.controller = controller
        self.axis_deadpoint=0.15
        self.back_buttons_deadpoint=0.3
        self.controller_name = self.controller.get_name()
        self.mouse_speed = 60
        self.active = True
        ############################################################
        buttons = self.controller.get_numbuttons()
        self.buttons = []
        for x in range(buttons):
            self.buttons.append(0)
        ############################################################
        axes = self.controller.get_numaxes()
        self.axes = []
        for _ in range(axes):
            self.axes.append(0)


    def check_events(self,events):

        for event in events:

            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
                self.buttons[event.button]=1
                
                self.keybinds(event.button,1)
                if self.active:
                    self.mouse_events(event.button,1)
                
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")
                self.buttons[event.button]=0
                
                self.keybinds(event.button,0)
                if self.active:
                    self.mouse_events(event.button,0)

            elif event.type == pygame.JOYAXISMOTION:
                if event.value >= self.axis_deadpoint or event.value <= -self.axis_deadpoint:
                    #print(f"Axis {event.axis} moved to {event.value}")
                    self.axes[event.axis]=event.value
                else:
                    self.axes[event.axis]=0

            elif event.type == pygame.JOYDEVICEREMOVED:
                print("Joystick Alert")
                start_notifications("Connection lost" , f"Lost connection with {self.controller_name}\n waiting for new one (10s)")
                for _ in range(50):
                    if pygame.joystick.get_count() > 0:
                        self.controller = pygame.joystick.Joystick(0)
                        self.controller.init()
                        start_notifications("Joystick connected", f"Joystick connected, name: {self.controller.get_name()}")
                        self.controller_name = self.controller.get_name()
                        return
                    sleep(0.2)

                self.controller.quit()
                start_notifications("Connection lost" , "Controller don't found\nExiting...")
                sys.exit(1)

        if self.active:
            if self.buttons[10] == 1:
                mouse.wheel(-1)

            if self.buttons[9] == 1:
                mouse.wheel(1)

    def keybinds(self,b_event,press):
        if self.active and press == 1:

            match b_event:
                case 11: #UP ARROW
                    keyboard.send(UP_ARROW)

                case 12: #DOWN ARROW
                    keyboard.send(DOWN_ARROW)    

                case 13: #LEFT ARROW
                    keyboard.send(LEFT_ARROW)

                case 14: #RIGHT ARROW
                    keyboard.send(RIGHT_ARROW)

                case 2:
                    if self.buttons[4]==0: #special 1
                        keyboard.send(SQUARE_BUTTON)
                    else:
                        keyboard.send(SQUARE_BUTTON_SHARE)
                        
                case 3:
                    if self.buttons[4]==0: #special 1
                        keyboard.send(TRIANGLE_BUTTON)
                    else:
                        keyboard.send(TRIANGLE_BUTTON_SHARE)

                case 15:
                    
                    self.show_keyboard = not self.show_keyboard
                    if self.show_keyboard == True:
                        self.k_process.start()
                    else:
                        self.k_process.terminate()
                        self.k_process.join()
                        self.k_process = multiprocessing.Process(target=start_vk)

                    print(f"Keyboard visibility toggled to: {self.show_keyboard}")

        if b_event ==5 and press == 1: #PS BUTTON
            self.active = not self.active

            if not self.active:
                print("turning off")
                start_notifications("Joystick Alert" , "Turning off joystick control")
            else:
                print("turning on")
                start_notifications("Joystick Alert" , "Turning on joystick control")



    def mouse_events(self,event,press):
        if press == 1:  
            if event == 0: 
                mouse.press("left")
            elif event == 1:  
                mouse.press("right")
        
        elif press == 0:  
            if event == 0: 
                mouse.release("left")
            elif event == 1: 
                mouse.release("right")


    def mouse(self):
        if self.active:
            if self.axes[5] >= self.back_buttons_deadpoint:     
                mouse.move(self.axes[0]*self.mouse_speed*3,self.axes[1]*self.mouse_speed*3, absolute=False, duration=0.1)

            elif self.axes[4] >= self.back_buttons_deadpoint: 
                mouse.move(self.axes[0]*self.mouse_speed*0.3,self.axes[1]*self.mouse_speed*0.3, absolute=False, duration=0.1)

            else:
                mouse.move(self.axes[0]*self.mouse_speed,self.axes[1]*self.mouse_speed, absolute=False, duration=0.1)


def main():
    # Initialize Pygame
    pygame.init()

    # Initialize the joystick
    pygame.joystick.init()

    # Check for joystick
    if pygame.joystick.get_count() < 1:
        print("No joystick found.")
        pygame.quit()
        sys.exit()

    # Get the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick name: ", joystick.get_name())



    controller1 = Controller(joystick)


    try:
        while True:
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            controller1.check_events(events)    
            controller1.mouse()
            

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()