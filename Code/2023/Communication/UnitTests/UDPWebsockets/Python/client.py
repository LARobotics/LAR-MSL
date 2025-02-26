import socket
import time
from threading import Thread
import numpy as np
import serial
import serial.tools.list_ports
import pyfirmata

#------------------- Serial communication --------------------
print('Searching...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports:
    print('Found port '+ port.device)

ser = serial.Serial(port.device)
if ser.isOpen():
    ser.close()

ser = serial.Serial(port.device, 57600, timeout=1)
ser.flushInput()
ser.flushOutput()
print('Connected to ' + ser.name)
com = str(ser.name)
ser.close()
# Pyfirmata
board = pyfirmata.ArduinoMega(com)
# Serial Status Reader
it = pyfirmata.util.Iterator(board) # Serial packet stablization
it.start()
print('Success')

# ----------------------- Servo Values -----------------------
thumb = board.get_pin('d:2:s')
index = board.get_pin('d:3:s')
midf = board.get_pin('d:4:s')
ring = board.get_pin('d:5:s')
pinky = board.get_pin('d:6:s')
wrist = board.get_pin('d:7:s')
elbow = board.get_pin('d:8:s') # Elbow Roll
armrot = board.get_pin('d:9:s') # Elbow Yaw
shoulderrot = board.get_pin('d:10:s') # Shoulder Pitch
handlift = board.get_pin('d:11:s') # Shoulder Roll

servos_arm = [handlift, shoulderrot, armrot, elbow]
servos_hand = [thumb, index, midf, ring, pinky]

open_pos_arm  = np.array([45, 150, 110, 125], dtype = float) # servo values at maximum angles
close_pos_arm = np.array([16,  40,  80,  55], dtype = float) # servo values at minimum angles

open_pos_hand =  [160, 15,   0,  20,  20] 
close_pos_hand = [80, 135, 110, 130, 120]

comando = ""
running = 1

localIP = "192.168.31.249"
localPort = 20001
bufferSize = 1024
PCAdress = ("192.168.31.45", 20000)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setblocking(0)
UDPServerSocket.bind((localIP, localPort))

# Quando não estiver a receber nada
for i in range(len(close_pos_arm)):
	if i == 3:
		servos_arm[i].write(open_pos_arm[i])
	else:
		servos_arm[i].write(close_pos_arm[i])
        
def readCommands():
    global comando
    global UDPServerSocket
    global running
    while running:
        try:
            message, adr = UDPServerSocket.recvfrom(bufferSize)
            comando = message.decode('utf8', 'strict')
            print(comando)
            comando = comando.replace("[", "").replace("]", "").split(",")
            comando = [int(c) for c in comando]
            servos_arm = comando[0:4]
            for i in range(len(1)):#servos_arm)):
                servos_arm[i].write(servo_values[i])
            

# Quando não estiver a receber nada
# for i in range(len(close_pos_arm)):
# 	if i == 3:
# 		servos_arm[i].write(open_pos_arm[i])
# 	else:
# 		servos_arm[i].write(close_pos_arm[i])
            if comando[-1] == 0: 
                print("OPEN HAND")
                #for j in range(len(servos_hand)):
                #    servos_hand[j].write(open_pos_hand[j])
            else:
                print("CLOSE HAND")
                #for j in range(len(servos_hand)):
                #    servos_hand[j].write(close_pos_hand[j])
        except Exception as e:
            running = globals()["running"]


# t = Thread(target=readCommands)
# t.start()

a = ""
while a != "stop":    
        try:
            message, adr = UDPServerSocket.recvfrom(bufferSize)
            comando = message.decode('utf8', 'strict')
            print(comando)
            comando = comando.replace("[", "").replace("]", "").split(",")
            comando = [int(c) for c in comando]
            servos_arm = comando[0:4]
            for i in range(len(1)):#servos_arm)):
                servos_arm[i].write(servo_values[i])
            

# Quando não estiver a receber nada
# for i in range(len(close_pos_arm)):
# 	if i == 3:
# 		servos_arm[i].write(open_pos_arm[i])
# 	else:
# 		servos_arm[i].write(close_pos_arm[i])
            if comando[-1] == 0: 
                print("OPEN HAND")
                #for j in range(len(servos_hand)):
                #    servos_hand[j].write(open_pos_hand[j])
            else:
                print("CLOSE HAND")
                #for j in range(len(servos_hand)):
                #    servos_hand[j].write(close_pos_hand[j])
        except Exception as e:
            running = globals()["running"]
    if a != "stop":
        UDPServerSocket.sendto(str.encode(a), PCAdress)

running = 0