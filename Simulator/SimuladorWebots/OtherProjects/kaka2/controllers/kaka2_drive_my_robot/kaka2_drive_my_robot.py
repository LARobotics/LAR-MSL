"""kdrive_my_robot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

if __name__ == "__main__":


    # create the Robot instance.
    robot = Robot()

    # get the time step of the current world.
    timestep = 64
    max_speed = 6.28
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  motor = robot.getDevice('motorname')
    #  ds = robot.getDevice('dsname')
    #  ds.enable(timestep)
    
    #Create motor instances
    motor1 = robot.getDevice('motor_1')
    motor2 = robot.getDevice('motor_2')
    motor3 = robot.getDevice('motor_3')
    
    motor1.setPosition(float('inf'))
    motor1.setVelocity(0.0)
    motor2.setPosition(float('inf'))
    motor2.setVelocity(0.0)
    motor3.setPosition(float('inf'))
    motor3.setVelocity(0.0)
    
    
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        motor1V = 0.5 * max_speed
        motor2V = 0 * max_speed
        motor3V = 0.5 * max_speed
        
        motor1.setVelocity(motor1V)
        motor2.setVelocity(motor2V)
        motor3.setVelocity(motor3V)
        
        
    
    # Enter here exit cleanup code.
    