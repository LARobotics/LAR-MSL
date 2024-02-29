import socket

class communication:
    def __init__(self, ROBOTID, Bport):
        Aport = 0
        self.SocketAdress2send = ("localhost", 20000+Bport*1000+Aport*100+ROBOTID*10+0)
        self.sendSocketAdress = ("localhost", 20000+Bport*1000+Aport*100+ROBOTID*10+1)
        self.recvSocketAdress = ("localhost", 20000+Aport*1000+Bport*100+ROBOTID*10+0)

        self.recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recvSocket.bind(self.recvSocketAdress)
        #self.recvSocket.settimeout(0.001)
        self.recvSocket.setblocking(0)

        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendSocket.bind(self.sendSocketAdress)
        #self.sendSocket.settimeout(0.001)
        self.sendSocket.setblocking(0)
    
    def getMessage(self, info):
        try:
            message = self.recvSocket.recvfrom(1024)
            mens = message[0].decode('utf8', 'strict').replace("[", "").replace("]", "").replace(" ", "").split(",")
            mens = [float(numeric_string) for numeric_string in mens]
            self.sendSocket.sendto(info.encode(), self.SocketAdress2send)
            return mens
        except:
            return [-1, -1, -1, -1, -1, -1, -1, -1]
