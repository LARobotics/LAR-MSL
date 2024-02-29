import consts
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
import numpy as np
import time

x = 240
y = 160

class pMapRule():
	def __init__(self, name, on, ID):
		self.name = name
		self.on = on
		self.enabled = True
		self.ID = ID
		self.X = int(consts.FIELD_SIZE["wall"][0] + consts.FACTOR)
		self.Y = int(consts.YOFFSET+consts.FACTOR+(ID)*8*consts.FACTOR)
		self.width = int(consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0]-2*consts.FACTOR)
		self.height = int(8*consts.FACTOR-consts.FACTOR*2)
		self.button = Button(consts.SCREEN, self.X, self.Y, self.width, self.height, radius = 10, inactiveColour=consts.COLORS["button"])
		self.button.disable()
		self.text = TextBox(consts.SCREEN, int(self.X+0.025*self.width), int(self.Y+(2/4)*self.height), int(0.2*self.width), int(self.height*0.5), colour=consts.COLORS["button"], borderColour = consts.COLORS["button"], textColour = (255, 255, 255))
		self.text.disable()
		self.text.setText(name)
		self.toggle = Toggle(consts.SCREEN, int(self.X+0.325*self.width), int(self.Y+(1/4)*self.height), int(0.075*self.width), int(self.height*0.5), startOn = on)
		self.slider = Slider(consts.SCREEN, int(self.X+0.425*self.width), int(self.Y+(1/4)*self.height), int(0.55*self.width), int(self.height*0.5), min = 0, max = 1, step = 0.01, initial = 0)
		self.slider.setValue(1)
		self.disableUI()

	def show(self):
		pass

	def enableUI(self):
		if self.enabled == False:
			self.enabled = True
			self.button._hidden = False
			self.button._x = self.X
			self.text._hidden = False
			self.text._x = int(self.X+0.025*self.width)
			self.toggle._hidden = False
			self.toggle._x = int(self.X+0.325*self.width)
			self.slider._hidden = False
			self.slider._x = int(self.X+0.425*self.width)

	def disableUI(self):
		if self.enabled == True:
			self.enabled = False
			self.button._hidden = True
			self.button._x = -self.width
			self.text._hidden = True
			self.text._x = -self.width
			self.toggle._hidden = True
			self.toggle._x = -self.width
			self.slider._hidden = True
			self.slider._x = -self.width


class pField():
	def __init__(self, name, on, ID, size_X = x, size_Y = y):
		self.field = np.zeros((size_X, size_Y))
		self.field0 = np.zeros((size_X, size_Y))
		self.field1 = np.zeros((x, y))
		self.field2 = np.zeros((x, y, 3))
		self.UI = pMapRule(name, on, ID)
		self.needPadding = False
		if size_X != x or size_Y != y:
			self.needPadding = True

	
	def calculate(self, maps, robot):
		global x, y
		pos = [robot.position[0], robot.position[1]]
		pos[0] = int(pos[0]*10)+int(x/2)
		pos[1] = -int(pos[1]*10)+int(y/2)

		self.field = np.zeros((x, y))
		numberOfMaps = 0
		for m in maps:
			if m.UI.toggle.getValue():
				numberOfMaps += 1
		if numberOfMaps:
			for m in maps:
				if m.needPadding:
					fieldShape = [max(0, int(pos[0]-m.field.shape[0]/2)), max(0, int(x-pos[0]-m.field.shape[0]/2)), max(0, int(pos[1]-m.field.shape[0]/2)), max(0, int(y-pos[1]-m.field.shape[1]/2))]
					m.field1 = np.pad(m.field, ((fieldShape[0], fieldShape[1]), (fieldShape[2], fieldShape[3])), 'constant', constant_values=(0))
					if pos[0] < m.field.shape[0]/2:
						m.field1 = m.field1[m.field1.shape[0]-x:, :]
					if pos[0] > x-m.field.shape[0]/2:
						m.field1 = m.field1[:x, :]
					if pos[1] < m.field.shape[1]/2:
						m.field1 = m.field1[:, m.field1.shape[1]-y:]
					if pos[1] > y-m.field.shape[1]/2:
						m.field1 = m.field1[:, :y]
					self.field += m.UI.toggle.getValue()*m.field1*m.UI.slider.getValue()#*(1/numberOfMaps)
				else:
					self.field += m.UI.toggle.getValue()*m.field*m.UI.slider.getValue()#*(1/numberOfMaps)
		self.field = np.clip(self.field, 0, 1)

	def get(self):
		self.field *= 255
		self.field2[:,:,0] = self.field
		self.field2[:,:,1] = 0
		self.field2[:,:,2] = (255-self.field)

		return self.field2.astype('uint8')

	def show(self):
		pass

def initFields(robotID):
	global x
	a = [pField(f"Main {robotID}", True, 0)]
	a.append(pField(f"Middle Field", False, len(a)))
	a[-1].field[:,:] = 0
	a[-1].field[int(x/2):,:] = 1
	# a.append(pField(f"Circle Field", True, len(a), 30, 30))
	# a[-1].field = circleMap(30, 30, 1, 2)
	a.append(pField(f"Radius With Ball", True, len(a), 60, 60))
	a[-1].field = circleMap(60, 60, 1, 2)
	a.append(pField(f"Ideal Pass Distance", True, len(a), 120, 120))
	a[-1].field = circleMap(120, 120, 2, 2, 10*consts.bestDistanceToPass, [consts.deviation, consts.deviationPower])
	a.append(pField(f"Ideal Goal Distance", True, len(a), 120, 120))
	a[-1].field = circleMap(120, 120, 2, 2, 10*consts.bestDistanceToGoal, [consts.deviation, consts.deviationPower])
	# a[1].field[int(x/2):,:] = 255
	# for i in range(20):
		# a.append(pField("3Meter", False, i))
		# a[-1].UI.disableUI()
	
	return a

def circleMap(size_X, size_Y, infill = 1, power = 1, radius = -1, args = []):
    center = size_X//2, size_Y//2
    centers = [(center[0],center[1]),(center[0]-1,center[1]),(center[0], center[1]-1),(center[0]-1, center[1]-1)]
    if radius == -1:
        radius = min(size_X, size_Y)//2
    else:
        radius = radius
    matrix = np.zeros((size_X,size_Y))
    matrixFinal = np.zeros((size_X,size_Y))
    x,y = np.meshgrid(np.arange(matrix.shape[1]), np.arange(matrix.shape[0]))

    for center in centers:
        if infill == 1:
            mask = (x-center[0])**2 + (y-center[1])**2 <= radius**2
            distance = np.sqrt((x-center[0])**2 + (y-center[1])**2)
            matrix[mask] = 1-(distance[mask]/radius)**power
        elif infill == 2:
            mask = ((x-center[0])**2 + (y-center[1])**2) <= ((min(size_X, size_Y)-1)//2)**2
            distance = np.sqrt((x-center[0])**2 + (y-center[1])**2)
            matrix[mask] = ((1/(args[0]*np.sqrt(2*3.14)))*np.exp(-(distance[mask]-radius)**2/(2*args[0]**2)))
        else:
            mask = (x-center[0])**2 + (y-center[1])**2 <= radius**2
            mask1 = (x-center[0])**2 + (y-center[1])**2 <= (radius-1)**2
            mask = mask^mask1
            matrix[mask] = 1

        matrixFinal += matrix/len(centers)
    if infill == 2:
        matrix -= np.min(matrix)

    matrixFinal *= (1/np.max(matrixFinal))
    print(np.max(matrixFinal), np.min(matrixFinal))
    return matrixFinal