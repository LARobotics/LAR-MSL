from site import abs_paths
import pygame
from pygame.locals import *
import numpy as np
import time
from collections import deque
import serial

ESP32_Handler = serial.Serial()
ESP32_Handler.port = "/dev/ttyUSB0"
ESP32_Handler.baudrate = 115200
#ESP32_Handler.open()

points = deque(maxlen=50)
points_move = deque(maxlen=50)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

P = 1000
I = 500
D = 0
Kl = 900
S = 5
values = [P, I, D, Kl, S]

def draw_gamepad(screen, joystick):

    pygame.draw.rect(screen, BLACK, (50, 50, 300, 300), 2)
    pygame.draw.rect(screen, BLACK, (400, 50, 300, 300), 2)

    left_stick_x = int(50 + 150 * (joystick.get_axis(0) + 1))
    left_stick_y = int(50 + 150 * (joystick.get_axis(1) + 1))
    pygame.draw.circle(screen, BLACK, (left_stick_x, left_stick_y), 10)

    right_stick_x = int(400 + 150 * (joystick.get_axis(2) + 1))
    right_stick_y = int(50 + 150 * (joystick.get_axis(3) + 1))
    pygame.draw.circle(screen, BLACK, (right_stick_x, right_stick_y), 10)

    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i) == 1:
            pygame.draw.rect(screen, GRAY, (80 + (i % 10) * 60, 400 + (i // 10) * 60, 40, 40))
        else:
            pygame.draw.rect(screen, WHITE, (80 + (i % 10) * 60, 400 + (i // 10) * 60, 40, 40))
        pygame.draw.rect(screen, BLACK, (80 + (i % 10) * 60, 400 + (i // 10) * 60, 40, 40), 2)


def draw_pid_menu(screen, selected_index, val):
    global values
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    menu_items = ['P', 'I', 'D', 'Kl', 'S']
    
    for i, item in enumerate(menu_items):
        text_surface = font.render(f"{item}: {values[i]}", True, BLACK)
        screen.blit(text_surface, (50, 50 + i * 50))
        if selected_index == i:
            values[i] += val
            pygame.draw.rect(screen, BLACK, (45, 45 + i * 50, 310, 50), 2)
    


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
    
    return [round(left_angle), left_magnitude], [round(right_angle), right_magnitude]


def draw_vector(screen, center, magnitude, angle_degrees, color=(255, 255, 255), thickness=2):
    angle_radians = np.radians(angle_degrees+90)
    
    end_point = (center[0] + (150*magnitude * np.cos(angle_radians)),
                 center[1] - (150*magnitude * np.sin(angle_radians)))
    pygame.draw.line(screen, color, center, end_point, thickness)


def add_polar_to_cartesian(x_cart, y_cart, theta_polar,  r_polar):
    x_polar = 5*r_polar * np.cos(np.radians(theta_polar+90))
    y_polar = -5*r_polar * np.sin(np.radians(theta_polar+90))
    
    x_new = x_cart + x_polar
    y_new = y_cart + y_polar
    
    return x_new, y_new


aa = [0, 0]
point = [400, 150]
clock = pygame.time.Clock()


def main():
    global point, points, points_move
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
    screen.fill(WHITE)
    pygame.display.set_caption("Gamepad Viewer")

    gamepad_view = True
    selected_index = 0
    val = 0
    try:
        running = True
        while running:
            screen.fill(WHITE)
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
            
            
            # # Example usage
            # polar1 = (1, np.deg2rad(0))  # rho, theta
            # polar2 = (1, np.deg2rad(-90))  # rho, theta
            # print(left[0], end="\t")
            if abs(left[0]+360 - aa[0]) < abs(left[0] - aa[0]):
                left[0] = left[0] + 360
            elif abs(left[0]-360 - aa[0]) < abs(left[0] - aa[0]):
                left[0] = left[0] - 360
            # print(left[0], left[1])
            
            aa[0] += 0.1 * (left[0] - aa[0])
            #aa[1] = 1/max(np.sqrt(abs(left[0] - aa[0])), 1)
            aa[1] = abs(left[1]*np.cos(np.deg2rad(left[0] - aa[0])))
            # aa[1] = min(aa[1], left[1])
            print(left, aa, end = " ! ")
            
            
            
            
            point = add_polar_to_cartesian(point[0], point[1], round(aa[0]), aa[1])
            points_move.append(point)
            print(point)
            # time.sleep(0.1)
            # pygame.draw.line()
            #desired = left
            #output = 

            # Print out the input
            #print("Axes:", axes)
            #print(f"Left: {left[0]} {left[1]}\tRight: {right[0]} {right[1]}")
            #print("Buttons:", buttons)
            #print("Hats:", hats)
            
            

            # if buttons[4] == 1:
            #     command = f"c,{int(left[1]*100)},{int(-axes[2]*100)},{int(left[0])},0,0\r\n"
            # else:
            #     command = f"c,{int(left[1]*50)},{int(-axes[2]*25)},{int(left[0])},0,0\r\n"
            # #ESP32_Handler.write(command.encode())
            # # print(command, end='\t')
            
            # if buttons[1] == 1:
            #     command = f"p,{int(values[0])},{int(values[1])},{int(values[2])}\r\n"
            #     #ESP32_Handler.write(command.encode())
            #     time.sleep(0.1)
            #     command = f"r,{int(values[3])},{int(values[4])}\r\n"
            #     #ESP32_Handler.write(command.encode())
            #     time.sleep(0.1)
            
            # #print(ESP32_Handler.readline().decode(), end='\t')
            # #print()
            
            if gamepad_view:
                draw_gamepad(screen, joystick)
                draw_vector(screen, (200, 200), left[1], left[0], (255,0,0))
                
                points.append(list(aa))
                for i,a in enumerate(points):
                    draw_vector(screen, (200, 200), a[1], a[0], (5*i,255-5*i,0))
                for i in points_move:
                    pygame.draw.circle(screen, (0,0,255), (i[0], i[1]), 2)
                    
            else:
                draw_pid_menu(screen, selected_index, val)
            pygame.display.flip()

            clock.tick(30)
            #pygame.time.delay(1)  # Delay to reduce CPU load/

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
