from consts import *
import pygame

FUNC = 0
SWITCH = 1

class Button():
    def __init__(self, screen, x, y, size_x, size_y, typ, func, args, flag = [], text = "", color = [-1, -1, -1]):
        self.screen = screen
        self.x = x*RESOLUTION[0]
        self.y = y*RESOLUTION[1]
        self.size_x = size_x*RESOLUTION[0]
        self.size_y = size_y*RESOLUTION[1]
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        self.type = typ
        if self.type == FUNC:
            self.func = func
            self.args = args
            self.flag = flag
            self.color_ON_func = COLORS["activated"]
        elif self.type == SWITCH:
            self.flag = func
            self.color_ON_switch = COLORS["selected"]
        else:
            print("TYPE OF BUTTON DOESNT EXIST")
        
        if color != [-1, -1, -1]:
            self.color = list(color)    
            self.color_on_hover = list(color)
            for a in range(len(self.color_on_hover)):
                self.color_on_hover[a] += 100
                if(self.color_on_hover[a] > 255): self.color_on_hover[a] = 255
                if(self.color_on_hover[a] < 0): self.color_on_hover[a] = 0
        else:
            self.color = COLORS["button"]
            self.color_on_hover = COLORS["hover"]

        self.textString = text
        if self.textString != "":
            smallfont = pygame.font.SysFont('comicsansms', int((self.size_x*self.size_y)/500))
            if(self.color[0]+self.color[1]+self.color[2] > 128*3):
                self.text = smallfont.render(self.textString , True , (0, 0, 0))
            else:
                self.text = smallfont.render(self.textString , True , (255, 255, 255))
        
    def handle_hover(self, mouse):
        if self.rect.collidepoint((mouse[0], mouse[1])):
            if self.flag == True:
                if self.type == SWITCH:
                    pygame.draw.rect(self.screen,self.color_ON_switch,self.rect, border_radius = 5)
                if self.type == FUNC:
                    pygame.draw.rect(self.screen,self.color_ON_func,self.rect, border_radius = 5)
            else:
                pygame.draw.rect(self.screen,self.color_on_hover,self.rect, border_radius = 5)
            if mouse[2] == 1:
                if self.type == FUNC:
                    self.func(self.args)
                if self.type == SWITCH:
                    self.flag = not self.flag
        else:
            if self.flag == True:
                if self.type == FUNC:
                    pygame.draw.rect(self.screen,self.color_ON_func,self.rect, border_radius = 5)
                elif self.type == SWITCH:
                    pygame.draw.rect(self.screen,self.color_ON_switch,self.rect, border_radius = 5)
            else:
                pygame.draw.rect(self.screen,self.color,self.rect, border_radius = 5)
        self.screen.blit(self.text, (self.x+(self.size_x/2)-int(self.text.get_width()/2), self.y+(self.size_y/2)-int(self.text.get_height()/2)))
    
    def getFlag(self):
        return self.flag
    def setFlag(self, flag):
        self.flag = flag



class DropDown():
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        if main != "":
            self.main = main
            self.active_option = -1
            self.option = -1
        else:
            self.main = options[0]
            self.active_option = 0
            self.option = 0
        self.options = options
        self.draw_menu = False
        self.menu_active = False

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0, border_radius=2*FACTOR)
        msg = self.font.render(self.main, 1, (255, 255, 255))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0, border_radius=2*FACTOR)
                msg = self.font.render(text, 1, (255, 255, 255))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, mouse):
        self.menu_active = self.rect.collidepoint((mouse[0], mouse[1]))
        
        self.active_option = self.option
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint((mouse[0], mouse[1])):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if mouse[2] == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                self.option = self.active_option
                return self.active_option
        return -1
