package skills

/*
#include <stdlib.h>
#include <stdio.h>
u_int16_t get_byte_16(void *buf, int offset)
{
	return *((u_int16_t *)buf + offset);
}
*/
import "C"

import (
	"fmt"
	"image"
	"image/color"
	"math"
	"os"
	coms "player/communication"
	freenect "player/freenect"
	"runtime"
	"strconv"
	"strings"
	"time"
	"unsafe"

	"gocv.io/x/gocv"
)

// Minimum area to detect the ball
const MinimumArea = 100

// Angle of view of camera
const horizontal_cam = 62.5
const vertical_cam = 48.6
const no_vision_cam = 58.75
const vertical_cam_angle = 90

// Angle of view of depth camera
const horizontal_depth_cam = 58.5
const vertical_depth_cam = 46.6
const no_vision_depth_cam = 60.75

const img_width = 640
const img_height = 480

// Minium hsv values for ball filter
const min_h_ball = 4.0 //25.0
const min_s_ball = 115.0
const min_v_ball = 76.0

// Maxium hsv values for ball filter
const max_h_ball = 13.5 //65.0
const max_s_ball = 255.0
const max_v_ball = 255.0

// Minium hsv values for ball filter
const min_h_team = 12.0 //25.0
const min_s_team = 137.0
const min_v_team = 75.0

// Maxium hsv values for ball filter
const max_h_team = 25 //65.0
const max_s_team = 255.0
const max_v_team = 255.0

/*
// Minium hsv values for ball filter
var min_h_ball = 26.0
var min_s_ball = 40.0
var min_v_ball = 100.0

// Maxium hsv values for ball filter
var max_h_ball = 36.0
var max_s_ball = 255.0
var max_v_ball = 255.0
*/
type Pid struct {
	kP, kI, kD  float64
	dt          float64
	lastError   float64
	integral    float64
	outputLimit float64
}

type Atractor struct {
	Katracao     float64
	Kintensidade float64
	outputLimit  float64
}

type PID_gains struct {
	Kp float64
	Ki float64
	Kd float64
}

type position struct {
	Y     float64
	X     float64
	Angle float64
}

// var lower = gocv.NewMatWithSizeFromScalar(gocv.NewScalar(min_h_ball, min_s_ball, min_v_ball, 0.0), img_height, img_width, gocv.MatTypeCV8UC3)
// var upper = gocv.NewMatWithSizeFromScalar(gocv.NewScalar(max_h_ball, max_s_ball, max_v_ball, 0.0), img_height, img_width, gocv.MatTypeCV8UC3)
var lower_ball_mask = gocv.NewScalar(min_h_ball, min_s_ball, min_v_ball, 0.0)
var upper_ball_mask = gocv.NewScalar(max_h_ball, max_s_ball, max_v_ball, 0.0)
var lower_teamates_mask = gocv.NewScalar(min_h_team, min_s_team, min_v_team, 0.0)
var upper_teamates_mask = gocv.NewScalar(max_h_team, max_s_team, max_v_team, 0.0)

var kinect_device freenect.Kinect

// var freenect_device *freenect.FreenectDevice
var led_sleep_time time.Duration
var image_quality = 100
var freenect_device_present = false

var fns []func(args_ [7]int, quit chan int)

// var fns_chan [8]chan bool
var fns_chan = make([]chan int, 10)

var window3 = gocv.NewWindow("before dilated")

var window1 = gocv.NewWindow("befo ilated")

// var window = gocv.NewWindow("dilated")
var ball_flag bool
var Fns_args = make(chan [7]int, 10)
var kick_flag = false

func getCommandParameters(package_ string, args_ *[7]int) int {

	splittedString := strings.Split(package_, ", ")
	splittedString1 := strings.Split(splittedString[0], "[")
	//fmt.Println("\npackage_    ", package_)
	//fmt.Println("\nsplittedString    ", splittedString)
	idx_cmd, _ := strconv.Atoi(splittedString1[1])
	args_[0], _ = strconv.Atoi(splittedString[1])
	args_[1], _ = strconv.Atoi(splittedString[2])
	args_[2], _ = strconv.Atoi(splittedString[3])
	args_[3], _ = strconv.Atoi(splittedString[4])
	args_[4], _ = strconv.Atoi(splittedString[5])
	args_[5], _ = strconv.Atoi(splittedString[6])
	//fmt.Println(splittedString1[1], '\t', splittedString[1])
	/*fmt.Printf("%s,%s,%s,%s,%s\n", splittedString[1], splittedString[2],
		splittedString[3], splittedString[4], splittedString[5])
	fmt.Printf("%d,%d,%d\n", args_[0], args_[1], args_[2])*/
	return idx_cmd
}

func Skills(mode int) {
	var s uint8
	fmt.Println("Skills")
	//BS_channel := make(chan string)
	//var fns_args chan [7]int
	//	var command_index int
	//initKinectCamera(&kinect_device)
	kinect_device.InitKinectContext()

	kinect_device.InitKinectDevice()
	//kinect_device.SetAutoExposureOFF()
	kinect_device.StartCallbacks()
	fmt.Println("Press a key to resume  SetAutoExposureOFF()")
	//fmt.Scanf("%c", &s)
	//time.Sleep(5 * time.Second)
	fmt.Println("\n\n🎥️  Kinect stream initialized", s, mode)
	if mode == 0 {
		chan_quit := make(chan int)
		var args = [7]int{-1, -1, -1, -1, -1, -1, -1}
		fmt.Println("mode 0 in")
		//skMove2(args, chan_quit)
		//skAtack(args, chan_quit)

		skKick2(args, chan_quit)
		//skAtack2()
		//skReceive(args, chan_quit)
		//skRemoteControl()
		fmt.Println("mode 0 out")
	} else if mode == 1 {
		fns = append(fns, skStop)
		fns = append(fns, skMove)
		fns = append(fns, skAtack)
		fns = append(fns, skKick)
		fns = append(fns, skReceive)
		fns = append(fns, skCover)
		fns = append(fns, skDefend)
		fns = append(fns, skRemoteControl)

		chan_quit := make(chan int)

		var command string
		var args [7]int
		var last_state int

		first_time_running := true
		for {
			//time.Sleep(1 * time.Millisecond)
			//fmt.Println("wainting", coms.New_BS_command)

			if coms.New_BS_command {
				//fmt.Println("inicio")
				coms.New_BS_command = false
				coms.GetBS_Command(&command)
				//fmt.Print("BaseStation_cmd")
				//fmt.Println(command)
				command_index := getCommandParameters(command, &args)
				//	fmt.Println(command_index, last_state)
				if command_index < 8 {
					//fmt.Println("entrou", first_time_running)
					if last_state != command_index || first_time_running {
						if !first_time_running {
							chan_quit <- 0
						}
						//fmt.Println("entrou1")
						first_time_running = false
						go fns[command_index](args, chan_quit)
					} else {
						Fns_args <- args

						//fns_chan[command_index] <- false
						//fmt.Println("skill2345")
					}
					last_state = command_index
				} else {
					fmt.Println("skill command value out of range")
				}

			}
		}
	}
}

// NewPid creates a new PID controller with the given constants and dt
func NewPid(kP, kI, kD, dt, outputLimit float64) *Pid {
	return &Pid{
		kP:          kP,
		kI:          kI,
		kD:          kD,
		dt:          dt,
		outputLimit: outputLimit,
	}
}

// NewPid creates a new PID controller with the given constants and dt
func NewAtractor(Katracao, Kintensidade, outputLimit float64) *Atractor {
	return &Atractor{
		Katracao:     Katracao,
		Kintensidade: Kintensidade,
		outputLimit:  outputLimit,
	}
}

func (a *Atractor) Update(erro float64) float64 {
	output := a.Katracao * math.Exp(erro*a.Kintensidade)

	if output > a.outputLimit {
		output = a.outputLimit
	}

	return output
}

// Update computes the new control output based on the current error and elapsed time
func (p *Pid) Update(erro float64, dt float64) float64 {
	// Proportional term
	pTerm := p.kP * erro
	//fmt.Println("pTerm", pTerm)
	// Integral term
	p.integral += erro * dt
	iTerm := p.kI * p.integral

	// Derivative term
	dTerm := p.kD * (erro - p.lastError) / dt

	// Compute the output
	output := pTerm + iTerm + dTerm
	//fmt.Println("UPDATE:   ", erro, pTerm, iTerm, dTerm, dt)
	// Limit the output if necessary
	//fmt.Println("output_update", output)
	if output > p.outputLimit {
		output = p.outputLimit
	} else if output < -p.outputLimit {
		output = -p.outputLimit
	}
	if p.lastError*erro < 0 {
		p.CleanIntegral()
	}
	p.lastError = erro

	return output
}

func (p *Pid) CleanIntegral() bool {

	p.integral = 0
	return true
}
func skStop(args_ [7]int, quit chan int) {
	fmt.Println(" Stop")
	arg := args_
	vare := arg[0]
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
			time.Sleep(10 * time.Millisecond)
			fmt.Println("Stop....")
			coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)
		}
	}
}

func skCover(args_ [7]int, quit chan int) {
	arg := args_
	vare := arg[0]
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			fmt.Println("COVER")
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
		}
	}
}
func skDefend(args_ [7]int, quit chan int) {
	arg := args_
	vare := arg[0]
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
		}
	}
}

func skMove(args_ [7]int, quit chan int) {
	fmt.Println("skMove")
	X_dest, Y_dest := 571.0, 0.0
	speed_atractor := NewAtractor(0.19, 0.03, 100)
	//direction_atractor := NewAtractor(0.01, 0.13, 100)
	var robot coms.Robot_st
	var ball coms.Ball_st
	arg := args_
	vare := arg[0]
	var direcao float64
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
			coms.GetBallPosition(&ball)
			coms.GetRobot(0, &robot)
			/*fmt.Print(" X  ")
			fmt.Print(robot.Coords.X)
			fmt.Print("    Y  ")
			fmt.Print(robot.Coords.Y)
			*/
			//calculo do deslocamento angular em relacao a bola
			ang := math.Atan2((float64(Y_dest) - float64(robot.Coords.Y)), (float64(X_dest) - float64(robot.Coords.X)))
			ang = (ang * 180) / math.Pi

			dir := 0
			if ang < 0 {
				dir = 360 + int(ang)
			} else {
				dir = int(ang)
			}
			if dir < -180 {
				dir = (360 - dir)
			} else {
				dir = (dir)
			}
			fmt.Print("    dir  ")
			fmt.Print(dir)

			ang_obs := math.Atan2(float64(robot.Coords.Y)-(float64(ball.Coords.Y)), float64(robot.Coords.X)-(float64(ball.Coords.Y)))
			ang_obs = (ang_obs * 180) / math.Pi

			aux_obstacle := direcao - float64(ang_obs)
			fmt.Print("     aux_obstacle  ")
			fmt.Print(int(aux_obstacle))

			//direcao=120*math.Sin(aux_target/(18*math.Pi))

			direcao = float64(dir) - (0.4 * aux_obstacle * math.Exp(-(math.Pow(aux_obstacle, 2) / 2 * math.Pow(180, 2))))
			fmt.Print("     direcao  ")
			fmt.Print(int((0.4 * aux_obstacle * math.Exp(-(math.Pow(aux_obstacle, 2) / 2 * math.Pow(180, 2))))))

			//calculo do deslocamento ate a bola

			vel_a := (X_dest - robot.Coords.X) * (X_dest - robot.Coords.X)
			vel_b := (Y_dest - robot.Coords.Y) * (Y_dest - robot.Coords.Y)

			displacement := math.Sqrt(vel_a + vel_b)
			vel := speed_atractor.Update((displacement))

			/*
				//calculo do deslocamento ate a bola
				slope := 1.0
				dir_erro := math.Atan2(-600,600)
				aux_x := (float64(robot.Orientation) - dir_erro/2*90)
				direction := slope * (float64(robot.Orientation) - dir_erro) * math.Exp(aux_x)

				//direction = direction_atractor.Update(erro)
			*/
			fmt.Print("    dir  ")
			fmt.Print(dir)
			/*
				fmt.Print("     ori  ")
				fmt.Print(int(robot.Orientation)-dir)

				/*fmt.Print("     dir-ori  ")
				if robot.Orientation < -180{
					fmt.Print(dir+robot.Orientation-360)
				}else{
					fmt.Print(dir-robot.Orientation)
				}*/

			fmt.Print("     vel  ")
			fmt.Print(int(vel))
			/*fmt.Print("     d  ")
			fmt.Println(int(displacement))
			/*fmt.Print("     ang  ")
			fmt.Print(int(ang))
			fmt.Print("     direction  ")
			fmt.Println(int(direction))*/
			time.Sleep(1 * time.Second)
			fmt.Println()
		}
	}
}

func skMove2(args_ [7]int, quit chan int) {
	fmt.Println("skMove")
	X_dest, Y_dest := 600.0, 0.0

	//direction_atractor := NewAtractor(0.01, 0.13, 100)
	var robot coms.Robot_st
	var ball coms.Ball_st
	arg := args_
	vare := arg[0]
	var direcao float64
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
			coms.GetBallPosition(&ball)
			coms.GetRobot(0, &robot)
			/*fmt.Print(" X  ")
			fmt.Print(robot.Coords.X)
			fmt.Print("    Y  ")
			fmt.Print(robot.Coords.Y)
			*/
			//calculo do deslocamento angular em relacao a bola
			ang := math.Atan2(float64(robot.Coords.Y)-(float64(Y_dest)), (float64(robot.Coords.X) - float64(X_dest)))
			ang = (ang * 180) / math.Pi

			dir := 0.0

			if ang < 0 {
				dir = (180 + ang)
			} else {
				dir = (360 + ang - 180)
			}

			fmt.Print("dir  ")
			fmt.Print(int(dir))

			ang_obs := math.Atan2(float64(robot.Coords.Y)-(float64(ball.Coords.Y)), float64(robot.Coords.X)-(float64(ball.Coords.X)))

			ang_obs = (ang_obs * 180) / math.Pi

			if ang_obs < 0 {
				ang_obs = 360 + ang_obs
			}
			if ang < 0 {
				ang = 360 + ang
			}
			aux_obstacle := ang - float64(ang_obs)

			direcao = dir + (1.8 * aux_obstacle * math.Exp(-((aux_obstacle * aux_obstacle) / (35 * 35))))

			if direcao < 0 {
				direcao = 360 + direcao
			}
			if direcao > 360 {
				direcao = direcao - 360
			}
			fmt.Print("     ang  ")
			fmt.Print(int(ang))
			fmt.Print("     ang_obs  ")
			fmt.Print(int(ang_obs))
			fmt.Print("     aux_obs  ")
			fmt.Print(int(aux_obstacle))
			fmt.Print("  direcao ")
			fmt.Print(int(direcao))

			fmt.Print("  ")
			fmt.Print(int((1.8 * aux_obstacle * math.Exp(-((aux_obstacle * aux_obstacle) / (35 * 35))))))

			time.Sleep(1 * time.Second)
			fmt.Println()
		}
	}
}

func skKick(args_ [7]int, quit chan int) {
	arg := args_
	vare := arg[0]
	var rgb_frame gocv.Mat
	var teammate position

	var rot, rot_aux, last_rot int
	//var rot2 int
	//input: deslocamento dos pixeis em x
	ori_pid_kinect := NewPid(0.020, 0.01, 0.009, 0.05, 40)
	ori_pid_omnivs := NewPid(0.25, 0.0, 0.1, 0.05, 20)

	//atractor_kinect := NewAtractor(0.19, 0.03, 60)
	//input: deslocamento angular do robot a bola
	old_time := time.Now()
	teammate.X = -1
	teammate.Y = -1
	kick_flag = true
	var i_robot coms.Robot_st
	var DB coms.LocalDB
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}

			rgb_frame = kinect_device.GetRGBMat()
			teammate.detectTeam(rgb_frame)
			fmt.Println("X  ", teammate.X, "Y  ", teammate.Y)
			//depth_array, _ := kinect.RawDepthFrame(4)
			if teammate.X != -1 && teammate.Y != -1 {
				//process the image from kinect
				//atctivate the ball flag possession
				current_time := time.Now()
				fmt.Println("\ntime lap  ", float64(current_time.Sub(old_time).Seconds()))
				//angulo := getAngle(teammate.X, teammate.Y, float64(distance))

				rot_aux = ori_pid_kinect.sk_orientation2(float64(current_time.Sub(old_time).Seconds()), teammate)

				rot = int(1*float64(rot_aux) + 0*float64(last_rot))
				old_time = current_time
				last_rot = rot_aux

				fmt.Println("teammate{Y,X}", teammate, " rotational  ", -rot)
				if teammate.X > 310 && teammate.X < 330 {
					coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 5)
					return
				}

				coms.SendCommandToESP(coms.CMD_all, 0, -rot, 0, 0, 0, 0)

			} else {
				ori_pid_omnivs.CleanIntegral()
				coms.GetRobot(0, &i_robot)
				coms.GetDatabase(&DB)
				//contolo da velocidade angular
				current_time := time.Now()
				//	fmt.Println("\ntime lap  ", float64(current_time.Sub(old_time).Milliseconds()))
				//rot2 = int(ori_pid_omnivs.Update(float64(DB.Team[1].Angle), float64(current_time.Sub(old_time).Seconds())))
				old_time = current_time
				//fmt.Println(" \nang  \n", DB, "\n   rot2   ", int(rot2))

				//fmt.Println(DB)
				coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)
			}
			time.Sleep(10 * time.Millisecond)

		}
	}
}
func skKick2(args_ [7]int, quit chan int) {
	arg := args_
	vare := arg[0]
	var rgb_frame gocv.Mat
	var target position

	var rot, rot2 int
	//input: deslocamento dos pixeis em x
	ori_pid_kinect := NewPid(0.1, 0.0, 0.0, 0.05, 40)
	ori_pid_omnivs := NewPid(0.25, 0.0, 0.1, 0.05, 20)
	/*
		ori_pid_kinect := NewPid(0.020, 0.01, 0.009, 0.05, 40)
		ori_pid_omnivs := NewPid(0.25, 0.0, 0.1, 0.05, 20)
	*/
	//input: deslocamento angular do robot a bola
	target.X = -1
	target.Y = -1
	kick_flag = true
	var i_robot coms.Robot_st
	var DB coms.LocalDB
	var current_time, old_time time.Time

	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}

			rgb_frame = kinect_device.GetRGBMat()
			target.detectBall(rgb_frame)
			//depth_array, _ := kinect.RawDepthFrame(4)
			if target.X != -1 && target.Y != -1 {
				//process the image from kinect
				old_time = current_time
				current_time = time.Now()
				//fmt.Println("\ntime lap  ", float64(current_time.Sub(old_time).Seconds()))
				target.Angle = getAngleRelativeToRobot(target.X, target.Y, 10)
				rot = int(ori_pid_kinect.Update(target.Angle, float64(current_time.Sub(old_time).Seconds())))

				fmt.Println("\ntarget", target.X, target.Y)
				fmt.Println("\ntarget", target.Angle)
				fmt.Println("rotational  ", -rot)
				/*if teammate.X > 310 && teammate.X < 330 {
					coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 5)
					return
				}*/
				//coms.SendCommandToESP(coms.CMD_all, 0, -rot, 0, 0, 0, 0)

			} else {
				ori_pid_kinect.CleanIntegral()
				coms.GetRobot(0, &i_robot)
				//coms.GetDatabase(&DB)
				//contolo da velocidade angular
				current_time := time.Now()
				//	fmt.Println("\ntime lap  ", float64(current_time.Sub(old_time).Milliseconds()))
				rot2 = int(ori_pid_omnivs.Update(float64(DB.Team[1].Angle), float64(current_time.Sub(old_time).Seconds())))
				old_time = current_time
				fmt.Println("\n   rot2   ", int(rot2))

				coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 0, 0, 0)
			}
			time.Sleep(10 * time.Millisecond)

		}
	}
}
func skRemoteControl(args_ [7]int, quit chan int) { //args_ [7]int
	//rot, ori_aux, dir_aux := 0, 0, 0
	fmt.Println("RemoteControl")
	rot := 0
	data_st := new(coms.MsiToEsp)
	var dx, dy int //ori
	arg := args_
	vare := arg[0]
	//var flg bool
	for { //flg= <- fns_chan[7]       args_ := range Fns_args

		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
			//fmt.Println(len(fns_chan[7]))

			/*if <-fns_chan[7] {
				return
			}*/
			//fmt.Println(args_)
			dx = args_[1]
			dy = args_[0]
			rot = args_[2]
			kick := args_[3]
			dir_atual := coms.Get_bussola()
			var vel, dir float64

			ang := math.Atan2(float64(dy), float64(dx))
			//fmt.Println("ang", ang, "   dx", dx, "dy   ", dy)

			//vel = float64(dy) / math.Sin(ang)
			dx2 := float64((dx * dx))
			dy2 := float64((dy * dy))
			vel = math.Sqrt(dx2 + dy2)
			///fmt.Println(dx, '\t', dy, '\t', vel)
			dir = ((ang * 180) / math.Pi) - float64(dir_atual)

			if dir < 0 {
				//fmt.Println("dirasasa", 360+dir)
				dir = dir + 360
			}
			kick = kick * 7

			/*fmt.Print("vel: ")
			fmt.Print(vel)
			fmt.Print("   dir: ")
			fmt.Print(dir)
			fmt.Print("   rot: ")
			fmt.Print(rot)
			fmt.Print("   Kick: ")
			fmt.Println(kick)
			*/
			data_st.Velocity = int(vel)
			data_st.Angular = int(rot)
			data_st.Direction = int(dir)
			data_st.KickTime = int(kick)
			//coms.SendCommandToESP(coms.CMD_all, data_st.Velocity, data_st.Angular, data_st.Direction, 0, 0, 0)
		}
	}
}

func (pid *Pid) sk_orientation(time_ float64, ball_pos2 position) int {
	fmt.Println("Orientation2")
	//ori_pid_kinect := NewPid(0.045, 0.035, 0.015, 0.05, 80)

	if ball_pos2.X != -1 {

		erro := float64(ball_pos2.X - 320)
		if erro < 3 && erro > -3 && !kick_flag {
			erro = 0
		}
		rot := pid.Update(erro, time_)
		fmt.Println(" \nerro:  ", erro)

		return int(rot)
	}
	return 0
}
func (pid *Pid) sk_orientation2(time_ float64, ball_pos2 position) int {
	fmt.Println("Orientation2")
	//ori_pid_kinect := NewPid(0.045, 0.035, 0.015, 0.05, 80)

	if ball_pos2.X != -1 {

		erro := float64(ball_pos2.X - 320)
		if erro < 3 && erro > -3 && !kick_flag {
			erro = 0
		}
		rot := pid.Update(erro, time_)
		fmt.Println(" \nerro:  ", erro)

		return int(rot)
	}
	return 0
}
func PrintMemUsage() {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	// For info on each, see: https://golang.org/pkg/runtime/#MemStats
	fmt.Printf("Alloc = %v MiB", bToMb(m.Alloc))
	fmt.Printf("\tTotalAlloc = %v MiB", bToMb(m.TotalAlloc))
	fmt.Printf("\tSys = %v MiB", bToMb(m.Sys))
	fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

func bToMb(b uint64) uint64 {
	return b / 1024 / 1024
}
func skAtack(args_ [7]int, quit chan int) {
	fmt.Println("skAtack")
	Katracao := 2.0
	Kintensidade := 3.8
	arg := args_
	vare := arg[0]
	fmt.Println("initKinectCamera!")
	var ball_pos2 position

	var rot, rot2 int
	//input: deslocamento dos pixeis em x
	ori_pid_kinect := NewPid(0.02, 0.005, 0.02, 0.05, 20)
	//atractor_kinect := NewAtractor(0.19, 0.03, 60)
	atractor_kinect := NewAtractor(1.9, 0.010, 25)
	//input: deslocamento angular do robot a bola
	ori_pid_omnivs := NewPid(0.25, 0.0, 0.1, 0.05, 20)
	old_time := time.Now()
	var current_time time.Time
	ball_pos2.X = -1
	ball_pos2.Y = -1
	var rgb_frame gocv.Mat
	var erro float64

	var vel float64

	var i_robot coms.Robot_st
	var ball coms.Ball_st

	var my_pos position
	var ball_pos position
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return

		default:

			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}
			rgb_frame = kinect_device.GetRGBMat()

			if !rgb_frame.Empty() {
				//fmt.Println("Image is empty!")

				ball_pos2.detectBall(rgb_frame)
				/*if ball_pos2.Y > 400 && ball_pos2.X > 250 && ball_pos2.X < 390 {
					fmt.Print("ball_X")
					fmt.Print(ball_pos2.X)
					fmt.Print("ball_Y")
					fmt.Println(ball_pos2.Y)
					coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, dribbler1, dribler2, 0)
					fmt.Println("----------OUT OF ATACK-----------------------OUT OF ATACK--------------------OUT OF ATACK-----------:")
					//return
				}*/
				//depth_array, _ := kinect.RawDepthFrame(4)
				if ball_pos2.X != -1 && ball_pos2.Y != -1 {
					//process the image from kinect
					//atctivate the ball flag possession
					fmt.Println("\nball_X", ball_pos2.X, "ball_Y", ball_pos2.Y)

					erro = float64(480 - ball_pos2.Y)

					vel = atractor_kinect.Update(erro)

					old_time = current_time
					current_time = time.Now()
					angle := getAngleRelativeToRobot(ball_pos2.X, ball_pos2.Y, 0)
					rot = int(ori_pid_kinect.Update(angle, float64(current_time.Sub(old_time).Seconds())))

					fmt.Println("angle ", angle, " rotational  ", -rot)

					fmt.Println("erro", erro, " velocity ", vel)

					//coms.SendCommandToESP(coms.CMD_all, vel, -rot, 0, dribbler1, dribler2, 0)

				} else {
					ori_pid_kinect.CleanIntegral()
					coms.GetRobot(0, &i_robot)
					//robot_ori := i_robot.Orientation
					my_pos.X = i_robot.Coords.X
					my_pos.Y = i_robot.Coords.Y

					coms.GetBallPosition(&ball)
					//ball_pos.X = ball.Coords.X
					///ball_pos.Y = ball.Coords.Y
					fmt.Println("\nmy_pos", int(ball_pos.X), int(ball_pos.Y))

					//calculo do deslocamento angular em relacao a bola
					/*ang := math.Atan2((float64(ball_pos.Y)-float64(my_pos.Y)), (float64(ball_pos.X)-float64(my_pos.X))) * 180 / math.Pi
					if ang < 0 {
						ang = 360 + ang
					}
					if robot_ori < 0 {
						robot_ori = 360 + robot_ori
					}
					dif := ang - float64(robot_ori)*/
					//calculo do deslocamento ate a bola
					//erro := float64((ball_pos.X - my_pos.X) / int(math.Sin(ang)))
					a2 := (ball_pos.X - my_pos.X) * (ball_pos.X - my_pos.X)
					b2 := +(ball_pos.Y - my_pos.Y) * (ball_pos.Y - my_pos.Y)
					erro := math.Sqrt(float64(a2 + b2))

					//contolo da velocidade angular
					vel := Katracao * math.Exp(erro*Kintensidade)
					current_time := time.Now()
					//	fmt.Println("\ntime lap  ", float64(current_time.Sub(old_time).Milliseconds()))
					rot2 = int(ori_pid_omnivs.Update(float64(ball.Z), float64(current_time.Sub(old_time).Seconds())))
					old_time = current_time
					fmt.Println(" \nang  ", int(ball.Z), "   rot2   ", int(rot2))
					fmt.Println("erro  ", int(erro), "   vel   ", vel)
					fmt.Println()
					//coms.SendCommandToESP(coms.CMD_all, 0, rot2, 0, 0, 0, 0)
				}
				time.Sleep(10 * time.Millisecond)
			}
		}
	}
}

func skAtack2() {
	//kLinear := 1.0
	//kRotational := 1.0
	fmt.Println("sk_atack2")

	//old_time := time.Now()
	fmt.Println("antes do for")

	var ball_pos2 position

	//var rot int
	//input: deslocamento dos pixeis em x
	//ori_pid_kinect := NewPid(0.03, 0.035, 0.008, 0.05, 80)

	//input: deslocamento angular do robot a bola
	//ori_pid_omnivs := NewPid(0.03, 0.035, 0.008, 0.05, 80)
	//old_time := time.Now()
	ball_pos2.X = -1
	ball_pos2.Y = -1
	var rgb_frame gocv.Mat
	//current_time := time.Now()
	for {

		rgb_frame = kinect_device.GetRGBMat()
		if !rgb_frame.Empty() {
			window3.IMShow(rgb_frame)
			window3.WaitKey(1)

			ball_pos2.detectBall(rgb_frame)

			//depth_array, _ := kinect.RawDepthFrame(4)

			if ball_pos2.X != -1 && ball_pos2.Y != -1 {
				//process the image from kinect
				//atctivate the ball flag possession
				fmt.Print("ball_pos2   ")
				fmt.Println(ball_pos2)
			}
		} //fmt.Println("\ntime lap  ", float64(current_time.Sub(time.Now()).Milliseconds()), '\n')
		//current_time = time.Now()

	}
}

func skReceive(args_ [7]int, quit chan int) {
	fmt.Println("skReceive")

	//var rgb_frame gocv.Mat
	var kinect_ball_pos position
	rgb_frame := gocv.NewMat()
	var depth_array unsafe.Pointer
	fmt.Println("ENTROU RECEI#           ")

	mov_pid := NewPid(0.2, 0.009, 0.0, 0.05, 50)         //NewPid(4, 0.0003, 0.5, 0.05, 100)
	ori_pid_kinect := NewPid(0.4, 0.005, 0.0, 0.05, 100) //NewPid(0.2, 0.3, 0.2, 0.05, 100)

	var vel float64
	//var current_time time.Time
	current_time := time.Now()
	old_time := time.Now()
	dir := 0
	dir++
	dir-- // ??
	arg := args_
	vare := arg[0]
	var rot int
	//input: deslocamento dos pixeis em x
	var ball_pos coms.Ball_st
	//var previous_position coms.Ball_st
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			return
		default:
			for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}

			rgb_frame = kinect_device.GetRGBMat()
			if !rgb_frame.Empty() {
				//fmt.Println("Image is empty!")
				depth_array = kinect_device.GetDepthArray()

				kinect_ball_pos.detectBall(rgb_frame)
				if kinect_ball_pos.X != -1 && kinect_ball_pos.Y != -1 && depth_array != nil {
					//previous_position = ball_pos
					coms.GetBallPosition(&ball_pos)

					ball_depth := uint16(C.get_byte_16(depth_array, C.int(kinect_ball_pos.Y*640+kinect_ball_pos.X)))
					angular_disp := getAngleRelativeToRobot(kinect_ball_pos.X, kinect_ball_pos.Y, 10)
					//angular_disp := getAngleRelativeToField(previous_position.Coords.X, previous_position.Coords.Y, ball_pos.Coords.X, ball_pos.Coords.Y)

					old_time = current_time
					current_time = time.Now()
					vel = mov_pid.Update((kinect_ball_pos.X)-310, float64(current_time.Sub(old_time).Seconds()))
					rot = int(ori_pid_kinect.Update(angular_disp, float64(current_time.Sub(old_time).Seconds())))

					if (kinect_ball_pos.X)-310 > 0 {
						dir = 90
					} else {
						dir = 270
					}
					if vel < 0 {
						vel = -vel
					}
					fmt.Println("\n\nball_position", kinect_ball_pos.X, kinect_ball_pos.Y)
					//fmt.Println(ball_pos2.X, ball_pos2.Y)
					fmt.Println("ball angle", angular_disp)
					fmt.Println("ball_depth", ball_depth)
					fmt.Println("vel", vel)
					fmt.Println("dir", dir)
					fmt.Println("rot", rot)
					coms.SendCommandToESP(coms.CMD_all, int(vel), int(rot), int(dir), 50, 50, 0)

				} else {
					coms.SendCommandToESP(coms.CMD_all, int(0), int(0), int(0), 0, 0, 0)
				}
				time.Sleep(10 * time.Millisecond)
			}
		}
	}
}

func getAngleRelativeToRobot(objectX float64, objectY float64, depthMM float64) float64 {

	angle_per_pixel := 0.0890625
	// Calculate angle in the horizontal plane
	var angle_ float64
	pixel_distance := objectX - 295
	if pixel_distance > 0 {
		angle_ = float64(pixel_distance) * angle_per_pixel

	} else {
		angle_ = float64(-pixel_distance) * angle_per_pixel
		angle_ = -angle_
	}
	//fmt.Println("angle_per_pixel", angle_per_pixel, " pixel_distance", pixel_distance)

	//fmt.Println("Pixel", objectX, objectY, " corresponds to an angle of", angle_)
	return angle_
}
func getAngleRelativeToField(previousX float64, previousY float64, objectX float64, objectY float64) float64 {

	var angle_ float64

	angle_ = math.Atan2((objectY - previousY), (objectX - previousX))

	return angle_
}
func (sp *position) calculateVelocity(centroid image.Point, prevCentroid image.Point, prevTime float64) {
	// Initialize the velocity in the X and Y directions to 0

	// Check if we have a previous centroid
	if prevCentroid.X >= 0 && prevCentroid.Y >= 0 {
		// Calculate the distance in the X and Y directions between the previous and current centroids
		distanceX := centroid.X - prevCentroid.X
		distanceY := centroid.Y - prevCentroid.Y

		// Calculate the time between the previous and current frames
		//currentTime := gocv.GetTickCount()
		timeDiff := prevTime //(currentTime - prevTime) / float64(gocv.GetTickFrequency())

		// Calculate the velocity in the X and Y directions based on the distance and time
		sp.X = float64(distanceX) / timeDiff
		sp.Y = float64(distanceY) / timeDiff
	}

}
func obtain_lateral(ball_1x float64, ball_2x float64, dist1 float64, dist2 float64) (ball_side float64, side int, ori float64) {
	var horizontal_dist1 = 0.0
	var horizontal_dist2 = 0.0

	//obtain the horizontal distance of the balls to the center of the image (pixels)
	dist_middle_1 := -((img_width / 2) - ball_1x)
	dist_middle_2 := -((img_width / 2) - ball_2x)

	//obtain the angle between the balls and the center
	horizontal_degrees_1 := dist_middle_1 * horizontal_cam / img_width
	horizontal_degrees_2 := dist_middle_2 * horizontal_cam / img_width

	//obtain the horizontal distance between the ballls and the robot
	horizontal_dist1 = dist1 * math.Tan(horizontal_degrees_1*(math.Pi/180))
	horizontal_dist2 = dist2 * math.Tan(horizontal_degrees_2*(math.Pi/180))

	/*fmt.Printf("Horizontal distance 1: ")
	fmt.Println(horizontal_dist1)
	fmt.Printf("Horizontal distance 2: ")
	fmt.Println(horizontal_dist2)
	*/
	//obtain the slope and the origin
	m := (dist2 - dist1) / (horizontal_dist2 - horizontal_dist1)
	b := dist1 - (m * horizontal_dist1)

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

	fmt.Printf("Declive: ")
	fmt.Println(m)
	fmt.Printf("Origem: ")
	fmt.Println(b)

	//Obtain the predicted location of the ball
	ball_side = -(b / m)
	side = 1
	ori = m
	/*fmt.Printf("Ball side: ")
	fmt.Println(ball_side)
	*/
	//if it is negative means is in the left side
	if ball_side < 0 {
		ball_side = -ball_side
		side = 0
	}

	//drawPlan(int(horizontal_dist1), int(horizontal_dist2), int(dist1), int(dist2), m)
	return
}

var hsv = gocv.NewMat()
var mask = gocv.NewMat()

var cx = -1
var cy = -1
var kernel gocv.Mat

func (pos *position) detectBall(img gocv.Mat) {

	pos.X = -1
	pos.Y = -1

	if img.Empty() {
		fmt.Printf("Failed to read image: \n")
		os.Exit(1)
	}
	if img.Channels() == 3 {
		gocv.CvtColor(img, &hsv, gocv.ColorBGRToHSV)
		//window1.IMShow(img)
		//window1.WaitKey(1)
		gocv.InRangeWithScalar(hsv, lower_ball_mask, upper_ball_mask, &mask)
		window1.IMShow(img)
		window1.WaitKey(1)
		var kernel = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(6, 6))
		gocv.Erode(mask, &mask, kernel)
		//kernel.Close()
		kernel = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(17, 17))
		gocv.Dilate(mask, &mask, kernel)
		//kernel.Close()
		/*window.IMShow(img)
		window.WaitKey(1)*/

		cnts := gocv.FindContours(mask, gocv.RetrievalExternal, gocv.ChainApproxNone)

		ball_flag = false
		var c int
		for c = 0; c < cnts.Size(); c++ {
			//fmt.Println("area", c, gocv.ContourArea(cnts.At(c)))
			if gocv.ContourArea(cnts.At(c)) > 600 {
				//fmt.Println("BOLA--------------------------|!!!!!")
				//cnt := cnts.At(c)
				var M = gocv.Moments(mask, false)

				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])
				gocv.Circle(&img, image.Pt(cx, cy), 4, color.RGBA{255, 0, 0, 0}, 4)
				ball_flag = true

			}
		}
		window3.IMShow(mask)
		window3.WaitKey(1)
		if ball_flag {
			pos.X = float64(cx)
			pos.Y = float64(cy)
		}
		cnts.Close()
	}

}
func (pos *position) detectTeam(img gocv.Mat) {

	pos.X = -1
	pos.Y = -1

	if img.Empty() {
		fmt.Printf("Failed to read image: \n")
		os.Exit(1)
	}
	if img.Channels() == 3 {
		//gocv.CvtColor(img, &img, gocv.ColorBGRToRGB)
		gocv.CvtColor(img, &hsv, gocv.ColorRGBToHSV)

		gocv.InRangeWithScalar(hsv, lower_teamates_mask, upper_teamates_mask, &mask)

		var kernel = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(1, 1))
		gocv.Erode(mask, &mask, kernel)
		kernel.Close()
		gocv.Line(&img, image.Pt(320, 0), image.Pt(320, 480), color.RGBA{255, 0, 0, 0}, 2)
		window1.IMShow(mask)
		window1.WaitKey(1)

		cnts := gocv.FindContours(mask, gocv.RetrievalExternal, gocv.ChainApproxNone)

		ball_flag = false
		var c int
		for c = 0; c < cnts.Size(); c++ {
			fmt.Println("area", c, gocv.ContourArea(cnts.At(c)))
			if gocv.ContourArea(cnts.At(c)) > 1000 {
				//fmt.Println("BOLA--------------------------|!!!!!")
				//cnt := cnts.At(c)
				var M = gocv.Moments(mask, false)

				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])
				ball_flag = true
				gocv.Circle(&img, image.Pt(cx+200, cy), 4, color.RGBA{255, 0, 0, 0}, 4)
			}
		}
		if ball_flag {
			pos.X = float64(cx)
			pos.Y = float64(cy)
		}
		window3.IMShow(img)
		window3.WaitKey(1)
		cnts.Close()
	}

}
func calculateDribblers(pos position) {
	cx := pos.X
	cy := pos.Y
	kp := 17.0
	//ki := 0.2
	erro := 411 - cy
	driblers_vel := (erro * kp) //+ float64(erro)*ki)
	balance := (cx * 100) / 580

	fmt.Print("    balance    ")
	fmt.Printf("%f\n", balance)

	db_v1 := float64((driblers_vel * (100 - balance)) / 50)
	db_v2 := float64((driblers_vel * balance) / 50)
	if db_v1 > 300 {
		db_v1 = 300
	}
	if db_v2 > 300 {
		db_v2 = 300
	}
	fmt.Printf("db_v1  %f    db_v2  %f \n ", db_v1, db_v2)
	//coms.SendCommandToESP(coms.CMD_omni_speed, 0, 0, 0)
	coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, db_v2, db_v1, 0)

}
