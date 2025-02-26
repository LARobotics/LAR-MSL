package skills

import (
	"context"
	"fmt"
	"math"
	coms "player/communication"
	"player/pb"
	"time"
)

/*
**
*************Move*************

Command: 1 X Y Ori Ox Oy

X -> target x coordinate
Y -> target y coordinate
Ori -> pass(0) or kick(0)
Ox -> Previous displacement on x Axis
Oy -> Previous displacement on y Axis

*************Move*************
**
*/

var move_orientation = NewPid(Kp_move, Ki_move, Kd_move, 0.0, outputLimit_PID_move)
var speed_atractor = NewAtractor(Katracao_move, Kintensidade_move, outputLimit_atractor_move)
var direction_reppeler = NewReppeller(Krepulsao_move, Kinfluencia_move, outputLimit_reppeller_move)

//var ball_as_repeller int

func skMove(args_ [7]int, quit chan int) {
	fmt.Println("skMove")

	//direction_atractor := NewAtractor(0.01, 0.13, 100)
	var db coms.LocalDB
	arg := args_
	//vare := arg[0]
	//var direcao float64
	//index := 0

	current_time := time.Now()
	old_time := current_time
	var elapsed_time float64
	//ori_pid_omnivs := NewPid(0.2, 0.0, 0.0, 0.05, 20)
	var ball_pos position

	//client := pb.NewYolo_KinectClient(conn)
	enable_drbblers := 0
	//var move_last_time time.Time
	//var move_time_now time.Time
	//reduction_gain := 0.2
	var ball_detected bool
	fmt.Println("Entrou2jjjhhjh", ball_detected)

	req = pb.Request{
		Check: true,
	}

	for {
		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return
		default:

			/*for len(Fns_args) > 0 && vare != -2 {
				arg = <-Fns_args
				//fmt.Println("ARGS        :", arg, idx)
			}*/
			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()

			//fmt.Println("move")

			coms.GetDatabase(&db)
			//fmt.Println("__________MOVE")
			X_target := arg[0]
			Y_target := arg[1]
			X_target_ori := arg[3]
			Y_target_ori := arg[4]
			ball_as_repeller := arg[5]
//			ball_reppele2:=arg[6]
			// If arg equal to 0, orientation target set to ball position
			if arg[2] == 0 {
				X_target_ori = int(db.Ball.Coords.X) //arg[3]
				Y_target_ori = int(db.Ball.Coords.Y) //arg[4]
			}

			// fmt.Println("__________MOVE22")
			resp, err := client.Send_Kinect(context.Background(), &req)
			//fmt.Println("__________MOVEndhbaerjna")
			ball_detected = false
			//move_time_now = time.Now()
			if err == nil && resp.Objects != nil {
				for idx, OBJ := range resp.Objects {
					if OBJ.Id == 0 {
						ball_detected = true
						ball_pos.X = float64(OBJ.X)
						ball_pos.Y = float64(OBJ.Y)
						fmt.Println("idx", idx)
						break
					}
				}
			}
			//fmt.Println("__________MOVE33")
			//fmt.Println("\ntime lap Basestation communication ", float64(time_now.Sub(last_time).Milliseconds()))
			//delta_cicle_coms = float64(time_now.Sub(last_time).Milliseconds())

			fmt.Println(elapsed_time)
			fmt.Println(db.Team != nil)

			current_time = time.Now()
			elapsed_time = float64(current_time.Sub(old_time).Milliseconds())
			fmt.Println("................................ball_as_repeller", ball_as_repeller,)
			if db.Team != nil { //&& float64(time_now.Sub(last_time).Milliseconds()) > S_TIMEOUT
				//last_time = time_now
				old_time = current_time
				//move_time_now = time.Now()

				ang_target := math.Atan2(float64(Y_target)-float64(db.Team[0].Coords.Y), (float64(X_target))-float64(db.Team[0].Coords.X))
				//fmt.Println("\nang_target first", ang_target*180/3.14)
				angle := math.Atan2(float64(Y_target_ori)-db.Team[0].Coords.Y, float64(X_target_ori)-db.Team[0].Coords.X)
				// angle := math.Atan2(db.Ball.Coords.Y-db.Team[0].Coords.Y, db.Ball.Coords.X-db.Team[0].Coords.X)
				erro := int(angle*180/math.Pi) - db.Team[0].Orientation
				//fmt.Println("erro", erro)

				for erro > 180 {
					erro -= 360
				}
				for erro < -180 {
					erro += 360
				}

				//process the image from kinect

				rot := int(move_orientation.Update(float64(erro), elapsed_time))

				fmt.Println("\nY_target_ori", Y_target_ori, "X_target_orY", X_target_ori, "\n")
				fmt.Println("Y_target", Y_target, "X_target", X_target, "ang_target", ang_target, "erro", erro)

				displacement := (math.Sqrt(math.Pow(float64(Y_target)-float64(db.Team[0].Coords.Y), 2) + math.Pow(float64(X_target)-float64(db.Team[0].Coords.X), 2)))

				vel := speed_atractor.Update((displacement))

				//if the robot have tha ball
				/*if vel > 50 && coms.GetBallStatus() < 3 {
					rot = rot / 3
				}*/
				/*else if coms.GetBallStatus() == 3 {
					//if the robot does not have the ball
					vel = 0
				}*/

				direction := int((((ang_target * 180) / 3.14) - float64(db.Team[0].Orientation))) //- db.Team[0].Orientation
				//fmt.Println("-direction antes", direction)
				if direction < -180 {
					direction = 180 - (-direction - 180)
					//fmt.Println("-direction-180", direction)
					//fmt.Println("ENTERI----------------ENTERI--------------ENTERI")
				}

				if direction > 180 {
					direction = -180 + (direction - 180)
					//fmt.Println("direction-180", direction)
					//fmt.Println("ENTERI----------------ENTERI--------------ENTERI")
				}

				/*if rot > 0 {
					direction=(8*direction/10)
				}else if rot < 0{
					direction=(12*direction/10)
				}*/

				//fmt.Println("-direction depois", direction)
				obstacles := db.Team

				obstacles = append(obstacles, db.Opponent...)
				if ball_as_repeller == 1 {
					fmt.Println("BALL_AS_REPELLER")
					obstacles[0].Angle = db.Ball.Angle
					obstacles[0].Distance = db.Ball.Dist
					//vel=25
				} else {
					obstacles = obstacles[1:]
					//speed_atractor.outputLimit = 100
				}
				direction = direction_reppeler.Update(obstacles, int(displacement), direction)
				/*
					if (rot!=0 && vel!=0){
						prev_dir:=direction
						direction+=(rot/100)*direction
						fmt.Println("rot",rot,"dir",direction,"prev dir ",prev_dir)
					}*/
				/*if vel > 50{
					rot=8
				}*/

				if direction < 0 {
					direction += 360
				}
				/*
					if rot < 0 {
						vel = vel + (reduction_gain * float64(rot))
					} else {
						vel = vel - (reduction_gain * float64(rot))
					}*/
				//Get mode to run skill
				//If arg equal to 1, limit speed to 30
				if ball_as_repeller == 1 {
					//speed_atractor.outputLimit = 15
vel=20
fmt.Println(".............hbvgcfyxdttcyvuinoohbvgcf.......")					
/*if vel<5{
						rot=0
					}*/
				} else {
					speed_atractor.outputLimit = outputLimit_atractor_move
				}
				if coms.GetBallStatus() != 3 {
					enable_drbblers = 0
				} else {
					enable_drbblers = 1
				}
				// fmt.Println("ang_obs\n", ang_obs)
				fmt.Println("direction  ", direction, "  displacement  ", displacement, "ball_as_reppeler",ball_as_repeller)
				fmt.Println("rot", rot, "vel", vel)

				coms.SendCommandToESP(coms.CMD_all, int(vel), int(rot), int(direction), enable_drbblers, 0)
				/*if ball_detected {
					ball_angle := int(getAngleRelativeToRobot(ball_pos.X, ball_pos.Y, 0))
					fmt.Println("OrbitarBola", OrbitarBola(1, ball_angle))
				}*/
				//fmt.Println("loop time", elapsed_time)
				coms.SetLoopTime(int(elapsed_time))
				//time.Sleep(50 * time.Millisecond)
				//move_last_time = time.Now()
				//fmt.Println("skMove   ball_detected", ball_detected, "middle time", (move_time_now.Sub(move_last_time).Milliseconds()))

			}

		}
	}

}
