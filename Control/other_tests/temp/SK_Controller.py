import pygame
from pygame.locals import *
import numpy as np
import time
import serial

ESP32_Handler = serial.Serial()
ESP32_Handler.port = "/dev/ttyUSB0"
ESP32_Handler.baudrate = 115200
#ESP32_Handler.open()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# Initialize values
P = 1000 #0-2000
I = 60 #0-2000
D = 0 #0-2000
Kl = 125 #0-1000
S = 20 #0-100
values = [P, I, D, Kl, S]

# Function to draw the gamepad
def draw_gamepad(screen, joystick):
    screen.fill(WHITE)

    # Draw the gamepad outline
    pygame.draw.rect(screen, BLACK, (50, 50, 300, 300), 2)
    pygame.draw.rect(screen, BLACK, (400, 50, 300, 300), 2)

    # Draw the analog sticks
    left_stick_x = int(50 + 150 * (joystick.get_axis(0) + 1))
    left_stick_y = int(50 + 150 * (joystick.get_axis(1) + 1))
    pygame.draw.circle(screen, BLACK, (left_stick_x, left_stick_y), 10)

    right_stick_x = int(400 + 150 * (joystick.get_axis(2) + 1))
    right_stick_y = int(50 + 150 * (joystick.get_axis(3) + 1))
    pygame.draw.circle(screen, BLACK, (right_stick_x, right_stick_y), 10)

    # Draw the buttons
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i) == 1:
            pygame.draw.rect(screen, GRAY, (80 + (i % 10) * 60, 400 + (i // 10) * 60, 40, 40))
        else:
            pygame.draw.rect(screen, WHITE, (80 + (i % 10) * 60, 400 + (i // 10) * 60, 40, 40))
        pygame.draw.rect(screen, BLACK, (80 + (i % 10) * 60, 400 + (i // 10) * 60, 40, 40), 2)

    # Update the display
    pygame.display.flip()

# Function to draw the PID menu
def draw_pid_menu(screen, selected_index, val):
    global values
    screen.fill(WHITE)
    # Define font
    font = pygame.font.SysFont(None, 36)
    menu_items = ['P', 'I', 'D', 'Kl', 'S']
    
    for i, item in enumerate(menu_items):
        text_surface = font.render(f"{item}: {values[i]}", True, BLACK)
        screen.blit(text_surface, (50, 50 + i * 50))
        if selected_index == i:
            values[i] += val
            pygame.draw.rect(screen, BLACK, (45, 45 + i * 50, 310, 50), 2)
    
    pygame.display.flip()


def joystick_to_angle_magnitude(joystick):
    left_x = joystick.get_axis(0)
    left_y = joystick.get_axis(1)
    right_x = joystick.get_axis(2)
    right_y = joystick.get_axis(3)

    left_angle = np.arctan2(-left_y, left_x)
    left_magnitude = min(round(np.hypot(left_x, left_y), 2), 1)

    right_angle = np.arctan2(-right_y, right_x)
    right_magnitude = min(round(np.hypot(right_x, right_y), 2), 1)

    left_angle = np.degrees(left_angle)-90
    right_angle = np.degrees(right_angle)-90
    
    
    left_angle = left_angle % 360
    right_angle = right_angle % 360
    
    #left_angle = round((left_angle + 180) % 360 - 180)
    #right_angle = round((right_angle + 180) % 360 - 180)
    
    if left_magnitude < 0.1:
        left_magnitude = 0
        left_angle = 0
    if right_magnitude < 0.1:
        right_magnitude = 0
        right_angle = 0
    
    return (round(left_angle), left_magnitude), (round(right_angle), right_magnitude)

def main():
    pygame.init()
    pygame.joystick.init()

    # Initialize the first connected joystick
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("Initialized joystick:", joystick.get_name())
    else:
        print("No joystick detected.")
        return

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gamepad Viewer")

    gamepad_view = True
    selected_index = 0
    val = 0
    try:
        running = True
        while running:
            val = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == 1539 or event.type == 1538:
                    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
                    hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
                    lr, ud = hats[0]
                    if buttons[5] == 1:
                        gamepad_view = not gamepad_view
                    
                    if lr != 0:
                        val += lr
                    elif ud > 0:
                        selected_index -= 1
                    elif ud < 0:
                        selected_index += 1
                    elif buttons[0] == 1:
                        val -= 10
                    elif buttons[2] == 1:
                        val += 10

                    if selected_index < 0:
                        selected_index = 0
                    if selected_index > 5:
                        selected_index = 5
            
            axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
            #print(type(buttons))
            #buttons.pop(8)
            #buttons.pop(8)
            #buttons.pop(-1)
            hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]

            left, right = joystick_to_angle_magnitude(joystick)

            # Print out the input
            #print("Axes:", axes)
            #print(f"Left: {left[0]} {left[1]}\tRight: {right[0]} {right[1]}")
            #print("Buttons:", buttons)
            #print("Hats:", hats)
            
            

            if buttons[4] == 1:
                command = f"c,{int(left[1]*100)},{int(-axes[2]*100)},{int(left[0])},0,0\r\n"
            else:
                command = f"c,{int(left[1]*50)},{int(-axes[2]*25)},{int(left[0])},0,0\r\n"
            #ESP32_Handler.write(command.encode())
            print(command, end='\t')
            
            if buttons[1] == 1:
                command = f"p,{int(values[0])},{int(values[1])},{int(values[2])}\r\n"
                #ESP32_Handler.write(command.encode())
                time.sleep(0.1)
                command = f"r,{int(values[3])},{int(values[4])}\r\n"
                #ESP32_Handler.write(command.encode())
                time.sleep(0.1)
            
            #print(ESP32_Handler.readline().decode(), end='\t')
            #print()
            
            if gamepad_view:
                draw_gamepad(screen, joystick)
            else:
                draw_pid_menu(screen, selected_index, val)
            #pygame.time.delay(100)  # Delay to reduce CPU load

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
