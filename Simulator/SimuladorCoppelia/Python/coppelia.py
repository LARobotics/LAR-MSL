import math
import numpy as np
import time
from zmqRemoteApi import RemoteAPIClient


class Coppelia:
    def __init__(self):
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject('sim')
        self.client.setStepping(False)
        self.stratSimulation()

    def stratSimulation(self):
        self.sim.startSimulation()
    
    def getInfo(self):
        self.ToPython = self.sim.getStringSignal("ToPython")
        if self.ToPython != None:
            self.Ball, Robot1, Robot2, Robot3, Robot4, Robot5, self.BalizaOpo, self.BalizaMine, self.BallHandler = self.ToPython.split(";")
            self.Ball = [float(a) for a in self.Ball.split(",")]
            self.BalizaOpo = [float(a) for a in self.BalizaOpo.split(",")]
            self.BalizaMine = [float(a) for a in self.BalizaMine.split(",")]
            Robot1 = [float(a) for a in Robot1.split(",")]
            Robot2 = [float(a) for a in Robot2.split(",")]
            Robot3 = [float(a) for a in Robot3.split(",")]
            Robot4 = [float(a) for a in Robot4.split(",")]
            Robot5 = [float(a) for a in Robot5.split(",")]
            self.Robots = [Robot1, Robot2, Robot3, Robot4, Robot5]
            return self.Ball, self.Robots, self.BalizaMine, self.BalizaOpo, self.BallHandler
        return -1, [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], -1, -1, -1
    
    def sendInfo(self, Trama):
        self.sim.setStringSignal("FrPython", Trama)

