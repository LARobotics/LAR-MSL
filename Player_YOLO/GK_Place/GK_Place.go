package GK_Place

import (
	"fmt"
	"image"
	"math"
	coms "player/communication"
)

const horizontal_cam = 64.0
const width = 640
const Goal_Y_position = 100
const Defend_X_position = 550

func get_slope(ball_x float64, dist float64, PosRobotRel image.Point, angle float64) (m float64) {
	//inicialize variables
	var x = 0.0
	var y = 0.0
	var distance image.Point

	//obtain the horizontal distance from the ball to the center of the image (pixels)
	var dist_middle = ((width / 2) - ball_x)

	//obtain the angle between the balls and the center
	var alfa_linha = dist_middle * horizontal_cam / width

	var alfa = alfa_linha + angle

	/*Code for the kinect v1.1
	//obtain the horizontal distance between the ball and the robot / Equivalent to x coordinate
	x = dist * math.Sin(alfa*(math.Pi/180))

	//obtain the vertical distance between the ball and the robot / Equivalent to y coordinate
	y = dist * math.Cos(alfa*(math.Pi/180))*/

	//Code for the kinect v1.2
	//obtain the horizontal distance between the ball and the robot / Equivalent to x coordinate
	x = dist * math.Tan(alfa*(math.Pi/180))

	//obtain the vertical distance between the ball and the robot / Equivalent to y coordinate
	y = dist

	//Translation between Robot referencial to goal referencial
	distance.X = PosRobotRel.X + int(x)
	distance.Y = PosRobotRel.Y + int(y) + Goal_Y_position

	fmt.Println("Posição Kinect: ", distance.X, distance.Y)

	//obtain the slope and the origin
	m = float64(distance.Y) / float64(distance.X)
	return
}

// A - Largura da porção da baliza a defender; B - Avanço da Elipse; Posição da Bola relativa ao centro da baliza
func Place(A float64, B float64, Ball image.Point, dist uint32, PosRobotRel image.Point, angle float64, x_2D int, y_2D int) (Pd image.Point) {
	Pd = image.Point{0, 0}
	var m = 0.0

	if Ball.X != -1 && dist != 0 {
		m = get_slope(float64(Ball.X), float64(dist), PosRobotRel, angle)
	} else {
		m = float64(y_2D) / float64(x_2D)
		fmt.Println("Posição DB: ", x_2D, y_2D)
	}

	Pd.X = int(B / math.Sqrt(m*m+(B*B)/(A*A)))
	if Pd.X > 550 {
		Pd.X = 550
	}
	if m < 0 {
		Pd.X = -Pd.X
	}
	Pd.Y = Goal_Y_position
	return Pd
}

var After_defend bool
var Velocity_Thr_Max int = 60
var Velocity_Thr_Min int = 5
var ang_target float64
var direction int
var velocity int
var error float64
var kp = 0.7

func Kinematics(P_GK image.Point, P_d image.Point, Angular int, defending bool, robot_angle float64) {
	//Verify if the robot is defending
	if !defending {
		//If not, got to the position with a minimum control
		error = math.Sqrt(math.Pow((float64(P_d.Y)-float64(P_GK.Y))/10, 2) + math.Pow((float64(P_d.X)-float64(P_GK.X))/10, 2))
		velocity = int(error * kp)
	} else {
		//If it is, we want him to go as fast as possible to defend
		if (P_d.X > 300 && P_GK.X > P_d.X-100) || (P_d.X < -300 && P_GK.X < P_d.X+100) {
			velocity = 0
			After_defend = true
		} else {
			velocity = 100
		}
	}

	//Calculate the angle between the target and the robot
	ang_target = math.Atan2(float64(P_d.Y)-float64(P_GK.Y), (float64(-P_d.X))-float64(-P_GK.X))

	//Obtain the direction that the robot needs to go, in the goal referencial
	direction = int((ang_target*180)/3.14) - int(robot_angle) - 90
	if direction < 0 {
		direction += 360
	}

	//DO a threshold for the velocity
	if velocity > Velocity_Thr_Max {
		velocity = 60
	}
	if velocity < Velocity_Thr_Min {
		velocity = 0
	}

	fmt.Println("Posicao guarda-redes: ", P_GK)
	fmt.Println("Posicao desejada: ", P_d)
	/*fmt.Println("Velocidade: ", velocity)
	fmt.Println("Angular: ", Angular)
	fmt.Println("Direction: ", direction)*/
	//Send the command to update the motor values
	//coms.SendCommandToESP(coms.CMD_all, velocity, Angular, direction, 0, 0, 0)
}

func Align() {
	fmt.Println("-------------- Entrou Align --------------")
	coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)
}
