import socket
import time
from threading import Thread

comando = ""
running = 1

localIP = "192.168.31.249"
localPort = 20000
bufferSize = 1024
RPIAdress = ("192.168.31.147", 20001)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setblocking(0)
UDPServerSocket.bind((localIP, localPort))


recieve = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
recieve.setblocking(0)
recieve.bind((localIP, 20011))

def readCommands():
    global comando
    global recieve
    global running
    while running:
        try:
            message, adr = recieve.recvfrom(bufferSize)
            comando = message.decode('utf8', 'strict')
            print(comando)
        except Exception as e:
            running = globals()["running"]


t = Thread(target=readCommands)
t.start()

a = ""
while a != "stop":    
    a = input()
    if a == "a":
        UDPServerSocket.sendto(str.encode("[7, 2, 3, 4, 5, 0, 0, 0]"), RPIAdress)
    elif a != "stop":
        UDPServerSocket.sendto(str.encode(a), RPIAdress)
running = 0