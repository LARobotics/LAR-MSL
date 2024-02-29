# import sys, pygame
# import time
# from pygame.locals import *
# import matplotlib.pyplot as plt
# import numpy as np

# width = 500
# height = 500
# screen_color = (0, 0, 0)
# line_color = (255, 255, 255)
# tt = 0
# tt2 = 0
# screen=pygame.display.set_mode((width,height))

# class Slider:
#     def __init__(self, x, y, w, h):
#         self.circle_x = x
#         self.volume = 0
#         self.sliderRect = pygame.Rect(x, y, w, h)

#     def draw(self, screen):
#         pygame.draw.rect(screen, (255, 255, 255), self.sliderRect)
#         pygame.draw.circle(screen, (255, 240, 255), (self.circle_x, (self.sliderRect.h / 2 + self.sliderRect.y)), self.sliderRect.h * 1.5)

#     def get_volume(self):
#         return self.volume

#     def set_volume(self, num):
#         self.volume = num

#     def update_volume(self, x):
#         if x < self.sliderRect.x:
#             self.volume = 0
#         elif x > self.sliderRect.x + self.sliderRect.w:
#             self.volume = 100
#         else:
#             self.volume = int((x - self.sliderRect.x) / float(self.sliderRect.w) * 100)

#     def on_slider(self, x, y):
#         if self.on_slider_hold(x, y) or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h:
#             return True
#         else:
#             return False

#     def on_slider_hold(self, x, y):
#         if ((x - self.circle_x) * (x - self.circle_x) + (y - (self.sliderRect.y + self.sliderRect.h / 2)) * (y - (self.sliderRect.y + self.sliderRect.h / 2)))\
#                <= (self.sliderRect.h * 1.5) * (self.sliderRect.h * 1.5):
#             return True
#         else:
#             return False

#     def handle_event(self, screen, x):
#         if x < self.sliderRect.x:
#             self.circle_x = self.sliderRect.x
#         elif x > self.sliderRect.x + self.sliderRect.w:
#             self.circle_x = self.sliderRect.x + self.sliderRect.w
#         else:
#             self.circle_x = x
#         self.draw(screen)
#         self.update_volume(x)
#         print(self.volume)

# sli = Slider(10, 10, 100, 10)
# while True:
# 	sli.draw(screen)
# 	pygame.display.update()
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray
from pygame_widgets.combobox import ComboBox
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
# from pygame_widgets.animations import Resize
# pygame_widgets.animations.Resize

pygame.init()
win = pygame.display.set_mode((1000, 600))

slider = Slider(win, 100, 100, 800, 20, min=0, max=99, step=9)
output = TextBox(win, 475, 200, 50, 50, fontSize=30)
output.disable()
toggle = Toggle(win, 100, 120, 40, 20)

button = Button(win, 200, 300, 300, 150)

# animation = pygame_widgets.Resize(button, 3, 200, 200)
# animation.start()

# output.disable()  # Act as label instead of textbox

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    output.setText(slider.getValue())

    pygame_widgets.update(events)
    pygame.display.update()