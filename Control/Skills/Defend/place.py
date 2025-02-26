import math

# Compute Goal Keeper Position to block the kicker for a parabolic shot 
#considering the best possible shot from the known ball position
K_diameter = 50 # Keeper Diameter
ky = 300    # Desired Fixed Y Coordinate
ky_MAX = K_diameter # Min dist to Ball 
#INPUT: A - Largura [mm] da porção da baliza a defender; B - Avanço [mm] da Elipse; Ball - Posição XY da Bola relativa ao centro da baliza
#OUTPUT: K - Posição XY desejada do Robot, W - Angulo do robot 
def gk_place(A, B, Ball_x, Ball_y):
    '''
        INPUTS - A - Largura [mm] da porção da baliza a defender; B - Avanço [mm] da Elipse; Ball - Posição [mm] XY da Bola relativa ao centro da baliza\\
        OUTPUT - Desired Keeper XY[mm] A[rad]
    '''
    #?print("Elipse", A, B)
    #print("Ball XY", Ball_x, Ball_y)
    if A == 0:
        A = 0.000001
    if Ball_x == 0:
        Ball_x = 0.000001
    # Ball Slope - Absolute Y to prevent ball behind the Goal Line
    Ball_m = abs(Ball_y)/Ball_x
    #?print("Ball Slope:", Ball_m)
    # Keeper X Coordinate
    Kx = B/math.sqrt(math.pow(Ball_m,2)+(math.pow(B,2)/math.pow(A,2)))
    
    # OPTIMISE 1/sqrt()
    if Ball_x <= 0:
        Kx = -Kx
    #?print("Kx:", Kx)
    # Ball inside Ellipse. ADD Linha de Fundo LIMIT
    if -A <= Ball_x and Ball_x<=A:
        if Ball_y <= math.sqrt(math.pow(B,2)-math.pow(B,2)/math.pow(A,2)*math.pow(Ball_x,2)):
            Kx = Ball_x
    # POSITION
    Ky = ky
    #print("Bx",Ball_x, "A", abs(A))
    #print("By", Ball_y, ky+ky_MAX)
    
    if -A <= Ball_x and Ball_x <= A and Ball_y >= 0 and Ball_y <= ky + ky_MAX: #Ball_x < abs(A)
        print("dentro da elipse Y:", Ball_y-ky_MAX)
        if Ball_y-ky_MAX>0:
            Ky = Ball_y-ky_MAX
        else:
            Ky = 0
    #print("Keeper XY:", Kx, Ky)

    # ORIENTATION
    Km = 0.0
    if (Ball_x-Kx==0 or Ball_y-Ky==0):
        Ka = 0
    else:
        Km = (Ball_y-Ky)/(Ball_x-Kx)
        #print("Km:", Km)
        if Ball_y<ky: # Ball Behing Keeper
            print("Ball Behind")
            if Ball_x<-A:   # Left Side
                print("Left") 
                Km=-0.01  # Zero Negative
            elif Ball_x > -A and Ball_x < A:    # Middle
                print("Mid")
                Km=-Km
            elif Ball_x>=A: # Righ Side
                print("Right") 
                Km=+0.01  # Zero Positive
        Ka = math.atan(1/Km)  # -pi:pi

    #print("Keeper m", Km,"ang", Ka)
        
    return Kx, Ky, Ka
