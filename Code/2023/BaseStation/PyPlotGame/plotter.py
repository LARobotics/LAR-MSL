import sys, pygame
import time
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np

width = 500
height = 500
screen_color = (0, 0, 0)
line_color = (255, 255, 255)
tt = 0
tt2 = 0
screen=pygame.display.set_mode((width,height))
# screen.fill(screen_color)
# pygame.display.flip()
# pygame.draw.line(screen,line_color, (60, 80), (130, 100))

class plotter:
	def __init__(self, pos_x, pos_y, size_x, size_y, x_axis, y_axis, Name = "", x_axis_name = "", y_axis_name = "", colorB = (-1, -1, -1), colorP = (255, 255, 255)):
		self.pos_x = pos_x*width
		self.pos_y = pos_y*height
		self.size_x = size_x*width
		self.size_y = size_y*height
	
	def plot(self, *args, a = ""):
		global tt, tt2
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y), 1)
		if len(args) > 1:
			X = args[0]
			Y = args[1]
		else:
			Y = args[0]
			X = list(range(0, len(Y)))
		
		points = []
		tt = time.time()
		for i in range(len(Y)):
			points.append([self.pos_x+(i)*(self.size_x/(len(Y)*1.1)) + (0.05*self.size_x), self.pos_y+self.size_y-((Y[i]*self.size_y)/((max(Y)-min(Y))*1.1)) + (0.5*(min(Y)*self.size_y)/max(Y))])#-(Y[i]*(max(Y))/min(Y)*self.size_y)])
		tt2 = time.time()
		for p in points:
			# screen.fill((255, 255, 255), (p, (3, 3)))
			pygame.draw.lines(screen, (255, 0, 0), False, points)	
		# print(len(points), len(Y))

		# plt.plot(X, Y)
		# plt.show()

x = np.arange(0,4*np.pi,4*np.pi/100)   # start,stop,step
y = 7*np.sin(x)

grafico = plotter(0.1, 0.1, 0.8, 0.8, 1, 1)
while True:
	# grafico.plot([1, 2, 3, 4, 5, 6, 7, 8, 9])
	# grafico.plot([1, 2, 3, 4, 5, 6, 7], [23, -45, 56, -67, 78, -89, 89])
	XX = [10, 100, 1000, 10000]
	for i in XX:
		x = np.arange(0,4*np.pi,4*np.pi/i)   # start,stop,step
		y = 7*np.sin(x)
		t = time.time()
		ttt = 0
		for j in range(10):
			screen.fill(screen_color)
			grafico.plot(x, y)
			# print(str(int((time.time()-t)*1000)), "ms", end=" | ")
			ti = time.time()
			pygame.display.update()
			print(str(int((time.time()-ti)*1000)), end="|")
			ttt += tt2-tt
		print(int(ttt)/10, str(int((time.time()-t)*100)), "ms")