package GK_vision

import (
	"fmt"
	"image"
	"image/color"
	"math"
	coms "player/communication"
	freenect "player/freenect"
	"time"

	"gocv.io/x/gocv"
)

// Minimum area to detect the ball
const MinimumArea = 300

// Minimum values of HSV to identify ball
const min_h = 4.0
const min_s = 115.0
const min_v = 76.0

// Maximum values of HSV to identify ball
const max_h = 13.5
const max_s = 255.0
const max_v = 255.0

//HSV values

var lowerMask = gocv.NewScalar(min_h, min_s, min_v, 0.0)
var upperMask = gocv.NewScalar(max_h, max_s, max_v, 0.0)

//var kernel_erode = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(5, 5))
//var kernel_dilate = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(25, 25))

// Angle of view of camera
const horizontal_cam = 64.0

//const vertical_cam = 48.6
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

// Kinect variables
var kinect_device freenect.Kinect

// Omni variables
var delta_y = 0
var y_movement = 0
var Velocity = 0
var Angular = 0.0
var Direction = 0

func defend(ball_side float64, side int) {
	//check if the ball is goig outside the goal or directly to the robot
	if ball_side < 3000 && ball_side > 200 {
		Velocity = 70
		Direction = 0
		stop_traj = 1
		if side == 0 {
			//go to the left
			Direction = 90
		} else {
			//go to the right
			Direction = 270
		}
		coms.SendCommandToESP(coms.CMD_all, Velocity, Angular, Direction, 0, 0, 0)
	}
}

// Middle orientation PID constants
var kP = 0.8
var kI = 0.0
var kD = 0.0

// Middle orientation PID variables
var error = 0.0
var integral = 0.0
var last_error = 0.0

// Debug variables (Goalkeeper back to middle of the goal)
var back_middle = 0
var set_middle = 0
var stop_traj = 0

var bussola int

// Orient Goalkeeper and move the Goalkeeper back to middle after defence
func check_movement(dt float64) {
	// Check the distance moved by the goalkeeper
	_, delta_y = coms.GetDisplacement()
	y_movement += delta_y
	if set_middle == 1 {
		//Go back to middle
		if y_movement > 300 || y_movement < -300 {
			Velocity = 0
			Direction = 0
			coms.SendCommandToESP(coms.CMD_all, Velocity, Angular, Direction, 0, 0, 0)
			set_middle = 0
			stop_traj = 0
			y_movement = 0
		}
	}
	// Stop in the edge of the goal
	if y_movement > 700 || y_movement < -700 {
		Velocity = 0
		Direction = 0
		coms.SendCommandToESP(coms.CMD_all, Velocity, Angular, Direction, 0, 0, 0)
		back_middle = 1
		y_movement = 0
	}

	// Get the angle to the middle and orient the robot correctly using the PID
	bussola = coms.Get_bussola()
	error = float64(-bussola)
	pTerm := kP * error
	integral += error * dt
	iTerm := kI * integral
	dTerm := kD * ((error - last_error) / dt)
	last_error = error
	Angular = pTerm + iTerm + dTerm
	// Set a limit to the angle velocity
	if Angular > 30 {
		Angular = 30
	} else if Angular < -30 {
		Angular = -30
	}
	coms.SendCommandToESP(coms.CMD_all, Velocity, Angular, Direction, 0, 0, 0)
}

func obtain_lateral(ball_1x float64, ball_2x float64, dist1 float64, dist2 float64) (ball_side float64, side int) {
	//inicialize variables
	var horizontal_dist1 = 0.0
	var horizontal_dist2 = 0.0
	var vertical_dist1 = 0.0
	var vertical_dist2 = 0.0

	//obtain the horizontal distance of the balls to the center of the image (pixels)
	var dist_middle_1 = -((width / 2) - ball_1x)
	var dist_middle_2 = -((width / 2) - ball_2x)

	//obtain the angle between the balls and the center
	var horizontal_degrees_1 = dist_middle_1 * horizontal_cam / width
	var horizontal_degrees_2 = dist_middle_2 * horizontal_cam / width

	//obtain the horizontal distance between the ballls and the robot
	horizontal_dist1 = dist1 * math.Sin(horizontal_degrees_1*(math.Pi/180))
	horizontal_dist2 = dist2 * math.Sin(horizontal_degrees_2*(math.Pi/180))

	//obtain the vertical distance between the ballls and the robot
	vertical_dist1 = dist1 * math.Cos(horizontal_degrees_1*(math.Pi/180))
	vertical_dist2 = dist2 * math.Cos(horizontal_degrees_2*(math.Pi/180))

	//obtain the slope and the origin
	var m = (vertical_dist2 - vertical_dist1) / (horizontal_dist2 - horizontal_dist1)
	var b = vertical_dist1 - (m * horizontal_dist1)

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
	side = 1

	//if it is negative means is in the left side
	if ball_side < 0 {
		ball_side = -ball_side
		side = 0
	}
	return
}

var hsv = gocv.NewMat()
var mask = gocv.NewMat()

//var window = gocv.NewWindow("Orange Detection")

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
		if gocv.ContourArea(cnts.At(c)) > MinimumArea {
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

func GK_vision() {
	// Ball coordinates and distance of the two ball frames
	var cx1 = -1
	var cx2 = -1
	var cy1 = -1
	var cy2 = -1
	var dist1 = uint16(0)
	var dist2 = uint16(0)
	// Variables to the distance of the ball trajectory
	var ball_side = 0.0
	var side = 0
	var last_side = 0
	// Variable to the position of the ball on the goal image
	var position = 0.0

	var i = 0

	fmt.Println("-----------------------------------START-----------------------------------")
	// Inicialize the Omni at 0
	coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)

	//Connect kinect
	kinect_device.InitKinectContext()
	kinect_device.InitKinectDevice()
	kinect_device.StartCallbacks()

	// Open image of the ball detection
	var window1 = gocv.NewWindow("Detect Ball")
	var img gocv.Mat

	// Open image of the ball prediction in the goal
	var filename = "GK_vision/Images/goal.png"
	var window2 = gocv.NewWindow("Goal")
	var goal = gocv.IMRead(filename, gocv.IMReadColor)

	// Times for the PID calculations
	var current_time time.Time
	old_time := time.Now()

	// Inicialize endless cycle
	for {
		//Get the RGB frame
		img = kinect_device.GetRGBMat()
		if img.Empty() { //check if there is an image
			fmt.Printf("Failed to read image!\n")
		}

		//Save the previous coordinates and distance
		cx1 = cx2
		cy1 = cy2
		dist1 = dist2

		//Obtain the coordinates of the ball
		cx2, cy2 = detect_ball(img)

		//Get the distance if there is a ball
		if cx2 != -1 && cy2 != -1 {
			dist2 = kinect_device.Pixel_distance(cx2, cy2)
		}

		//Orientation to the ball
		//ball_orientation(cx2)

		// If the robot is moving, stop the trajectory prediction
		if stop_traj == 0 {
			//if the ball moved into the robot calculate the trajectory
			if cx1 != -1 && cy1 != -1 && cx2 != -1 && cy2 != -1 && dist2 < (dist1-200) && dist1 > 200 && dist2 > 200 {
				last_side = side
				// Returns wich side of the robot the ball is going and the distance
				ball_side, side = obtain_lateral(float64(cx1), float64(cx2), float64(dist1), float64(dist2))
				if ball_side < 200 {
					side = last_side
				}
				// Call the function to defend
				defend(ball_side, side)
			}
		}

		//Print a circle in the ball
		if cx2 != -1 && cy2 != -1 {
			gocv.Circle(&img, image.Pt(cx2, cy2), 20, color.RGBA{255, 0, 0, 255}, 5)
		}

		// Delay for the consecutive commands
		time.Sleep(10 * time.Millisecond)
		// Current time to PID
		current_time = time.Now()
		// Call movement function
		check_movement(float64(current_time.Sub(old_time).Seconds()))
		// Reset PID time
		old_time = current_time
		// Call the goalkeeper back to middle
		if back_middle == 1 {
			i++
			// This calculates 2 seconds, and after that make the robot go to the middle of the goal
			if i > 200 {
				i = 0
				back_middle = 0
				y_movement = 0
				set_middle = 1
				Velocity = 30
				Direction = 0
				if side == 0 {
					//go to the left
					Direction = 270
				} else {
					//go to the right
					Direction = 90
				}
				coms.SendCommandToESP(coms.CMD_all, Velocity, Angular, Direction, 0, 0, 0)
			}
		}
		//Print in the goal image the ball prediction
		if ball_side != 0 && dist2 < 100 {
			if side == 0 {
				if ball_side <= 1000 {
					position = (ball_side * 167 / 1000) + 233
					gocv.Circle(&goal, image.Pt(int(position), 190), 20, color.RGBA{255, 0, 0, 255}, 5)
				} else {
					gocv.Circle(&goal, image.Pt(450, 190), 20, color.RGBA{255, 0, 0, 255}, 5)
				}
			} else {
				if ball_side <= 1000 {
					position = 233 - (ball_side * 183 / 1000)
					gocv.Circle(&goal, image.Pt(int(position), 190), 20, color.RGBA{255, 0, 0, 255}, 5)
				} else {
					gocv.Circle(&goal, image.Pt(10, 190), 20, color.RGBA{255, 0, 0, 255}, 5)
				}
			}
			ball_side = 0
		}

		// Open the images windows
		window1.IMShow(img)
		window1.WaitKey(1)
		window2.IMShow(goal)
		window2.WaitKey(1)

	}
}
