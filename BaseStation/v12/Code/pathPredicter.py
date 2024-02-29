# import consts
import matplotlib.pyplot as plt
import time
import numpy as np

class movementPrediciton:
	def __init__(self, name, len, power = 1):
		self.name = name
		self.X =[0]*len 
		self.Y = [0]*len
		self.angle = [0]*len
		self.power = power
		self.weights = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
		self.weights = self.weights/np.sum(self.weights)
	
	def NextMove(self, x, y):
		self.X.pop(0)
		self.X.append(x)
		self.Y.pop(0)
		self.Y.append(y)

	def NextAngle(self, x):
		self.angle.pop(0)
		self.angle.append(x)

	def getPrediction(self, numberOfNextPoints = 1):
		################# COM ESTAS CONVOLUÇÔES ACHO QUE SO TOU A UTILIZAR OS ULTIMOS 3 PONTOS; A MEDIA DELES
		# self.weights = np.repeat(1.0, len(self.X)) / len(self.X)
		self.x_pred = np.convolve(self.X, self.weights, 'valid')
		# print(self.weights, self.X, self.x_pred)
		self.y_pred = np.convolve(self.Y, self.weights, 'valid')
		self.nextX = self.X[-1]+(self.X[-1]-self.x_pred[-1])
		self.nextY = self.Y[-1]+(self.Y[-1]-self.y_pred[-1])
		self.nextXUI = self.X[-1]+(self.X[-1]-self.x_pred[-1])
		self.nextYUI = self.Y[-1]+(self.Y[-1]-self.y_pred[-1])
		return self.nextX, self.nextY

if __name__ == "__main__":
	a = movementPrediciton("name", 10, 2)
	# tic = time.time()
	# a.NextMove(1, 1)
	# a.NextMove(2, 2)
	# a.NextMove(3, 3)
	# NextMove(4, 4)
	# a.NextMove(5, 5)
	# a.NextMove(6, 6)
	# a.NextMove(7, 7)
	# NextMove(8, 8)
	# a.NextMove(19, 19)
	# NextMove(0, 0)
	# toc = (time.time()-tic)*1000
	# print(toc)
	running = 1
	temp = 0

	for i in range(1, 5):
		tic = time.time()
		temp = 0
		for j in range(10):
			temp += 1
			a.NextMove(0, 0)
			x_pred, y_pred = a.getPrediction(1)
		toc = (time.time()-tic)
		print(toc)

		plt.scatter(a.X, a.Y, label='Original Data')
		plt.scatter(x_pred, y_pred, label='Predictions')
		plt.show(block = False)
		plt.pause(5)