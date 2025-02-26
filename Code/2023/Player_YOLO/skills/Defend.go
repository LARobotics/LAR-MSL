package skills

import (
	"context"
	"fmt"
	"image"
	"math"
	GK_P "player/GK_Position"
	omni "player/OmniVision_pkg"
	coms "player/communication"
	"time"
)

// Minimum area to detect the ball
const Minimum_Area = 300

/* // Maximum angle of the robot
const max_angle = 50

// Minimum values of HSV to identify ball
const min_h = 4.0
const min_s = 115.0
const min_v = 76.0

// Maximum values of HSV to identify ball
const max_h = 13.5
const max_s = 255.0
const max_v = 255.0

var lowerMask = gocv.NewScalar(min_h, min_s, min_v, 0.0)
var upperMask = gocv.NewScalar(max_h, max_s, max_v, 0.0) */

// Variabels relative to Goal Elipse || A - Max width desired (half goal); B - Elipse Distance
var A float64 = A_ellipse
var B float64 = B_ellipse

const ka_angle = 0.00000002 //29000000 //0.000147
const kb_angle = 0.03333333 //60 //0.3
const max_angle = 50

//var kernel_erode = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(5, 5))
//var kernel_dilate = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(25, 25))

// Angle of view of camera
const Horizontal_Cam = 57.0

// Constant that defines the size of half the field
const half_field = int(omni.A * 10 / 2)

//const vertical_cam = 43
//const vertical_cam_angle = 90

//Angle of view of depth camera
/*const horizontal_depth_cam = 58.5
const vertical_depth_cam = 46.6
const no_vision_depth_cam = 60.75*/

// Number of Pixies of the camera
const width = 640

//const height = 480

//Goalkeeper characteristics
//const robot_height = 6

var desired_angle = 0.0

// Debug variables (Goalkeeper back to middle of the goal)
var Defending bool = false

//var attack_ball = false

func defend(ball_side float64, side int, Pos image.Point) (Pos_Des image.Point) {
	//check if the ball is goig outside the goal or directly to the robot
	if ball_side < 1400 && ball_side > 300 {
		if side == 0 {
			//go to the left
			Pos_Des.X = Defend_X_position
			Pos_Des.Y = Goal_Y_position
		} else {
			//go to the right
			Pos_Des.X = -Defend_X_position
			Pos_Des.Y = Goal_Y_position
		}
	} else if ball_side <= 300 {
		Pos_Des.X = 0
		Pos_Des.Y = Goal_Y_position
	} else {
		Pos_Des = Pos
		Defending = false
	}
	return Pos_Des
}

/* // Middle orientation PID constants
var kP = 0.35
var kI = 0.0
var kD = 0.08

// Middle orientation PID variables
var error_PID float64
var integral float64
var last_error = 0.0
var last_desired_angle = 0.0

// Constant for the angular threshold
const ang_threshold = 10
const ang_hist = 3

// Orient Goalkeeper and move the Goalkeeper back to middle after defence
func desired_orientation(dt float64, angle float64, ang_robot float64) int {
	var angular float64

	fmt.Println("Tempo de ciclo: ", dt)

	if angle > max_angle {
		angle = max_angle
	} else if angle < -max_angle {
		angle = -max_angle
	}

	//Obtain the error of the angle and keep the last one
	last_error = error_PID
	error_PID = angle - ang_robot

	if error_PID < ang_hist && error_PID > -ang_hist {
		error_PID = 0
		integral = 0
	}

	//Calcualate the Proporcional of the PID
	pTerm := kP * error_PID

	//Calcualate the Integral of the PID
	integral += error_PID * dt
	iTerm := kI * integral

	//Calcualate the Derivative of the PID
	dTerm := kD * ((error_PID - last_error) / dt)

	//Get the angular velocity
	angular = pTerm + iTerm + dTerm

	// Set a limit to the angle velocity
	if angular > ang_threshold {
		angular = ang_threshold
	} else if angular < -ang_threshold {
		angular = -ang_threshold
	}

	fmt.Println("Angulo desejado: ", angle)
	fmt.Println("Angulo guarda-redes: ", ang_robot)
	fmt.Println("Error: ", error_PID)
	return int(angular)
}

func ball_orientation(ball_1x int, DB coms.LocalDB) {
	//Check if the ball is out of range
	if ball_1x > 480 {
		//rotate to the right
		fmt.Println("Rotate to the right")
		//rotating = true
		//Angular = 20
	} else if ball_1x < 160 {
		//rotate to the left
		fmt.Println("Rotate to the left")
		//rotating = true
		//Angular = -20
	} else if 200 < ball_1x && ball_1x < 440 {
		//Stop rotating
		fmt.Println("Stop rotating")
		//robot_angle = GK_P.Get_robotAngle()
		//rotating = false
		//Angular = 0
	}
	if GK_P.Get_robotAngle(DB) > 60 || GK_P.Get_robotAngle(DB) < -60 {
		fmt.Println("Stop rotating")
		//Stop rotating
		//rotating = false
		//Angular = 0
	}
}*/

/*var hsv = gocv.NewMat()
var mask = gocv.NewMat()

//var window = gocv.NewWindow("Yellow Detection")

// function to detect the ball and return the position
func detect_ball(img gocv.Mat) (cx int, cy int) {
	cx = -1
	cy = -1
	gocv.CvtColor(img, &hsv, gocv.ColorBGRToHSV)
	gocv.InRangeWithScalar(hsv, lowerMask, upperMask, &mask)
	var kernel = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(5, 5))
	gocv.Erode(mask, &mask, kernel)
	kernel = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(10, 10))
	gocv.Dilate(mask, &mask, kernel)
	//window.IMShow(mask)
	cnts := gocv.FindContours(mask, gocv.RetrievalExternal, gocv.ChainApproxNone)
	var c int
	for c = 0; c < cnts.Size(); c++ {
		if gocv.ContourArea(cnts.At(c)) > Minimum_Area {
			var M = gocv.MinAreaRect(cnts.At(c)).Center
			cx = M.X
			cy = M.Y
			cnts.Close()
			return
		}
	}
	cnts.Close()
	return
}

// Number of Pixies of the field image
const image_width = 1307
const image_height = 980

var pixel_X_ref float64 = 160
var y_borders = 20
var pixel_Y_ref float64 = image_height / 2

var filename = "skills/Images/Field_Image.jpg"
var field = gocv.IMRead(filename, gocv.IMReadColor)

func represent_field(ball image.Point, robot image.Point) {
	var image_ball = image.Point{0, 0}
	var image_robot = image.Point{0, 0}

	field = gocv.IMRead(filename, gocv.IMReadColor)

	//Transformations from Meters to pixels for the field
	var transformation_X = float64((image_width - pixel_X_ref*2) / (omni.A * 10))
	var transformation_Y = float64(float64(image_height-y_borders*2) / float64(omni.B*10))

	//Coordinates to represent the ball in the image
	image_ball.X = int(pixel_X_ref + float64(ball.Y)*transformation_X)
	image_ball.Y = int(pixel_Y_ref - float64(ball.X)*transformation_Y)

	//Coordinates to represent the ball in the image
	image_robot.X = int(pixel_X_ref + float64(robot.Y)*transformation_X)
	image_robot.Y = int(pixel_Y_ref + float64(robot.X)*transformation_Y)

	fmt.Println("Transformation: ", transformation_X, transformation_Y)
	fmt.Println("Image Ball: ", image_ball)
	fmt.Println("Image Robo: ", image_robot)

	gocv.Circle(&field, image_ball, 20, color.RGBA{255, 255, 0, 255}, -1)
	gocv.Circle(&field, image_robot, 20, color.RGBA{255, 0, 0, 255}, -2)
}*/

func get_point(object_x float64, dist float64, PosRobotRel image.Point, angle float64) image.Point {
	//inicialize variables
	var x = 0.0
	var y = 0.0
	var distance image.Point

	//obtain the horizontal distance from the object to the center of the image (pixels)
	var dist_middle = ((width / 2) - object_x)

	//obtain the angle between the object and the center
	var alfa_linha = dist_middle * horizontal_cam / width

	var alfa = alfa_linha + angle

	/*Code for the kinect v1.1
	//obtain the horizontal distance between the object and the robot / Equivalent to x coordinate
	x = dist * math.Sin(alfa*(math.Pi/180))

	//obtain the vertical distance between the object and the robot / Equivalent to y coordinate
	y = dist * math.Cos(alfa*(math.Pi/180))*/

	//Code for the kinect v1.2
	//obtain the horizontal distance between the object and the robot / Equivalent to x coordinate
	x = dist * math.Tan(alfa*(math.Pi/180))

	//obtain the vertical distance between the object and the robot / Equivalent to y coordinate
	y = dist

	//Translation between Robot referencial to goal referencial
	distance.X = PosRobotRel.X + int(x)
	distance.Y = PosRobotRel.Y + int(y)

	return distance
}

func obtain_lateral_GK(point image.Point, point2 image.Point, robot image.Point, ang_robot float64) (ball_side float64, side int) {
	//obtain the slope and the origin
	var m = (float64(point2.Y) - float64(point.Y)) / (float64(point2.X) - float64(point.X))
	var b = float64(point.Y) - (m * float64(point.X))

	//make a limit for the values
	if m > 50 {
		m = 50
	} else if m < -50 {
		m = -50
	}
	if b > 100000 {
		b = 100000
	} else if b < -100000 {
		b = -100000
	}

	//Obtain the predicted location of the ball
	ball_side = -(b / m)
	side = 0

	//if it is negative means is in the rigth side
	if ball_side < 0 {
		ball_side = -ball_side
		side = 1
	}
	return
}

func obtain_DB(position image.Point, ang_robot float64, ang_ball float64, dist float64) (point image.Point) {
	//Rotate the referencial to be in the same direction as the goal
	if dist != 0 {
		var alpha = ang_ball + ang_robot

		//Calculate the ball position in the direction of the goal referencial
		var x_linha = dist * 10 * math.Sin(alpha*(math.Pi/180))
		var y_linha = dist * 10 * math.Cos(alpha*(math.Pi/180))

		//Translation to the goal referencial
		point.X = int(x_linha) + position.X
		point.Y = int(y_linha) + position.Y
	} else {
		point = image.Point{0, half_field}
	}

	return
}

const num_pos = 30

var pos_ball [num_pos]image.Point

func filter(ball image.Point) (ret image.Point) {
	var sum float64

	for i := len(pos_ball) - 1; i > 0; i-- {
		pos_ball[i] = pos_ball[i-1]
	}

	pos_ball[0] = ball

	for i := 0; i < len(pos_ball); i++ {
		ret.X += pos_ball[i].X / (i + 1)
		ret.Y += pos_ball[i].Y / (i + 1)
		sum += 1 / float64(i+1)
	}

	ret.X = int(float64(ret.X) / sum)
	ret.Y = int(float64(ret.Y) / sum)

	return ret
}

func rec2pol(rec image.Point) (dist float64, angle float64) {
	dist = math.Sqrt(math.Pow(float64(rec.Y), 2) + math.Pow(float64(rec.X), 2))
	angle = math.Atan2(float64(rec.Y), float64(rec.X))
	return
}

// Variables related to the team and opponent robots
var team_pos []image.Point
var opponent_pos []image.Point
var robot_pos image.Point

func get_rob_ball(DB coms.LocalDB) (cx int, cy int, dist uint32, ball_detected bool) {
	//Get the position of the ball
	for i := 0; i < len(resp.Objects); i++ {
		switch resp.Objects[i].Id {
		case 0: // Ball
			cx = int(resp.Objects[i].X)
			cy = int(resp.Objects[i].Y)
			dist = resp.Objects[i].Dist
			ball_detected = true
			//fmt.Println("Encontrou bola: ", cx2, cy2, dist2)
		case 1: // Blue shirt
			// Get the coordinates and distance of the robot
			fmt.Println("Robo return: ", resp.Objects[i].X, float64(resp.Objects[i].Dist))
			robot_pos = get_point(float64(resp.Objects[i].X), float64(resp.Objects[i].Dist), GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
			if robot_shirt == RED_SHIRT { // if the team is playing in red
				// Save the robot in the array
				opponent_pos = append(opponent_pos, robot_pos)
			} else {
				team_pos = append(team_pos, robot_pos)
			}
		case 4: // Red shirt
			// Get the coordinates and distance of the robot
			robot_pos = get_point(float64(resp.Objects[i].X), float64(resp.Objects[i].Dist), GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
			if robot_shirt == BLUE_SHIRT { // if the team is playing in blue
				// Save the robot in the array
				opponent_pos = append(opponent_pos, robot_pos)
			} else {
				team_pos = append(team_pos, robot_pos)
			}
		case 5: // Robot
			// Get the coordinates and distance of the robot
			robot_pos = get_point(float64(resp.Objects[i].X), float64(resp.Objects[i].Dist), GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
			// Save the robot in the array
			opponent_pos = append(opponent_pos, robot_pos)
		}
	}
	return
}

const Y_area = 3000
const X_area = 6000
const dist2ball float64 = 1000
const ally_dist2ball = 1000

func mancha_situation(ball image.Point) (mancha bool) {
	var rob_dist2ball float64
	mancha = false
	// Verify if the ball is inside the big area
	if ball.Y < Y_area && math.Abs(float64(ball.X)) < X_area {
		fmt.Println("Bola dentro!")
		// Check every enemy
		for i := 0; i < len(opponent_pos); i++ {
			fmt.Println("Inimigo: ", opponent_pos[i].X, opponent_pos[i].Y)
			rob_dist2ball = math.Sqrt(math.Pow(float64(ball.Y-opponent_pos[i].Y), 2) + math.Pow(float64(ball.X-opponent_pos[i].X), 2))
			fmt.Println("distancia inimigo: ", rob_dist2ball)
			// if the attacker has the ball
			if rob_dist2ball < dist2ball {
				fmt.Println("Inimigo dentro!")
				// Check every ally
				for i := 0; i < len(team_pos); i++ {
					rob_dist2ball = math.Sqrt(math.Pow(float64(ball.Y-team_pos[i].Y), 2) + math.Pow(float64(ball.X-team_pos[i].X), 2))
					// if the ally is in front of the ball
					if rob_dist2ball < ally_dist2ball && team_pos[i].Y < ball.Y {
						fmt.Println("Aliado dentro!")
						mancha = false
					} else { // If there's no ally coverage go for mancha
						fmt.Println("Aliado fora!")
						mancha = true
						return
					}
				}
			} else {
				// if not, go to the ball to defend it
				mancha = false
				//attack_ball = true
			}
		}
	}
	return
}

// Variable threshold that checks the robot closest to the ball
const robot_dist_pen float64 = 500

// Function to defend the penalti
func defend_penalti(ball image.Point) (posDes image.Point) {
	var rob_dist2ball float64
	var take_pen = false
	var shooter image.Point
	var slope int
	var b int

	//Check wich robot is in the ball and return that robot
	for i := 0; i < len(opponent_pos) && !take_pen; i++ {
		rob_dist2ball = math.Sqrt(math.Pow(float64(ball.Y-opponent_pos[i].Y), 2) + math.Pow(float64(ball.X-opponent_pos[i].X), 2))
		//If the attacker has the ball
		if rob_dist2ball < robot_dist_pen {
			take_pen = true
			shooter = opponent_pos[i]
		}
	}

	//If a robot was seen in near the ball
	if take_pen {
		//Get the line that intercets the the ball and robot
		slope = (shooter.Y - ball.Y) / (shooter.X - ball.X)
		b = ball.Y - (slope * ball.X)

		//Make the position of the robot be the interception of the line in the goal referencial
		posDes = image.Point{-(b / slope), Goal_Y_position}
		if math.Abs(float64(posDes.X)) > Defend_X_position {
			posDes.X = Defend_X_position
		}
	}
	return
}

func skDefend(args_ [7]int, quit chan int) {
	// GoalKeeper desired position
	var PosDes image.Point
	// Ball coordinates and distance of the two ball frames
	var cx1 = -1
	var cy1 = -1
	var cx2 = -1
	var cy2 = -1
	var dist0 = uint32(0)
	var dist1 = uint32(0)
	var dist2 = uint32(0)
	//var point_0 = image.Point{-1, -1}
	var point_1 = image.Point{-1, -1}
	var point_2 = image.Point{-1, -1}
	// Variables to the distance of the ball trajectory
	var ball_side = 0.0
	var side = 0
	var last_side = 0
	// Variable to the position of the ball on the goal image
	//var position = 0.0
	var ball_dist, ball_angle float64
	// Verify if a ball was detected
	var ball_detected = false
	// Variable of the DataBase
	var DB coms.LocalDB
	// Variable for the angular velocity
	var dt int64 = 0

	var mancha bool = false

	var arg = args_
	//var vare = arg[0]

	/*var goal_dist_1 int = 0
	var goal_dist_2 int = 0*/

	fmt.Println("-----------------------------------START DEFEND-----------------------------------", arg)
	// Inicialize the Omni at 0
	coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)

	// Open image of the ball prediction in the goal
	/* var filename2 = "skills/Images/goal.png"
	var window2 = gocv.NewWindow("Goal") */
	//var goal = gocv.IMRead(filename2, gocv.IMReadColor)

	// Open image of the field
	//var window = gocv.NewWindow("Field")

	// Times for the PID calculations
	var current_time time.Time
	var old_time time.Time

	// Inicialize endless cycle
	for {
		select {
		case <-quit:
			fmt.Println("----------------------------- Quit -----------------------------")
			wait_4_skill.Done()
			//window2.Close()
			return
		default:

			//Receive arguments from base station
			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()

			//Update the database information
			coms.GetDatabase(&DB)

			// If it doesn't find the database, try again
			if DB.Team != nil {
				//Get the position of the objects on the kinect frame
				resp, _ = client.Send_Kinect(context.Background(), &req)

				//Save the previous values of the ball
				cx1, cy1, dist0, dist1 = cx2, cy2, dist1, dist2

				//Get the ball and robots coordinates
				cx2, cy2, dist2, ball_detected = get_rob_ball(DB)

				//If the GK is in the default stage (not penalty)
				if arg[5] == 0 {
					//If a ball was detected
					if ball_detected && dist2 != 0 && dist2 > 200 {
						ball_detected = false

						//Save the previous ball point
						point_1 = point_2
						//Get the new ball point and filter the value
						point_2 = get_point(float64(cx2), float64(dist2), GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
						point_2 = filter(point_2)

						// If the ball moved into the robot calculate the trajectory
						if cx1 != -1 && cy1 != -1 && dist1 != 0 && dist1 > 200 && dist2+100 < dist1 && dist1+100 < dist0 && !Defending {
							Defending = true
							last_side = side

							// Returns wich side of the robot the ball is going and the distance
							ball_side, side = obtain_lateral_GK(point_1, point_2, GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
							if ball_side < 200 {
								side = last_side
							}

							// Call the function to obtain the defend position
							PosDes = defend(ball_side, side, PosDes)

							// Get the starting distance to defend
						}
					} else { //If the ball wasn't detected or is not reading distance, get it from database
						cx2 = -1
						cy2 = -1
						dist2 = 0
						if DB.Ball.Conf > 30 {
							point_2 = obtain_DB(GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB), float64(DB.Ball.Angle), float64(DB.Ball.Dist))
						} else {
							point_2 = image.Point{0, half_field}
						}
						if point_2.Y < 0 {
							point_2 = image.Point{0, half_field}
						}
					}
					//fmt.Println("Posição da bola: ", point_2)
					//fmt.Println("Posicao antes: ", GK_P.Get_robotPosition(DB, half_field))

					// Verify if the Robot is defending a shoot
					if Defending {
						// If is defending a shoot, verify when is already defended
						if After_defend {
							After_defend = false
							Defending = false
						}
					} else {
						//mancha = mancha_situation(point_2)
						mancha = false

						if !mancha {
							PosDes = Place(A, B, point_2, GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
							//desired_angle = math.Pow(float64(PosDes.X/10), 3)*ka_angle + float64(PosDes.X/10)*kb_angle
							desired_angle = ka_angle*math.Pow(float64(PosDes.X), 3) + kb_angle*float64(PosDes.X)
							if math.Abs(desired_angle) > max_angle {
								desired_angle = max_angle
							}
						} else {
							ball_dist, ball_angle = rec2pol(point_2)
							PosDes = la_mancha(ball_dist, ball_angle)
							if ball_dist >= 3000 {
								PosDes = image.Point{0, 0}
							}
							desired_angle = ball_angle
							if PosDes.Y == 0 { //PosDes.X == 0 &&
								PosDes = Place(A, B, point_2, GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
								if math.Abs(desired_angle) > max_angle {
									desired_angle = max_angle
								}
							}
						}
					}
				} /*else if arg[5] == 1 { //If a penalty was indicated
					//Go to the center of the goal
					PosDes = image.Point{0, Goal_Y_position}
					//Oriented to the front
					desired_angle = 0
					Defending = false
				} else { //If the penalty start
					//Verify if the ball is detected
					if ball_detected {
						//Get the point of the ball in the goal referencial
						point_2 = get_point(float64(cx2), float64(dist2), GK_P.Get_robotPosition(DB, half_field), GK_P.Get_robotAngle(DB))
						//Call the penalti function
						PosDes = defend_penalti(point_2)
					} else {
						//If the ball is not detected, stay in the middle
						PosDes = image.Point{0, Goal_Y_position}
					}
					//Always orient in front
					desired_angle = 0
				}*/
				// Reset PID time
				old_time = current_time

				// Orient in the desired angle
				current_time = time.Now()
				dt = current_time.Sub(old_time).Milliseconds()
				// Make the Robot go to the desired place
				Kinematics(GK_P.Get_robotPosition(DB, half_field), PosDes, GK_P.Get_robotAngle(DB), desired_angle, dt, Defending)

				/* //Print in the goal image the ball prediction
				if ball_side != 0 {
					if side == 0 {
						if ball_side <= 1000 {
							position = (ball_side * 167 / 1000) + 220
							gocv.Circle(&goal, image.Pt(int(position), 190), 20, color.RGBA{255, 0, 0, 255}, 5)
						} else {
							gocv.Circle(&goal, image.Pt(450, 190), 20, color.RGBA{255, 0, 0, 255}, 5)
						}
					} else {
						if ball_side <= 1000 {
							position = 220 - (ball_side * 183 / 1000)
							gocv.Circle(&goal, image.Pt(int(position), 190), 20, color.RGBA{255, 0, 0, 255}, 5)
						} else {
							gocv.Circle(&goal, image.Pt(10, 190), 20, color.RGBA{255, 0, 0, 255}, 5)
						}
					}
					ball_side = 0
				}
				//represent_field(point_2, GK_P.Get_robotPosition(DB, half_field))
				// Open the images windows
				//window.IMShow(field)
				//window.WaitKey(1)
				window2.IMShow(goal)
				window2.WaitKey(1) */
			}
		}
	}
}
