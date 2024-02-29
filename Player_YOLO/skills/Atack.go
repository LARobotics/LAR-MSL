package skills

import (
	"context"
	"fmt"
	"math"

	//"math"
	coms "player/communication"
	"time"
)

const DRS_GAIN = 1.3

/*
**
*************Atack*************

Command: 2 Bx By E/S

Bx -> target x coordinate
By -> target y coordinate
E/S ->

*************Atack*************
**
*/
//input: deslocamento dos pixeis em x
var atack_atractor = NewAtractor(Katracao_atack, Kintensidade_atack, outputLimit_atractor_atack)

//atack_atractor := NewAtractor(0.55, 0.03, 80)

// input: deslocamento angular do robot a bola
// atack_orientation := NewPid(0.45, 0.0, 0.0, 0.05, 80)
var atack_orientation = NewPid(Kp_atack, Ki_atack, Kd_atack, 0.05, outputLimit_PID_atack)

//var direction_reppeler = NewReppeller(Krepulsao_move, Kinfluencia_move, outputLimit_reppeller_move)

func skAtack(args_ [7]int, quit chan int) {
	fmt.Println("skAtack")
	//Katracao := 2.0
	//Kintensidade := 3.8
	arg := args_
	//vare := arg[0]
	fmt.Println("initKinectCamera!")
	var ball_pos2 position
	KICK_DONE = false
	// := 0
	var rot int
	var esta_flag bool
	var old_time time.Time
	var current_time time.Time
	ball_pos2.X = -1
	ball_pos2.Y = -1
	var erro float64

	var vel float64
	var angle float64
	var i_robot coms.Robot_st
	var direction int

	var my_pos position
	var db coms.LocalDB
	var last_iter time.Time
	var now_iter time.Time
	var accelerate bool

	fmt.Println("Entrou3", last_iter)

	var erro_array []float64
	var acc float64

	var ball_coords coms.Ball_st
	var bs_ball_coords coms.Ball_st
	ball_detected := false
	esta_flag = false
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return

		default:

			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()

			fmt.Println("_________skAtack........1", arg)
			resp, err := client.Send_Kinect(context.Background(), &req)
			//fmt.Println("\n\nEntrou5", resp.Objects, resp.Objects[1].Id)
			//fmt.Println("\nEntrou6", resp)
			//fmt.Println("ismsimsismsimsi")
			coms.GetDatabase(&db)

			//last_ball_X := ball_coords.Coords.X
			//last_ball_Y := ball_coords.Coords.Y

			ball_coords.Coords.X = db.Ball.Coords.X
			ball_coords.Coords.Y = db.Ball.Coords.Y

			//Get ball position from basestation
			bs_ball_coords.Coords.X = float64(arg[0])
			bs_ball_coords.Coords.Y = float64(arg[1])

			//Get mode to run skill
			//If arg equal to 1, limit speed to 30
			if arg[5] == 1 {
				atack_atractor.outputLimit = 20
			} else {
				atack_atractor.outputLimit = outputLimit_atractor_atack
			}

			ball_detected = false
			if err == nil && resp.Objects != nil {
				for _, OBJ := range resp.Objects {
					if OBJ.Id == 0 {
						fmt.Println("ismsimsismsimsi")

						ball_detected = true
						ball_pos2.X = float64(OBJ.X)
						ball_pos2.Y = float64(OBJ.Y)
						//ball_depth_kinect = int(OBJ.Dist)

						break
					}
				}
			}
			fmt.Println("skAtack......2")
			now_iter = time.Now()
			if ball_detected { //&& float64(now_iter.Sub(last_iter).Milliseconds()) > 33
				esta_flag = false
				atack_orientation.outputLimit = outputLimit_atractor_atack
				last_iter = now_iter
				fmt.Println("resp.Objects[0]", resp.Objects)
				fmt.Println("aquiaquiAUIQi")

				//process the image from kinect
				//erro = float64(resp.Objects[0].Dist) / 10
				last_erro := erro
				erro = float64(db.Ball.Dist)

				erro_array = append([]float64{erro}, erro_array...)
				if len(erro_array) > 5 {
					erro_array = erro_array[:len(erro_array)-1]
				}
				//println("error_array", erro_array)

				acc = 0
				if len(erro_array) > 1 {
					for idx := 1; idx < len(erro_array)-2; idx++ {
						fmt.Println(".......idx", idx)
						acc += erro_array[idx-1] - erro_array[idx]
					}
				}
				//println("acc -------------->>>>", acc)

				if acc > 200 {
					fmt.Println("accelleration last vs erro", last_erro, erro)
					accelerate = true
				} else {
					accelerate = false
				}
				//trajectory_ball_angle := int(math.Atan2(last_ball_X-ball_coords.Coords.X, last_ball_Y-ball_coords.Coords.Y) * 180 / 3.14)

				//If ball angle passes this threshold, it means its moving on my direction
				/*if trajectory_ball_angle > 90 || trajectory_ball_angle < (-90) {
					vel = 0.75 * vel
				}*/
				//fmt.Println("\nball_X", ball_pos2.X, "ball_Y", ball_pos2.Y)

				//erro = float64(480 - ball_pos2.Y)

				angle = getAngleRelativeToRobot(ball_pos2.X, ball_pos2.Y, 0)
				fmt.Println("Kinect ang  ", int(angle))
				fmt.Println("Kinect erro  ", int(erro))
				direction = int(angle)

				if ball_pos2.Y > 390 {
					my_pos.X = i_robot.Coords.X
					my_pos.Y = i_robot.Coords.Y
					//fmt.Println(" -- tenho a bola --")

					//angle = math.Atan2((0 - my_pos.Y), (900 - my_pos.X))
					//fmt.Println(" - angle - ", angle)
					// angle = float64(ball.Angle)
				}
			} else if db.Team != nil && db.Ball.Conf > 0 {
				//atack_orientation.outputLimit=30
				if db.Ball.Dist > 150 {
					erro = 0 //float64(db.Ball.Dist) / 6
				} else {
					erro = 0
				}
				angle = float64(db.Ball.Angle)

				direction = int(angle)
				if direction < 0 {
					direction = 360 + direction
				}
				esta_flag = true

			} else {
				esta_flag = true
				fmt.Println("BaseStation coordinates")
				angle = math.Atan2(bs_ball_coords.Coords.Y-db.Team[0].Coords.Y, bs_ball_coords.Coords.X-db.Team[0].Coords.X)
				erro = math.Sqrt(math.Pow(bs_ball_coords.Coords.Y-db.Team[0].Coords.Y, 2) + math.Pow(bs_ball_coords.Coords.X-db.Team[0].Coords.X, 2))
			}

			//contolo da velocidade angular
			//Se o erro = a 0 -> distancia kinect < 50 cm
			//Alterar verificação dos pixeis pelo status da Carolina
			//erro = float64(db.Ball.Dist)
			vel = atack_atractor.Update(erro)

			old_time = current_time
			current_time = time.Now()
			coms.SetLoopTime(int(current_time.Sub(old_time).Milliseconds()))

			rot = int(atack_orientation.Update(angle, float64(current_time.Sub(old_time).Seconds())))

			if esta_flag {
				if vel > 20 {
					//vel=20
				}
				if rot > 20 {
					rot = 20
				}
				if rot < -20 {
					rot = -20
				}
			}
			fmt.Println(esta_flag, arg[2], rot)
			if accelerate {
				//vel = DRS_GAIN * vel
			}
			/*obstacles := db.Team*/
			/*obstacles := db.Team

			obstacles = append(obstacles, db.Opponent...)

			obstacles = obstacles[1:]

			direction = direction_reppeler.Update(obstacles, int(erro), direction)*/
			//last_direction := direction
			//direction = (7 * direction / 10) + (3 * last_direction / 10)
			if direction < 0 {
				direction += 360
			}
			//fmt.Println(" rotational  ", rot)

			//fmt.Println(" velocity ", int(vel))

			//fmt.Println("direction  ", int(direction))

			if coms.GetBallStatus() < 3 {
				//fmt.Println("direction  ORBITA BOLA", OrbitarBola(1, int(angle)))
				vel = 0
			}

			coms.SendCommandToESP(coms.CMD_all, int(vel), int(rot), int(direction), 1, 0)
			//time.Sleep(10 * time.Millisecond)
		}

	}
}
