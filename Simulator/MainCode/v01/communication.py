import math
import numpy as np
import time
import socket
import asyncio
from Robot import *


class Communication:
    def __init__(self, myIP, B):
        self.Robots = []
        for a in range(5):
            self.Robots.append(Robot(a+1, myIP, "localhost", 0, B))

        for robot in self.Robots:
            print(robot)
        #self.AdressSocket2Robots = (self.ip, self.Port)
        #self.socket2Robots = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        #self.socket2Robots.bind(self.AdressSocket2Robots)
        #self.socket2Robots.settimeout(0.001)

        self.i = 0

    