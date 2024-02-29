"""supervisor_controller controller."""

from controller import Supervisor, Keyboard

TIME_STEP = 32

robot = Supervisor()
keyboard = Keyboard()

keyboard.enable(TIME_STEP)

# get the time step of the current world.
#timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
bb8_node = robot.getFromDef('BB-8')
translation_field = bb8_node.getField('translation')

root_node = robot.getRoot()
children_field = root_node.getField('children')

children_field.importMFNodeFromString(-1, 'DEF BALL Ball { translation 0 1 1 }')
ball_node = robot.getFromDef('BALL')
color_field = ball_node.getField('color')

i = 0
key = keyboard.getKey()

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1:
    if i == 0:
        new_value = [0, 0, 0]
        translation_field.setSFVec3f(new_value)
        
    '''
    if i == 10:
        #bb8_node.remove()
       pass
    if i == 20:
        #children_field.importMFNodeFromString(-1, 'Nao { translation 2.5 0 0.334}')
        pass
    '''

    key = keyboard.getKey()
    if key == keyboard.UP:
        new_value[0] += 0.01
        translation_field.setSFVec3f(new_value)
        print('Up key is pressed')

    if  key == keyboard.DOWN:
        new_value[0] -= 0.01
        translation_field.setSFVec3f(new_value)
        print('Up key is pressed')
        
            
    position = ball_node.getPosition()
    print('Ball position:', position[0], position[1], position[2])
    
    if position[2] < 0.2:
        red_color = [1, 0, 0]
        color_field.setSFColor(red_color)
    
    i += 1