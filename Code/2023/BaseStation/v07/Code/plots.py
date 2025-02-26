import matplotlib
# matplotlib.use('module://pygame_matplotlib.backend_pygame')
matplotlib.use("Agg")
import warnings
warnings.filterwarnings("ignore") #used to supress warnings from matplotlib because we use Agg, non
import matplotlib.pyplot as plt
import pylab
import pygame
# from pygame.locals import *
# import numpy as np
import consts
# import sys, pygame
import time
# from pygame.locals import *
# import matplotlib.pyplot as plt
import numpy as np

# width = 500
# height = 500
# screen_color = (0, 0, 0)
# line_color = (255, 255, 255)
# tt = 0
# tt2 = 0
# screen=pygame.display.set_mode((width,height))

class plot():
	def __init__(self, size_x, size_y, x_axis_min, x_axis_max, y_axis_min, y_axis_max, x_position, y_position, numberOfPoints):
		self.size_x = size_x*consts.RESOLUTION[0]
		self.size_y = size_y*consts.RESOLUTION[1]
		self.x_axis_min = x_axis_min
		self.x_axis_max = x_axis_max 
		self.y_axis_min = y_axis_min 
		self.y_axis_max = y_axis_max 
		self.x_position = x_position*consts.RESOLUTION[0]
		self.y_position = y_position*consts.RESOLUTION[1]
		self.numberOfPoints = numberOfPoints
		self.dpis = 100

		self.x_axis = np.linspace(x_axis_min, y_axis_max, x_axis_max)
		# self.fig = pylab.figure(figsize=[3, 3], dpi=100,)
		self.fig = pylab.figure(figsize=[int(self.size_x/self.dpis), int(self.size_y/self.dpis)], dpi=self.dpis,)
		self.ax = self.fig.gca()
		self.line, = self.ax.plot([x_axis_min, x_axis_max], [y_axis_min, y_axis_max])
		self.ax.set_autoscale_on(True)
		self.ax.set_facecolor("orange")
		self.ax.draw_artist(self.ax.patch)
		self.ax.draw_artist(self.line)
		plt.show(block=False)
		plt.pause(0.0001)
		plt.close()
		self.ax.draw_artist(self.ax.patch) # Draws the white around the 
		self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
		self.reset_bg(x_axis_min, x_axis_max, y_axis_min, y_axis_max, numberOfPoints)

	def reset_bg(self, x_axis_min, x_axis_max, y_axis_min, y_axis_max, numberOfPoints):
		self.numberOfPoints = numberOfPoints
		self.fig = pylab.figure(figsize=[int(self.size_x/self.dpis), int(self.size_y/self.dpis)], dpi=self.dpis,)
		# self.fig.set_facecolor("blue")
		# self.fig.patch.set_alpha(0)
		self.ax = self.fig.gca()
		self.line, = self.ax.plot([x_axis_min, x_axis_max], [y_axis_min, y_axis_max])

		self.ax.set_autoscale_on(True)
		# self.ax.set_facecolor("orange")
		self.ax.draw_artist(self.ax.patch)
		self.ax.draw_artist(self.line)
		plt.show(block=False)
		plt.pause(0.0001)
		plt.close()
		self.ax.draw_artist(self.ax.patch) # Draws the white around the 
		self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
		

	def set_plot(self, y_data):
		if consts.REPRESENT_PLOTS:
			if len(y_data) != self.numberOfPoints:
				self.reset_bg(0, len(y_data), min(y_data)-1, max(y_data)+1, len(y_data))
			self.line, = self.ax.plot(y_data, "b")
			self.ax.draw_artist(self.ax.patch) # Draws the white around the 
			self.ax.draw_artist(self.line)

	def add_plot(self, y_data):
		if consts.REPRESENT_PLOTS:
			self.line, = self.ax.plot(y_data, "b")
			self.ax.draw_artist(self.ax.patch) # Draws the white around the 
			self.ax.draw_artist(self.line) # Draws that data on the graph

	def get_plot(self):
		if consts.REPRESENT_PLOTS:
			renderer = self.fig.canvas.get_renderer() # Gets the image generated frmo the graph
			raw_data = renderer.tostring_rgb() # Converts the image
			size = self.fig.canvas.get_width_height() # Gets image size
			self.surf = pygame.image.fromstring(raw_data, size, "RGB") # Generates the image in pygame format
			return self.surf

	def show_plot(self):
		if consts.REPRESENT_PLOTS:
			self.surf = self.get_plot()	
			# screen.blit(self.surf, (self.x_position, self.y_position))
			consts.SCREEN.blit(self.surf, (self.x_position, self.y_position))

# x = np.arange(0,4*np.pi,4*np.pi/100)   # start,stop,step
# y = 7*np.sin(x)

# # grafico = plot(0.1, 0.1, 0.8, 0.8, 1, 1)
# grafico = plot(0.3, 0.5, 0, 10, -3, 3, 0, 0, 10)
# XX = [10, 100, 1000, 10000]
# for i in XX:
# 	x = np.arange(0,4*np.pi,4*np.pi/i)   # start,stop,step
# 	y = 7*np.sin(x)
# 	t = time.time()
# 	ttt = 0
# 	for j in range(10):
# 		screen.fill(screen_color)
# 		grafico.set_plot(y)
# 		grafico.show_plot()
# 		# print(str(int((time.time()-t)*1000)), "ms", end=" | ")
# 		ti = time.time()
# 		pygame.display.update()
# 		print(str(int((time.time()-ti)*1000)), end="|")
# 		ttt += tt2-tt
# 	print(int(ttt)/10, str(int((time.time()-t)*100)), "ms")