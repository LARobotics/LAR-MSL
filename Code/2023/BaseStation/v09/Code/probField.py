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
import fileHandling
import time
import cv2

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
		self.highestValue = 0

	
	def calculate(self, maps, robot, Robots, solution):
		global x, y
		pos = [robot.position[0], robot.position[1]]
		pos[0] = int(pos[0]*10)+int(x/2)
		pos[1] = -int(pos[1]*10)+int(y/2)
		if robot.robotID == 1:
			consts.REPRESENT_EVERY_MAX_PIXEL_ON_HEAT_MAP = self.UI.toggle.getValue()

		self.field = np.zeros((x, y))
		numberOfMaps = 0

		for m in maps:
			if m.UI.toggle.getValue():
				if m.needPadding:
					if len(solution) > 0:
						if "Pass Distance" in m.UI.name:# or "Goal Distance" in m.UI.name:# and robot.robotID != solution[0]:
							tempPassId = np.where(solution==robot.robotID)
							if len(tempPassId[0]) > 0:
								nextPassId = solution[tempPassId[0][0] - 1]-1
								if nextPassId < 5 and nextPassId >= 0:
									pos = [Robots[nextPassId].position[0], Robots[nextPassId].position[1]]
								else:
									pos = [11, 0]
								pos[0] = int(pos[0]*10)+int(x/2)
								pos[1] = -int(pos[1]*10)+int(y/2)
							else:
								continue
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
					self.field += m.field1*m.UI.slider.getValue()
				else:
					if "PC" in m.UI.name:
						self.field += m.field1*m.UI.slider.getValue()
					else:
						self.field += m.field*m.UI.slider.getValue()

		self.field = np.clip(self.field, -1, 1)
		self.highestValue = np.amax(self.field)
		if self.highestValue > 0 and consts.REPRESENT_MAX_VALUE_ON_HEAT_MAP:
			self.mask = np.array(np.where(self.field >= self.highestValue, 1, 0), np.uint8)
			contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			self.centers = []
			for contour in contours:
				moments = cv2.moments(contour, binaryImage = True)
				if moments['m00'] != 0:
					cx = int(moments['m01'] / moments['m00'])
					cy = int(moments['m10'] / moments['m00'])
				else:
					cx, cy = 0, 0
				self.centers.append((cx, cy))
			# print(self.centers)
			if consts.REPRESENT_EVERY_MAX_PIXEL_ON_HEAT_MAP:
				self.temp = np.where(self.field >= self.highestValue)
				self.maxValues = np.array([[self.temp[0][i], self.temp[1][i]] for i in range(len(self.temp[0]))])
				self.meanValue = [int(np.mean(self.maxValues[:, 0])), int(np.mean(self.maxValues[:, 1]))]

	def calculateFriends(self, points, m):
		self.Opofield = np.zeros((x, y))
		pos = [0, 0]
		for i, position in enumerate(points):
			pos[0] = int(position[0]*10)+int(x/2)
			pos[1] = -int(position[1]*10)+int(y/2)
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
			self.Opofield += m.field1

		return self.Opofield

	def calculateOpponents(self, ball, points, m):
		self.Opofield = np.zeros((x, y))
		ball1 = [0, 0]
		pos = [0, 0]
		ball1[0] = int(ball[0]*10)+int(x/2)
		ball1[1] = -int(ball[1]*10)+int(y/2)
		
		for i, position in enumerate(points):
			pos[0] = int(position[0]*10)+int(x/2)
			pos[1] = -int(position[1]*10)+int(y/2)
			angle = round(np.degrees(np.arctan2((ball1[1]-pos[1]), (ball1[0]-pos[0])) - np.radians(90)))
			
			fieldShape = [max(0, int(pos[0]-m.field.shape[0]/2)), max(0, int(x-pos[0]-m.field.shape[0]/2)), max(0, int(pos[1]-m.field.shape[0]/2)), max(0, int(y-pos[1]-m.field.shape[1]/2))]
			m.field1 = np.pad(m.opponentFields[angle], ((fieldShape[0], fieldShape[1]), (fieldShape[2], fieldShape[3])), 'constant', constant_values=(0))
			if pos[0] < m.field.shape[0]/2:
				m.field1 = m.field1[m.field1.shape[0]-x:, :]
			if pos[0] > x-m.field.shape[0]/2:
				m.field1 = m.field1[:x, :]
			if pos[1] < m.field.shape[1]/2:
				m.field1 = m.field1[:, m.field1.shape[1]-y:]
			if pos[1] > y-m.field.shape[1]/2:
				m.field1 = m.field1[:, :y]
			self.Opofield += m.field1

		return self.Opofield

	def get(self, robotID):
		self.field *= 127
		self.field += 128
		self.field2[:,:,0] = self.field
		self.field2[:,:,1] = 0
		self.field2[:,:,2] = 255-self.field
		if self.highestValue > 0 and consts.REPRESENT_MAX_VALUE_ON_HEAT_MAP:
			if consts.REPRESENT_EVERY_MAX_PIXEL_ON_HEAT_MAP:
				self.field2[self.maxValues[:,0], self.maxValues[:,1]] = [0, 128, 0]
			for center in self.centers:
				self.field2[center[0]-1:center[0]+2, center[1]] = [0, 255, 0]
				self.field2[center[0], center[1]-1:center[1]+2] = [0, 255, 0]
			# for i in consts.ZonesPoints:
			self.field2[consts.ZonesPoints[robotID][0]-5:consts.ZonesPoints[robotID][0]+5, consts.ZonesPoints[robotID][1]] = [128, 255, 128]
			self.field2[consts.ZonesPoints[robotID][0], consts.ZonesPoints[robotID][1]-5:consts.ZonesPoints[robotID][1]+5] = [128, 255, 128]
			# self.field2[:, consts.ZonesPoints[robotID][1]] = [128, 255, 128]

		return self.field2.astype('uint8')

	def show(self):
		pass

def initFields(robotID):
	global x

	dic = {}
	try:
		dic = fileHandling.load4File("./configs/robot" + str(robotID) + "/probField.txt")
		print(dic)
	except:
		pass

	a = [pField(f"Main {robotID}", False, 0)]
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	a.append(pField(f"Middle Field", False, len(a)))
	for i in range(x):
		a[-1].field[i,:] = i/x
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()
	
	a.append(pField(f"Other Middle Field", False, len(a)))
	for i in range(y):
		a[-1].field[:,i] = (y/2-abs(i-y/2))/(y/2)
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	if robotID == 1:
		consts.zonesDefault = makeZones(len(a))
	consts.zonesFields = []
	for i in consts.zonesDefault:
		consts.zonesFields.append(i.field)
	a.append(consts.zonesDefault[robotID-1])
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	a.append(pField(f"Circle Field", False, len(a), 60, 60))
	a[-1].field = circleMap(60, 60, 0, 2)
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	a.append(pField(f"Radius With Ball", False, len(a), 60, 60))
	a[-1].field = circleMap(60, 60, 1, 2)
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	a.append(pField(f"Ideal Pass Distance", False, len(a), 120, 120))
	a[-1].field = circleMap(120, 120, 2, 2, 10*consts.bestDistanceToPass, [consts.deviation, consts.deviationPower])
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	a.append(pField(f"Ideal Goal Distance", False, len(a)))
	a[-1].field = matrixPad(circleMap(140, 140, 2, 2, 10*consts.bestDistanceToGoal, [consts.deviation, consts.deviationPower]), [11, 0])
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	sizeInf = 90
	if robotID == 1:
		consts.opponentsFields = [circleMap(sizeInf, sizeInf, 3, 1, args=[i]) for i in range(360)]
	a.append(pField(f"PC Opponents", False, len(a)))
	a[-1].field = circleMap(sizeInf, sizeInf, 3, 1, args=[0])
	a[-1].opponentFields = consts.opponentsFields# [circleMap(sizeInf, sizeInf, 3, 1, args=[i]) for i in range(360)]
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()

	sizeInf = 60
	a.append(pField(f"PC Teammates", False, len(a)))
	a[-1].field = circleMap(sizeInf, sizeInf, 1, 2)
	if a[-1].UI.name in dic:
		a[-1].UI.slider.setValue(dic[a[-1].UI.name]["slider"])
		if dic[a[-1].UI.name]["on"]:
			a[-1].UI.toggle.toggle()
	
	return a


def makeZones(lenA):
	a = []
	a.append(pField(f"Zone", False, lenA))
	for i in range(y):
		a[-1].field[:,i] += (y/2-abs(i-y/2))/(y/2)
	for i in range(x):
		a[-1].field[i,:] += (x/6-abs(i-4*x/6))/(x/3)
	a[-1].field = np.clip(a[-1].field, 0, 1)

	# a.append(pField(f"Zone", False, lenA))
	# for i in range(0, y):
	# 	a[-1].field[:,i] += (y/3-abs(i-2*y/6))/(y/12)
	# a[-1].field = np.clip(a[-1].field, 0, 1)

	a.append(pField(f"Zone", False, lenA))
	for i in range(0, y):
		a[-1].field[:,i] += (y/3-abs(i-2*y/3))/(y/12)
	a[-1].field = np.clip(a[-1].field, 0, 1)

	a.append(pField(f"Zone", False, lenA))
	for i in range(0, y):
		a[-1].field[:,i] += (y/3-abs(i-2*y/6))/(y/12)
	a[-1].field = np.clip(a[-1].field, 0, 1)

	a.append(pField(f"Zone", False, lenA))
	for i in range(y):
		a[-1].field[:,i] += (y/2-abs(i-y/2))/(y/2)
	for i in range(x):
		a[-1].field[i,:] += (x/4-abs(i-x/4))/(x/6)
	a[-1].field = np.clip(a[-1].field, 0, 1)

	a.append(pField(f"Zone", False, lenA))
	for i in range(int(y/2)-int(y/5), int(y/2)+int(y/5)):
		a[-1].field[int(x/24):int(x/7),i] += (y/2-abs(i-y/2))/(y/2)
	a[-1].field = np.clip(a[-1].field, 0, 1)

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
        elif infill == 3:
            X, Y = np.meshgrid(np.linspace(-1, 1, size_X), np.linspace(-1, 1, size_Y))
            angle = np.mod(np.radians(args[0]) + np.pi, 2 * np.pi) - np.pi
            theta = np.arctan2(Y, X)
            distance = np.sqrt((x-center[0])**2 + (y-center[1])**2)
            rotated_theta = theta + angle
            # matrix = np.cos(rotated_theta)#(np.exp(- radius**2 / (2 * 1**2)) * np.cos(rotated_theta*3))
            matrix = abs(distance-radius)**power * np.cos(rotated_theta)#(np.exp(- radius**2 / (2 * 1**2)) * np.cos(rotated_theta*3))
            # matrix = abs(distance-radius) * (np.exp(- radius**2 / (2 * 1**2)) * np.cos(rotated_theta*3) - np.exp(- radius**2 / (2 * 1**2)) * 4 * np.cos(rotated_theta+np.pi))
            mask = ((x-center[0])**2 + (y-center[1])**2) > ((min(size_X, size_Y)-1)//2)**2
            matrix[mask] = 0
        elif infill == -1:
            matrix[:, :] = 1
            mask = (x-center[0])**2 + (y-center[1])**2 <= radius**2
            distance = np.sqrt((x-center[0])**2 + (y-center[1])**2)
            matrix[mask] = (distance[mask]/radius)**power
        else:
            mask = (x-center[0])**2 + (y-center[1])**2 <= radius**2
            mask1 = (x-center[0])**2 + (y-center[1])**2 <= (radius-1)**2
            mask = mask^mask1
            matrix[mask] = 1

        matrixFinal += matrix/len(centers)
    if infill == 2:
        matrixFinal -= np.min(matrixFinal)
    if infill == -1:
        matrixFinal -= np.max(matrixFinal)
    else:
    	matrixFinal *= (1/np.max(matrixFinal))
    return matrixFinal

def matrixPad(field, pos):
	global x, y
	pos[0] = int(pos[0]*10)+int(x/2)
	pos[1] = -int(pos[1]*10)+int(y/2)
	fieldShape = [max(0, int(pos[0]-field.shape[0]/2)), max(0, int(x-pos[0]-field.shape[0]/2)), max(0, int(pos[1]-field.shape[0]/2)), max(0, int(y-pos[1]-field.shape[1]/2))]
	field1 = np.pad(field, ((fieldShape[0], fieldShape[1]), (fieldShape[2], fieldShape[3])), 'constant', constant_values=(0))
	if pos[0] < field.shape[0]/2:
		field1 = field1[field1.shape[0]-x:, :]
	if pos[0] > x-field.shape[0]/2:
		field1 = field1[:x, :]
	if pos[1] < field.shape[1]/2:
		field1 = field1[:, field1.shape[1]-y:]
	if pos[1] > y-field.shape[1]/2:
		field1 = field1[:, :y]
	return field1