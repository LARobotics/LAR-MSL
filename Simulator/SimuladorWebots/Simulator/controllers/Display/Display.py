"""Display controller."""
from controller import Robot, Display, Supervisor
import socket
import numpy as np

supervisor = Supervisor()

dispSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dispSocket.bind(("localhost", 22200))
dispSocket.setblocking(0)
#dispSocket.settimeout(0.001)

display = Display("display")

fieldImage = display.imageLoad("./../../../OtherFiles/Campo3.png")

def background(args):
	display.imagePaste(fieldImage, 0, 0, True)
def setFont(args):
	display.setFont(args[0], args[1], args[2])
def drawPixel(args):
	args = [int(a) for a in args]
	display.drawPixel(args[0], args[1])
def drawLine(args):
	args = [int(a) for a in args]
	display.drawLine(args[0], args[1], args[2], args[3])
def drawRectangle(args):
	args = [int(a) for a in args]
	display.drawRectangle(args[0], args[1], args[2], args[3])
def drawOval(args):
	args = [int(a) for a in args]
	display.drawOval(args[0], args[1], args[2], args[3])
def drawPolygon(args):
	args = [int(a) for a in args]
	argsTemp0 = args[0:int(len(args)/2)]
	argsTemp1 = args[int(len(args)/2):int(len(args)-1)]
	display.drawPolygon(argsTemp0, argsTemp1)
	
def drawText(args):
	display.drawText(args[0], int(args[1]), int(args[2]))
def fillRectangle(args):
	args = [int(a) for a in args]
	display.fillRectangle(args[0], args[1], args[2], args[3])
def fillOval(args):
	args = [int(a) for a in args]
	display.fillOval(args[0], args[1], args[2], args[3])
def fillPolygon(args):
	args = [int(a) for a in args]
	argsTemp0 = args[0:int(len(args)/2)]
	argsTemp1 = args[int(len(args)/2):int(len(args)-1)]
	display.fillPolygon(argsTemp0, argsTemp1)


background([0, 0])
backgroundCounter = 0

if 0:
	while 1:#supervisor.step(1) != -1:
		try:
			message = dispSocket.recvfrom(1024)
			mens = message[0].decode('utf8', 'strict').split(";")
			func = mens[0]
			cao = mens[1].replace("\'","").replace("[","").replace("]","").replace(" ","").split(",")
			args = mens[2].replace("\'","").replace("[","").replace("]","").replace(" ","").split(",")
			#print(func, cao, args)
			display.setColor(int(cao[0]))
			display.setAlpha(float(cao[1]))
			display.setOpacity(float(cao[2]))
			if func == "background":
				backgroundCounter += 1
				if backgroundCounter >= 3:
					backgroundCounter = 0
					supervisor.step(0)
			globals()[func](args)
			a = ""
		except Exception as e:
			#print(e)
			pass
	
