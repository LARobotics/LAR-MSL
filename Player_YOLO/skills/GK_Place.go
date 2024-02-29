package skills

import (
	"fmt"
	"image"
	"math"
	coms "player/communication"
)

const Goal_Y_position = 350
const Defend_X_position = 850

/*const defend_threshold = 100
const side_limits = Defend_X_position - 50*/

// Movement PID's
var defend_orientation = NewPid(0.3, 0, 0.1, 0.0, outputLimit_PID_move)
var place_atractor = NewAtractor(Katracao_place, Kintensidade_place, outputLimit_atractor_place)
var defend_atractor = NewAtractor(Katracao_defend, Kintensidade_defend, outputLimit_atractor_defend)

// A - Largura da porção da baliza a defender; B - Avanço da Elipse; Posição da Bola relativa ao centro da baliza
func Place(A float64, B float64, point image.Point, PosRobotRel image.Point, angle float64) (Pd image.Point) {
	Pd = image.Point{0, 0}
	var m = 0.0

	// Verify if the ball is inside the elipse, if so then follow the ball	// Rectangular aproximation
	if point.Y < int(B) && math.Abs(float64(point.X)) < A {
		Pd.X = point.X
	} else {
		m = float64(point.Y) / float64(point.X)
		Pd.X = int(B / math.Sqrt(m*m+(B*B)/(A*A)))
	}

	// Have a maximum value for the X position
	if Pd.X > int(A) {
		Pd.X = int(A)
	}

	// The slope signal defines the side
	if m < 0 {
		Pd.X = -Pd.X
	}

	// Define the y position of the robot
	Pd.Y = Goal_Y_position
	return Pd
}

var After_defend bool
var first_defend = true
var first_disp = true

const rot_threshold = 20
const disp_threshold = 7
const vel_treshold = 5

var disp_max float64

// Current GK Position; Desired Position; GK Orientation; GK Desired Orientation; Time stamp; Flag
func Kinematics(P_GK image.Point, P_d image.Point, robot_angle float64, desired_angle float64, dt int64, defending bool) {
	var vel float64
	//Send commands in more then 30 ms to ESP
	if !(float64(dt) < 30) {
		// Obtain the angle between the desired postion and the robot
		var ang_target = math.Atan2(float64(P_d.Y)-float64(P_GK.Y), (float64(-P_d.X))-float64(-P_GK.X))

		//Get the error between the desired angle and the robot angle
		var erro = int(desired_angle) - int(robot_angle)

		//Make the error be between 180 and -180
		for erro > 180 {
			erro -= 360
		}
		for erro <= -180 {
			erro += 360
		}

		//Get the rotational speed desired for the specific error
		rot := int(defend_orientation.Update(float64(erro), float64(dt*1000)))

		//Do a threshold so the rotational speed have a limit
		if rot > rot_threshold {
			rot = rot_threshold
		} else if rot < -rot_threshold {
			rot = -rot_threshold
		}

		//Displacement is the distance between the desired position and the robot
		var displacement = math.Sqrt(math.Pow(float64((P_d.Y/10)-(P_GK.Y/10)), 2) + math.Pow(float64((P_d.X/10)-(P_GK.X/10)), 2))

		//If the displacement is within the threshold
		if displacement > disp_threshold {
			//If the robot is defending a shot
			if defending {
				//Get a displacement of the X coordenate
				displacement = math.Sqrt(math.Pow(float64((P_d.X/10)-(P_GK.X/10)), 2))
				//If it is the first time, get the maximum displacement
				if first_disp {
					//destroy the flag
					first_disp = false
					//Get the max displacemnent
					disp_max = displacement
				}

				//Make the displacement vbe in percentage
				displacement = (displacement * 100) / disp_max
				//If it's outside the limits of a percentage, resolve it
				if displacement > 100 {
					displacement = 100
				} else if displacement < 0 {
					displacement = 0
				}

				//If is the first time that enters from defending, open the arms
				if first_defend {
					//Set the flag to false
					first_defend = false
					//Send the command to the pi pico to open the arms
					coms.SendDefend("Defend\n\r")
				}
				//Get the velocity from defend atractor
				vel = defend_atractor.Update((displacement))
				//vel = place_atractor.Update((displacement))
			} else {
				//Get the velocity from the place atractor
				vel = place_atractor.Update((displacement))
			}
		} else {
			//If not, make the velocity equal to zero
			vel = 0
		}

		//If the velocity is below the threshold, make it zero
		if vel < vel_treshold {
			vel = 0
		}

		//Obtain the direction that the robot needs to go, to go for the desired position
		var direction = int(((ang_target*180)/math.Pi)-float64(robot_angle)) - 90

		//if the robot is defending and the velocity goes to zero, it as already defended
		if defending && vel == 0 {
			//fmt.Println("Entrou 4")
			//Reset all the flags
			After_defend = true
			first_defend = true
			first_disp = true
			//Make the robot invert the motors
			vel = 20
			direction += 180
		}

		//Make the direction be between -180 and 180
		if direction < -181 {
			direction = 180 - (-direction - 180)
		} else if direction > 181 {
			direction = -180 + (direction - 180)
		}

		//Make the direction be between 0 and 360
		if direction < 0 {
			direction += 360
		}

		//Print every desired variable for debug

		/*fmt.Println("Displacement: ", displacement)
		fmt.Println("Angulo desejado: ", desired_angle)
		fmt.Println("Angulo guarda-redes: ", robot_angle)
		fmt.Println("Error: ", erro)
		fmt.Println("Posicao guarda-redes: ", P_GK)
		fmt.Println("Posicao desejada: ", P_d)
		fmt.Println("Velocidade: ", vel)
		fmt.Println("Angular: ", rot)
		fmt.Println("Direction: ", direction)
		fmt.Println("--------------------------------------------------")*/
		coms.SendCommandToESP(coms.CMD_all, int(vel), int(rot), int(direction), 0, 0, 0)
	}
}

func Align() {
	fmt.Println("-------------- Entrou Align --------------")
	coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)
}

// ----------------------------------------------- MANCHA -----------------------------------------------

const (
	ball_height float64 = 0.23 * 1000 // [mm]
	y0_ball     float64 = ball_height / 2
	shoot_angle float64 = 30 * math.Pi / 180
	x_Goal      float64 = 1 * 1000   // [mm] Ball Dist for Xmancha
	GK_Height   float64 = 0.8 * 1000 // [mm]
	GoalHeight  float64 = 1 * 1000   // [mm]
	g           float64 = 9.8 * 1000 // [m/s^2] earth gravitational aceleration
)
const (
	GoalWidth         = 2 * 1000   // [mm]
	GK_Width  float64 = 0.7 * 1000 // [mm]
)

func YMancha(x0_ball float64) (dist_GK2Goal float64) {
	// Verify if there is possible arc goal
	mul1 := math.Tan(shoot_angle) * (x_Goal - x0_ball)
	var1 := y0_ball + (mul1) - GoalHeight
	//fmt.Printf("var1=y0_ball + math.Tan(shoot_angle)*(x_Goal-x0_ball) - GoalHeight\n %v=%v + math.Tan(%v)*(%v) - %v\n", var1, y0_ball, shoot_angle, (x_Goal - x0_ball), GoalHeight)
	// var1 < 0 results in imaginary numbers; var1 = 0 causes indetermination {.../0}
	if var1 <= 0 {
		return 0
	}
	// Determine Inicial Velocity from an assumed shoot_angle, knowing ball distance from the goal
	v0 := (math.Sqrt((g * math.Pow(x_Goal-x0_ball, 2)) / (2 * var1))) / (math.Cos(shoot_angle))
	v0_x := v0 * math.Cos(shoot_angle)
	v0_y := v0 * math.Sin(shoot_angle)

	// GK Interception Distance
	delta := math.Sqrt(math.Pow(v0_y, 2) + 2*g*(y0_ball-GK_Height))
	dist_GK2Goal = math.Abs(x0_ball + v0_x*(v0_y-delta)/g)
	// fmt.Println("------ Y ------")
	//fmt.Println("v0:\t", v0)
	//fmt.Printf("Distância Keeper Goal: %v\n", dist_GK2Goal)
	return
}

func XMancha(dist_Goal2Ball float64, angle_Goal2Ball float64) (dist_GK2Goal float64) {
	/* With Ball coords rectangle
	var P_R, P_L float64 = 1000, -1000
	var ballX, ballY float64 = polar2rectangular(dist_Goal2Ball, angle_Goal2Ball)
	var dist_B2P float64 = math.Sqrt(math.Pow(P_R-ballX, 2))
	*/
	// Convert Ball distance and angle to Ball Coordinates. Relative to the Goal Line Center
	// var ball image.Point = polar2Rectangular(dist_Goal2Ball, angle_Goal2Ball)
	// fmt.Println("Ball XY:\t", ball)
	var post float64 = -GoalWidth / 2
	if angle_Goal2Ball > 0 {
		post = GoalWidth / 2
	}
	a := math.Pow(dist_Goal2Ball, 2)
	b := math.Pow(post, 2)
	c := (dist_Goal2Ball * GoalWidth * math.Cos((math.Pi/2)-angle_Goal2Ball))

	var dist_B2P float64 = math.Sqrt(a + b - c)

	// Compute distance between Ball and Right Pole
	//var dist_B2P float64 = math.Sqrt(math.Pow(dist_Goal2Ball, 2) + math.Pow(post, 2) - dist_Goal2Ball*GK_Width*math.Cos(math.Pi/2-angle_Goal2Ball))
	// Compute Theta ► aux angle. ball as reference. goal mid and right post
	var aux_angle float64 = math.Acos((math.Pow(post, 2) - math.Pow(dist_Goal2Ball, 2) - math.Pow(dist_B2P, 2)) / (-2 * dist_Goal2Ball * dist_B2P))
	// Desired distance of GK from the Ball
	var dist_Ball2GK float64 = (GK_Width / 2) / math.Tan(aux_angle)
	// Desired distance of GK from the Goal Line Center
	dist_GK2Goal = dist_Goal2Ball - dist_Ball2GK
	if dist_GK2Goal <= 0 {
		dist_GK2Goal = 0
	}
	return
}

func la_mancha(ball_dist float64, ball_angle float64) (PosDes image.Point) {
	// Intercept air balls
	y := YMancha(-ball_dist)

	// Intercept low balls
	x := XMancha(ball_dist, ball_angle)

	fmt.Println("--------------------------------------------------")
	fmt.Println("Input: ", ball_dist, ball_angle)

	// Estimate the best position knowing y&x estimations
	var select_dist float64 = 0
	if x > y {
		select_dist = x
		fmt.Println("Escolheu X!")
	} else {
		select_dist = y
		fmt.Println("Escolheu Y!")
	}

	PosDes.X = int(math.Sin(ball_angle) * select_dist)
	PosDes.Y = int(math.Cos(ball_angle) * select_dist)

	fmt.Println("Posicao desejada: ", PosDes)
	fmt.Println("--------------------------------------------------")
	return
}
