from controller import Robot, Motor, Supervisor
from math import pi, sin
import socket

TIME_STEP = 5

supervisor = Supervisor()
#robot = Robot()
#print(robot)
#ball_node = supervisor.getFromDef("Bola")
robot = supervisor.getFromDef("OMNI_WHEELS")
children = robot.getField("children")
a = children.importMFNodeFromString(-1, 'DEF SOLID1 Solid {}')
print(a)
#trans_field = ball_node.getField("translation")

#roda = robot.getField("SOLID1")
#motor1 = roda.getField("WHEEL1")
#print(ball_node)
#print(robot)
#print(trans_field)
#print(motor1)
#motors = [robot.getDevice("wheel1"), robot.getDevice("wheel2"), robot.getDevice("wheel3")]
#print(motors)
#for motor in motors:
#    motor.setPosition(float('inf'))
#    motor.setVelocity(0.0)

while supervisor.step(TIME_STEP) != -1:
    pass
    #motors[0].setVelocity(0.0)
    #motors[1].setVelocity(-8.0)
    #motors[2].setVelocity(8.0)
    #values = trans_field.getSFVec3f()
    #print(values)

