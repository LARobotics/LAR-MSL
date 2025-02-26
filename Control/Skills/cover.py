import math
import Skills.Cover.Block as Block
import Skills.PID as PID

linVel = PID.PID(9,0.00,0.00,0.0,20) # MAX: 70
angVel = PID.PID(0.01,0.03,0.003,0.05,15) # MAX 15
# def closestBody(tar_x, tar_y, body_x, body_y):
#     return 
def skCover(data, dt):
    # * INPUT
    field_Lenght = 2200 # [cm]  #! CONFIG FILE 
    x1 = data.baseStation.arg0
    y1 = data.baseStation.arg1
    x2 = data.baseStation.arg2
    y2 = data.baseStation.arg3
    a  = data.baseStation.arg4
    block_overwrite = data.baseStation.arg5 # * 0: Default 1: Block 
    cover_type = 0 #data.baseStation.arg5 # * 0: Default 1: Block 
    print(f"BS: {round(x1,2)} : {round(y1,2)} ; {round(x2,2)} : {round(y2,2)} ; {round(a,2)} ; {cover_type}")
    # Posts
    goal_cx, goal_cy = 0,0
    goals = data.goalPosts
    # Ball Position to Robot
    ball_angle = data.ball.ang # [deg]
    ball_dist = data.ball.dist # [cm]
    ball_x = data.ball.x/100       # [cm] to [m]
    ball_y = data.ball.y/100       # [cm] to [m]
    
    #print(f"TARGET_1: {x1};{y1}\tTARGET_2: {x2};{y2}")
    # Robot Absolute/Field Position
    cur_x = data.robot.x    # [cm]
    cur_y = data.robot.y    # [cm]
    cur_a = data.robot.ang

    # * PROCESS
    # Find cosest bots to the Target Positions
    tar1 = data.Position()
    tar2 = data.Position()
    d_min = 22000           #! GET FIELD LENGHT # Reset to Absolute Max Value - FIELD LENGHT 
    opponents = data.robots#data.opponents
    print(f"LEN-Opponents= {len(opponents)}  {opponents}")
    if len(opponents) == 0:
        '''Use Basestation Target Points'''
        tar1.x = x1
        tar1.y = y1
        tar2.x = x2
        tar2.y = y2 
    else:
        '''Use Detected Target Points Closest to the Basestation Target Points'''
        # Target 1
        i = 0 
        for bot in opponents:
            print(f"BOT1:{bot.x};{bot.y}")
            i += 1
            d_tar2bot = math.sqrt((bot.x - x1)**2 + (bot.y - y1)**2)
            if d_tar2bot < d_min:
                d_min = d_tar2bot
                tar1.x = bot.x / 100 # [cm] to [m]
                tar1.y = bot.y / 100 # [cm] to [m]
        
        # Target 2
        i=0
        d_min = 22000           #! GET FIELD LENGHT # Reset to Absolute Max Value - FIELD LENGHT
        for bot in opponents:
            i+=1
            print(f"BOT2:{bot.x};{bot.y} | {tar1.x*100} {tar1.y*100}")
            d_tar2bot = math.sqrt((bot.x - x2)**2 + (bot.y - y2)**2)
            if d_tar2bot < d_min and (round((bot.x / 100), 2) != round(tar1.x, 2)) and (round(bot.y / 100, 2) != round(tar1.y, 2)):#bot != tar1: #! TRY TO FIX COLISION
                d_min = d_tar2bot
                #tar2 = bot
                tar2.x = bot.x / 100 # [cm] to [m]
                tar2.y = bot.y / 100 # [cm] to [m]

        if len(opponents) == 1:#tar1.x == tar2.x and tar1.y ==tar2.y:
            print(f"<SINGLE OPPONENT>")
            tar2.x = x2
            tar2.y = y2
    
    # print(f"LOCAL TARGET: {round(tar1.x,2)}; {round(tar1.y, 2)} : {round(tar2.x, 2)}; {round(tar2.y, 2)}")

    #? des_x = tar1.x + a*(tar2.x-tar1.x)
    #? des_y = tar1.y + a*(tar2.y-tar1.y)
    #? des_a = ball_angle
    #? print(f"Desired: {round(des_x,2)}: {round(des_y)} : {round(des_a)}")
    #? # Do not allow to the robot to hit one of he oponnets positions
    #? SELF2TAR_TH = 1
    #? dist2Tar = math.sqrt((tar1.x)**2 + (tar1.y)**2)
    #? if dist2Tar < SELF2TAR_TH:
    #?     print(f"<TOO CLOSE> {dist2Tar}")
    #?     des_x = 0   
    #?     des_y = 0   # data.robot

    #print(f"DESIRED XYA: {round(des_x,2)};{round(des_y,2)};{round(des_a,2)}")
    # Compute Intersection Point from given Cover Points
    # * Default Cover
    #des_x = x1 + a*(x2-x1)
    #des_y = y1 + a*(y2-y1)
    # If any of the cover points is the goal
    # * Block
    #if (y1 == 0 and x1 == -field_Lenght/2) or (y2 == 0 and x2 == -field_Lenght/2):
    #    des_x, des_y = Block.skill_block(ball_angle, ball_dist) #TODO Convert to Absolute Coordinates 
    if block_overwrite:
        # * PROCESS
        # Find cosest posts to the Target Positions
        tar1 = data.Position()
        tar2 = data.Position()
        print(f"Clear TARGET: {tar1}\n{tar2}")
        d_min = 22000           #! GET FIELD LENGHT # Reset to Absolute Max Value - FIELD LENGHT 
        posts = data.goalPosts#data.opponents
        print(f"LEN-posts= {len(posts)}  {posts}")
        print(f"LEN-Opponents= {len(opponents)}  {opponents}")
        if len(posts) == 0:
            '''Use Basestation Target Points'''
            tar1.x = x1
            tar1.y = y1
        else:
            '''Use Detected Target Points Closest to the Basestation Target Points'''
            # Target 1
            i = 0 
            for post in posts:
                print(f"closest:{post.x};{post.y}")
                i += 1
                d_tar2post = math.sqrt((post.x - x1)**2 + (post.y - y1)**2)
                if d_tar2post < d_min:
                    d_min = d_tar2post
                    tar1.x = post.x / 100 # [cm] to [m]
                    tar1.y = post.y / 100 # [cm] to [m]
        
        if len (opponents) == 0:
            '''Use Basestation Target Points'''
            tar2.x = x2
            tar2.y = y2 
        else:
            # Target 2 # Opponents
            i = 0
            for bot in opponents:
                print(f"BOT1:{bot.x};{bot.y}")
                i += 1
                d_tar2bot = math.sqrt((bot.x - x1)**2 + (bot.y - y1)**2)
                if d_tar2bot < d_min:
                    d_min = d_tar2bot
                    tar2.x = bot.x / 100 # [cm] to [m]
                    tar2.y = bot.y / 100 # [cm] to [m]
            
        print(f"LOCAL TARGET: {round(tar1.x,2)}; {round(tar1.y, 2)} : {round(tar2.x, 2)}; {round(tar2.y, 2)}")

    des_x = tar1.x + a*(tar2.x-tar1.x)
    des_y = tar1.y + a*(tar2.y-tar1.y)
    des_a = ball_angle
    print(f"Desired: {round(des_x,2)}: {round(des_y)} : {round(des_a)}")
    # Do not allow to the robot to hit one of he oponnets positions
    SELF2TAR_TH = 1
    dist2Tar = math.sqrt((tar1.x)**2 + (tar1.y)**2)
    if dist2Tar < SELF2TAR_TH:
        print(f"<TOO CLOSE> {dist2Tar}")
        des_x = 0   
        des_y = 0   # data.robot
    # MANCHA/BLOCK
    if cover_type :
        print(f"<MANCHA>")
        # * Allocate Target_1 to Ball
        x1 = ball_x
        y1 = ball_y

        # * Allocate Target_2 to Goal
        # Find Goal Center by Avegare Point between goalPosts
        i = 1
        for i in range(0, len(goals)):
            if i == 2: break
            goal_cx += goals[i].x
            goal_cy += goals[i].y
        
        # Posts Angle
        if len(goals) >= 2:
            posts_a = math.atan((goals[0].y - goals[0].y)/goals[1].x - goals[1].x)
            print(f"Nmr Posts: ",i)
            goal_cx /= i
            goal_cy /= i
            ## * RELATIVE to ROBOT 2 RELATIVE to GOAL
            # Distance Goal Center Line 2 Robot
            if goal_cx == 0:    # Avoid mathematical errors 
                goal_cx = 0.0001
            goal_a = math.atan(goal_cy/goal_cx)
            goal_d = math.sqrt(goal_cx**2 + goal_cy**2)
            # PARAM1 Ball Dist # Find Distance between Ball and Goal Center Line - COS LAW
            d_BG = math.sqrt(ball_dist**2+goal_d**2-2*ball_dist*goal_d*math.cos(ball_angle-goal_a))
            
            # PARAM2
            a_B2G = math.pi/4-math.atan2(ball_y-goal_cy, ball_x-goal_cx)+posts_a
            ## 
            # * Compute Desired XY for Block(Mancha)
            #Computation with reference to the Goal
            print(f"_INPUT: {d_BG};{a_B2G}")
            des_x, des_y = Block.skill_block(a_B2G, d_BG) # TODO Convert to Absolute Coordinates
            print(f"_OUTPUT: {des_x};{des_y}") 
            
        else:
            print(f"<NONE/SINGLE POST>")
            posts_a = 0
            if ball_dist < SELF2TAR_TH:
                des_x = ball_x
                des_y = ball_y
            else:
                print(f"<BALL TOO CLOSE>")
                des_x = 0 
                des_y = 0 

    # * OUTPUT
    # Delta Pose
    dx = des_x #-cur_x
    dy = des_y #-cur_y
    dxy = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
    da = des_a

    # Control
    #linear_vel = 0.1 * dxy
    direction = math.atan2(des_y,des_x)*180/math.pi
    #angular_vel = 0.1*da
    linear_vel = linVel.Update(dxy,dt)
    angular_vel = angVel.Update(da,dt) 
    # Show
#    print(f"Error: dxy = {round(dxy,2)} ; dx = {round(dx,2)} ; dy = {round(dy,2)}") 
    print(f"Kinematics: {linear_vel}; {direction}; {angular_vel}")
    return linear_vel, direction, angular_vel, round(des_x+cur_x, 2), round(des_y+cur_y, 2), da-cur_a
#des_x_field/1000, des_y_field/1000
