import numpy

# Physics
g = 9800 # gravity acceleration 9.8 m/s^2
# Ball
ball_radius = 115   # 11.5 centimeters
y0 = ball_radius
#x0 = -2000  # PARAM # Ball Distance
# Goal
Y_G = 1000  # 1 meter
X_G = 2000 # 2 meters
# Goal Keeper
Y_GK = 800  # 80 centimeters
r_GK = 250  # 25 centimeters

# Kicker Properties
kickAngle_deg = 30 # PARAM # Vertical Degrees 
kickAngle = kickAngle_deg * numpy.pi/180
 

# Compute Goal Keeper Position to block the kicker for a parabolic shot 
#considering the best possible shot from the known ball position

#INPUT: Ball Polar Position Relative to the Goal Center-Line. Angle: +/- 180 Degrees, Distance: milimiters.
def skill_block(ballAngle = 0, ballDist = 2000):
    '''
        Compute Goal Keeper Position to block the kicker for a parabolic shot 
        #considering the best possible shot from the known ball position
        INPUT: Ball Polar Position Relative to the Goal Center-Line. Angle: +/- 180 Degrees, Distance: milimiters.
    '''
    ballAngle = ballAngle * numpy.pi/180 # Degrees to Radians
    x0 = -ballDist
#    print("Ball Angle:",ballAngle,"\tBall Dist:",ballDist)
    #if math.abs(ballAngle) > math.pi:
    ##    print("⛔ Block Error: Ball Angle → Ball is beyond End Line")
    # ---- Y ---- #
    # Compute Ideal Inicial Ball velocity, knowing the kick angle and goal height
    aux = ((g/2)*numpy.power(X_G-x0,2))/(y0+numpy.tan(kickAngle)*(X_G-x0)-Y_G)
    if aux < 0: 
        print("Math Error: Negative value in sqrt()")
    v0 = numpy.sqrt(aux)/numpy.cos(kickAngle)
    v0_x = v0*numpy.cos(kickAngle)
    v0_y = v0*numpy.sin(kickAngle)
#    print("v0:", v0,"\tv0_x:",v0_x,"\tv0_y:", v0_y)

    # Compute the GoalKeeper Distance from the Goal so it intersects the Ball Trajectory in the Rising Phase
    d_G2K=x0+v0_x*(v0_y-numpy.sqrt(numpy.power(v0_y,2)+2*g*(y0-Y_GK)))/g
    d_G2K=-d_G2K
#    print("d_G2K:",d_G2K)
    # ----------- #
    # ---- X ---- #
    # Compute Ball XY Coordinates from Ball Distance & Angle
    ball_x = ballDist*numpy.cos(numpy.pi/2-ballAngle)
    ball_y = ballDist*numpy.sin(numpy.pi/2-ballAngle)
#    print("Ball X:", ball_x,"\tBall Y:", ball_y)

    # Compute Cross between Goal and Ball for Keeper Positioning
    # Keeper
    # Keeper Point
    k_x=d_G2K*numpy.cos(numpy.pi/2-ballAngle)
    k_y=d_G2K*numpy.sin(numpy.pi/2-ballAngle)
    # Keeper Line
    m_k = -ball_x/ball_y
    b_k = k_y+(ball_x/ball_y)*k_x
    message = "Kx:{0:.3f}\tKy:{1:.3f}\tm_k:{2:.3f}\tb_k:{3:.3f}"
#    print(message.format(k_x,k_y,m_k,b_k))
    # ----------- #
    # Find wich Corner - Left or Right 
    if ballAngle>=0:
        goalSide = X_G/2
        mul = 1
    else:
        goalSide = -X_G/2
        mul = -1
    # Compute Corner Line
    m_c = - ball_y/(goalSide-ball_x)
    b_c = ball_y*(1+ball_x/(goalSide-ball_x))
    # Compute Corner Point
    c_x = (b_c-b_k)/(m_k-m_c)
    c_y = m_k*c_x+b_k
    message = "Post:{0:.3f}\tm_c:{1:.3f}\tb_c:{2:.3f}\tc_x:{3:.3f}\tc_y:{3:.3f}"
#    print(message.format(goalSide,m_c,b_c,c_x,c_y))
    # ----------- #

    # Distance from the K to the Corner     
    d_K2C = numpy.sqrt(numpy.power(c_x-k_x,2)+numpy.power(c_y-k_y ,2))

    # Distance from K Point to the Desired Position   
    if (d_K2C-r_GK<=r_GK):
        d_b = d_K2C-r_GK
    else:
        d_b = r_GK
#    print("d_K2C:", d_K2C,"\td_b:", d_b)
    
    xd = k_x + mul*d_b*numpy.cos(ballAngle)
    yd = k_y + mul*d_b*numpy.sin(-ballAngle)       
#    print("X:",xd, "\tY:", yd)  
    # ----------- #

    # Return the X Y Desired Coordinates for the Goal Keeper 
    return xd, yd