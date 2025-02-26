import socket
import time
from threading import Thread
import json

comando = ""
running = 1

localIP = "127.0.0.1"
localPort = 12346
bufferSize = 1024
RPIAdress = ("127.0.0.1", 49622)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setblocking(0)
UDPServerSocket.bind((localIP, localPort))


recieve = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
recieve.setblocking(0)
recieve.bind((localIP, 12345))

def readCommands():
    global comando
    global recieve
    global running
    while running:
        try:
            message, adr = recieve.recvfrom(bufferSize)
            comando = message.decode('utf8')
            comando = comando.rstrip('\x00')#strip()
            if len(comando) > 0:
                a = json.loads(comando, cls=json.JSONDecoder, strict = False)
                print(json.dumps(a, indent=2))
        except Exception as e:
            if "10035" not in str(e):
                print(" - ", e)
            running = globals()["running"]

t = Thread(target=readCommands)
t.start()

a = ""
while a != "stop":    
    a = input()
running = 0