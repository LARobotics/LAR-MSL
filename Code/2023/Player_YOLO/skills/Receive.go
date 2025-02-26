package skills

import (
	"context"
	"fmt"
	"image"
	"math"
	coms "player/communication"
	"time"
)

const RCV_LOOP_TIMEOUT = 15
const PASS_DIST_THRESH = 100 //centemeters
/*
**
*************Receive*************

Command: 4 Bx By

Bx -> target x coordinate
By -> target y coordinate

*************Receive*************
**
*/
//receive_orientation := NewPid(0.05, 0.0, 0.0, 0.05, 20)
var receive_orientation = NewPid(Kp_receive_rot, Ki_receive_rot, Kd_receive_rot, 0.05, outputLimit_PID_receive_rot)

// /db_pid := NewPid(1, 0, 0, 0.05, 100)
// receive_linear_mov := NewPid(0.12, 0.0, 0.0, 0.05, 40)
var receive_linear_mov = NewPid(Kp_receive_vel, Ki_receive_vel, Kd_receive_vel, 0.05, outputLimit_PID_receive_vel)

type MovementPrediction struct {
	name    string
	X       []float64
	Y       []float64
	angle   []float64
	power   int
	weights []float64
}

func NewMovementPrediction(name string, length int, power int) *MovementPrediction {
	weights := []float64{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1}
	sumWeights := 0.0
	for _, weight := range weights {
		sumWeights += weight
	}
	for i := range weights {
		weights[i] /= sumWeights
	}

	return &MovementPrediction{
		name:    name,
		X:       make([]float64, length),
		Y:       make([]float64, length),
		angle:   make([]float64, length),
		power:   power,
		weights: weights,
	}
}

func (m *MovementPrediction) NextMove(x, y float64) {
	m.X = append(m.X[1:], x)
	m.Y = append(m.Y[1:], y)
}

func (m *MovementPrediction) NextAngle(x float64) {
	m.angle = append(m.angle[1:], x)
}

func (m *MovementPrediction) getPrediction(numberOfNextPoints int) (float64, float64) {
	xLen := len(m.X)
	xPred := make([]float64, xLen-numberOfNextPoints+1)
	yPred := make([]float64, xLen-numberOfNextPoints+1)

	for i := 0; i < xLen-numberOfNextPoints+1; i++ {
		for j := 0; j < numberOfNextPoints; j++ {
			xPred[i] += m.X[i+j] * m.weights[j]
			yPred[i] += m.Y[i+j] * m.weights[j]
		}
	}

	nextX := m.X[xLen-1] + (m.X[xLen-1] - xPred[xLen-numberOfNextPoints])
	nextY := m.Y[xLen-1] + (m.Y[xLen-1] - yPred[xLen-numberOfNextPoints])

	return nextX, nextY
}

func skReceive(args_ [7]int, quit chan int) {
	fmt.Println("skReceive")

	//var rgb_frame gocv.Mat
	//var kinect_ball_pos position
	//var last_kinect_ball_pos position

	var vel int
	var current_time, old_time time.Time
	dir := 0

	arg := args_
	//vare := arg[0]
	var rot int

	var receive_time_now time.Time
	var receive_last_time time.Time

	var db coms.LocalDB

	//var last_omni_x, last_omni_y float64
	var erro_angular float64
	var erro_linear float64
	//var last_x, last_y float64
	var last_x_omni, last_y_omni float64
	var last_x, last_y float64
	state_Receive := "WAIT_BALL"
	last_dist_omni := 0
	last_dist_kinect := 0
	//var X_coords_antes float64
	//var last_erro_angular float64
	var ball_distance_omni int
	var kinect_ball_pos position
	var ball_depth_kinect int
	first_depth_ball := 0
	var trajectory_angle float64
	fmt.Println(trajectory_angle)
	first_time_receiving := true
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return
		default:
			loop_time_now = time.Now()

			/*for len(Fns_args) > 0 && vare != -2 {
				arg = <-Fns_args
				//fmt.Println("ARGS        :", arg)
			}*/
			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()

			fmt.Println("_________skReceive", arg)
			last_dist_omni = ball_distance_omni
			last_dist_kinect = ball_depth_kinect
			if first_time_receiving && last_dist_omni != 0 {
				first_depth_ball = int(last_dist_omni)
			}
			coms.GetDatabase(&db)
			ball_distance_omni = db.Ball.Dist * 10
			ball_angle := (db.Ball.Angle)
			//fmt.Println(LoopTimePassed(loop_time_now, loop_last_time))
			//fmt.Println("LEN", resp.Objects)
			resp, _ = client.Send_Kinect(context.Background(), &req)

			if LoopTimePassed(loop_time_now, loop_last_time) > RCV_LOOP_TIMEOUT && db.Team != nil {
				loop_last_time = loop_time_now
				//fmt.Println(resp.Objects)
				fmt.Println(receive_linear_mov)
				ball_detected := false
				if resp.Objects != nil {
					for _, OBJ := range resp.Objects {
						if OBJ.Id == 0 {
							ball_detected = true
							kinect_ball_pos.X = float64(OBJ.X)
							kinect_ball_pos.Y = float64(OBJ.Y)
							ball_depth_kinect = int(OBJ.Dist)

							var kinect_point image.Point
							kinect_point.X = int(kinect_ball_pos.X)
							kinect_point.Y = int(kinect_ball_pos.Y)
							filter(kinect_point)
							break
						}
					}
					if !ball_detected {
						state_Receive = "WAIT_BALL"

					}
				}

				//fmt.Println(coms.Data_ESP.Ball_status)
				//erro_linear = 0
				switch state_Receive {
				case "WAIT_BALL":
					{
						fmt.Println("ball_distance_omni", ball_distance_omni, ball_angle)
						if first_time_receiving && last_dist_kinect != 0 {
							first_depth_ball = last_dist_kinect
							first_time_receiving = false
							//fmt.Println("first_time_receiving")
						}
						erro_angular = float64(ball_angle)
						if ball_depth_kinect != 0 {
							erro_angular = getAngleRelativeToRobot(kinect_ball_pos.X, kinect_ball_pos.Y, 0)
							//If the kinect is measuring the distance to the ball
							//fmt.Println("ball_distance", ball_depth_kinect, first_depth_ball)
							if ball_depth_kinect+300 < int(first_depth_ball) && ball_depth_kinect < 5500 {
								state_Receive = "FINE_ADJUST"

							}
						} else if ball_distance_omni+250 < int(last_dist_omni) {
							//If the kinect is not measuring the distance to the ball, use the omni vision
							state_Receive = "MOVE_INTERCEPTION"
							if ball_distance_omni < 5000 {
								state_Receive = "FINE_ADJUST"
							}

						}

					}
				case "MOVE_INTERCEPTION":
					{
						//trajectory_angle := -(math.Atan2(last_x-kinect_ball_pos.X, last_y-kinect_ball_pos.Y) * 180 / math.Pi)
						trajectory_angle = -(math.Atan2(last_x_omni-db.Ball.Coords.X, last_y_omni-db.Ball.Coords.Y) * 180 / math.Pi)

						last_x_omni = db.Ball.Coords.X
						last_y_omni = db.Ball.Coords.Y

						//fmt.Println("ball_distance_omni", ball_distance_omni, "ball_angle", ball_angle, "trajectory_angle", trajectory_angle)
						erro_angular = 0 //float64(db.Team[0].Orientation) - trajectory_angle
						if ball_distance_omni < 5000 {
							state_Receive = "FINE_ADJUST"
						}
						//state_Receive = "FINE_ADJUST"
						//erro_angular = float64(db.Ball.Angle)
						erro_linear = float64(ball_distance_omni) * math.Sin(float64(ball_angle)*180/math.Pi)
						if erro_linear < 0 {
							/*dir = int(90.0 + db.Team[0].Orientation)
							if dir < -180 {
								dir = 180 - (dir + 180)
							}*/
							dir = 90
						} else {
							/*dir = int(-90.0 - db.Team[0].Orientation)
							if dir > 180 {
								dir = -180 + (dir - 180)
							}*/
							dir = 270

						}

					}

				case "FINE_ADJUST":
					{
						if resp.Objects != nil {
							ang_aux := getAngleRelativeToRobot(kinect_ball_pos.X, kinect_ball_pos.Y, float64(ball_depth_kinect))

							/*fmt.Println("ball_pos.X", kinect_ball_pos.X, "ball_pos.Y", kinect_ball_pos.Y)
							fmt.Println("Ball Angle", ang_aux)*/
							x := math.Sin(ang_aux * math.Pi / 180)
							x = x * float64(ball_depth_kinect)
							y := math.Cos(ang_aux * math.Pi / 180)
							y = y * float64(ball_depth_kinect)
							trajectory_angle = -(math.Atan2(last_x-x, last_y-y) * 180 / math.Pi) + float64(db.Team[0].Orientation)
							last_x = x
							last_y = y
							//fmt.Println("ball_distance", ball_depth_kinect, "ball_angle", ang_aux, "trajectory_angle", trajectory_angle)

							erro_linear = x  //float64(ball_depth_kinect) * math.Sin(float64(ang_aux)*180/math.Pi)
							erro_angular = 0 //float64(db.Team[0].Orientation) - trajectory_angle
							if ball_distance_omni > int(last_dist_omni) {
								//atack()

							}
						}
						//fmt.Println("db.Team[0].Orientation", db.Team[0].Orientation, "dir", dir)

						if erro_linear > 0 {
							dir = 90 //int(90.0 + db.Team[0].Orientation)
							if dir > 180 {
								//dir = 180 - (dir + 180)

								dir -= 360
							}
						} else {
							dir = -90 //int(-90.0 - db.Team[0].Orientation)
							if dir < -180 {
								//dir = -180 + (dir - 180)
								dir += 360
							}

						}
						if coms.GetBallStatus() == 2 || coms.GetBallStatus() == 1 {

						}
						break
					}
				case "Atack":
					{
						if resp.Objects != nil {
							ang_aux := getAngleRelativeToRobot(kinect_ball_pos.X, kinect_ball_pos.Y, float64(ball_depth_kinect))

							//fmt.Println("ball_distance", ball_depth_kinect, "ball_angle", ang_aux, "trajectory_angle", trajectory_angle)

							erro_linear = float64(ball_depth_kinect) //float64(ball_depth_kinect) * math.Sin(float64(ang_aux)*180/math.Pi)
							erro_angular = ang_aux                   //float64(db.Team[0].Orientation) - trajectory_angle

						}

						if coms.GetBallStatus() == 2 || coms.GetBallStatus() == 1 {

						}
						break
					}

				}

				old_time = current_time
				current_time = time.Now()

				/*fmt.Println("state_Receive", state_Receive)
				fmt.Println("Erro Angular:", int(erro_angular))
				fmt.Println("Erro linear:", int(erro_linear))*/

				old_time = current_time
				current_time = time.Now()

				if erro_linear < 0 {
					erro_linear = -erro_linear
				}
				rot = int(receive_orientation.Update(erro_angular, float64(current_time.Sub(old_time).Seconds())))

				vel = int(receive_linear_mov.Update(erro_linear, float64(current_time.Sub(old_time).Seconds())))

				if dir < 0 {
					fmt.Println("DIR MENOR QUE 0 DIR:", dir)
					dir += 360
				}
				if vel < 0 {
					vel = -vel
				}

				//fmt.Println("vel: ", (vel), "dir: ", (dir), "rot", rot, "\n")

				coms.SendCommandToESP(coms.CMD_all, (vel), (rot), dir, 100, 100, 0)
				coms.SetLoopTime(int(receive_time_now.Sub(receive_last_time).Milliseconds()))
				receive_last_time = receive_time_now
				receive_time_now = time.Now()
			}

			//time.Sleep(10 * time.Millisecond)

		}
	}
}

func GoToReceptionPoint(ball_side float64, side int, Pos image.Point) (Pos_Des image.Point) {
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
func skReceive2(args_ [7]int, quit chan int) {
	fmt.Println("skReceive")

	//var rgb_frame gocv.Mat
	//var kinect_ball_pos position
	//var last_kinect_ball_pos position

	var vel int
	var current_time, old_time time.Time
	direction := 0

	arg := args_
	//vare := arg[0]
	var rot int

	var receive_time_now time.Time
	var receive_last_time time.Time

	var db coms.LocalDB

	//var last_omni_x, last_omni_y float64
	var erro_angular float64
	var erro_linear float64
	//var last_x, last_y float64
	var last_x_omni, last_y_omni float64
	state_Receive := "WAIT_BALL"

	//var X_coords_antes float64
	//var last_erro_angular float64
	var ball_distance_omni int
	var last_ball_distance_omni int
	var kinect_ball_pos position
	var ball_depth_kinect int
	var trajectory_angle float64
	fmt.Println(trajectory_angle)

	var BS_ball_coords coms.Ball_st
	var ball_angle int
	var ball_acceleration coms.Ball_st
	var elappsed_time float64

	var last_x float64
	var last_y float64
	var last_dist_omni int
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return
		default:
			loop_time_now = time.Now()

			/*for len(Fns_args) > 0 && vare != -2 {
			  arg = <-Fns_args
			  //fmt.Println("ARGS        :", arg)
			 }*/
			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()

			BS_ball_coords.Coords.X = float64(arg[0])
			BS_ball_coords.Coords.X = float64(arg[1])

			coms.GetDatabase(&db)
			last_dist_omni = ball_distance_omni
			ball_distance_omni = db.Ball.Dist
			ball_angle = db.Ball.Angle

			elappsed_time = LoopTimePassed(loop_time_now, loop_last_time)

			if LoopTimePassed(loop_time_now, loop_last_time) > RCV_LOOP_TIMEOUT && db.Team != nil {
				loop_last_time = loop_time_now
				//fmt.Println(resp.Objects)
				fmt.Println(receive_linear_mov)
				ball_detected := false
				if resp.Objects != nil {
					for _, OBJ := range resp.Objects {
						if OBJ.Id == 0 {
							ball_detected = true
							kinect_ball_pos.X = float64(OBJ.X)
							kinect_ball_pos.Y = float64(OBJ.Y)
							ball_depth_kinect = int(OBJ.Dist)

							var kinect_point image.Point
							kinect_point.X = int(kinect_ball_pos.X)
							kinect_point.Y = int(kinect_ball_pos.Y)
							filter(kinect_point)
							break
						}
					}
					if !ball_detected {
						state_Receive = "WAIT_BALL"

					}
				}

				//fmt.Println(coms.Data_ESP.Ball_status)
				//erro_linear = 0
				switch state_Receive {
				case "WAIT_BALL":
					{
						if ball_distance_omni < (last_ball_distance_omni + PASS_DIST_THRESH) {
							state_Receive = "MOVE_INTERCEPTION"
						} else {
							erro_linear = 0
							erro_angular = float64(ball_angle)
						}
						break
					}
				case "MOVE_INTERCEPTION":
					{
						trajectory_angle = -(math.Atan2(last_x_omni-db.Ball.Coords.X, last_y_omni-db.Ball.Coords.Y) * 180 / math.Pi)

						last_x_omni = db.Ball.Coords.X
						last_y_omni = db.Ball.Coords.Y

						ball_acceleration.Coords.X = (db.Ball.Coords.X - last_x_omni) / elappsed_time
						ball_acceleration.Coords.Y = (db.Ball.Coords.Y - last_y_omni) / elappsed_time

						//erro_angular = float64(db.Ball.Angle)
						next_pos_x := float64(ball_distance_omni) * math.Sin(float64(ball_angle)*180/math.Pi)
						next_pos_y := -float64(ball_distance_omni) * math.Cos(float64(ball_angle)*180/math.Pi)
						erro_linear = math.Sqrt(math.Pow(next_pos_x, 2) + math.Pow(next_pos_y, 2))

						direction = int(math.Atan2((next_pos_x-db.Team[0].Coords.X), (next_pos_y-db.Team[0].Coords.Y)) * 180 / math.Pi)
						direction -= (db.Team[0].Orientation)

						erro_angular = float64(ball_angle - db.Team[0].Orientation)

						fmt.Println("ball_acceleration(X;Y)", ball_acceleration.Coords.X, ball_acceleration.Coords.Y)
						fmt.Println("next_pos_x(X;Y)", next_pos_x, next_pos_y)
						fmt.Println("erro_linear", erro_linear, "erro_angular", erro_angular)

						if direction < -180 {
							direction = 180 - (-direction - 180)
						}

						if direction > 180 {
							direction = -180 + (direction - 180)
						}

						break
					}

				case "FINE_ADJUST":
					{
						if resp.Objects != nil {
							ang_aux := getAngleRelativeToRobot(kinect_ball_pos.X, kinect_ball_pos.Y, float64(ball_depth_kinect))

							/*fmt.Println("ball_pos.X", kinect_ball_pos.X, "ball_pos.Y", kinect_ball_pos.Y)
							fmt.Println("Ball Angle", ang_aux)*/
							x := math.Sin(ang_aux * math.Pi / 180)
							x = x * float64(ball_depth_kinect)
							y := math.Cos(ang_aux * math.Pi / 180)
							y = y * float64(ball_depth_kinect)
							trajectory_angle = -(math.Atan2(last_x-x, last_y-y) * 180 / math.Pi) + float64(db.Team[0].Orientation)
							last_x = x
							last_y = y
							//fmt.Println("ball_distance", ball_depth_kinect, "ball_angle", ang_aux, "trajectory_angle", trajectory_angle)

							erro_linear = x  //float64(ball_depth_kinect) * math.Sin(float64(ang_aux)*180/math.Pi)
							erro_angular = 0 //float64(db.Team[0].Orientation) - trajectory_angle
							if ball_distance_omni > int(last_dist_omni) {
								//atack()

							}
						}
						//fmt.Println("db.Team[0].Orientation", db.Team[0].Orientation, "dir", dir)

						if erro_linear > 0 {
							direction = 90 //int(90.0 + db.Team[0].Orientation)
							if direction > 180 {
								//dir = 180 - (dir + 180)

								direction -= 360
							}
						} else {
							direction = -90 //int(-90.0 - db.Team[0].Orientation)
							if direction < -180 {
								//dir = -180 + (dir - 180)
								direction += 360
							}

						}
						if coms.GetBallStatus() == 2 || coms.GetBallStatus() == 1 {

						}
						break
					}
				case "Atack":
					{

						if resp.Objects != nil {
							ang_aux := getAngleRelativeToRobot(kinect_ball_pos.X, kinect_ball_pos.Y, float64(ball_depth_kinect))

							//fmt.Println("ball_distance", ball_depth_kinect, "ball_angle", ang_aux, "trajectory_angle", trajectory_angle)

							erro_linear = float64(ball_depth_kinect) //float64(ball_depth_kinect) * math.Sin(float64(ang_aux)*180/math.Pi)
							erro_angular = ang_aux                   //float64(db.Team[0].Orientation) - trajectory_angle

						} else {
							erro_linear = float64(ball_depth_kinect) //float64(ball_depth_kinect) * math.Sin(float64(ang_aux)*180/math.Pi)
							erro_angular = float64(ball_angle - db.Team[0].Orientation)

						}

						if coms.GetBallStatus() == 2 || coms.GetBallStatus() == 1 {

						}
						break
					}

				}

				old_time = current_time
				current_time = time.Now()

				/*fmt.Println("state_Receive", state_Receive)
				  fmt.Println("Erro Angular:", int(erro_angular))
				  fmt.Println("Erro linear:", int(erro_linear))*/

				old_time = current_time
				current_time = time.Now()

				if erro_linear < 0 {
					erro_linear = -erro_linear
				}
				rot = int(receive_orientation.Update(erro_angular, float64(current_time.Sub(old_time).Seconds())))

				vel = int(receive_linear_mov.Update(erro_linear, float64(current_time.Sub(old_time).Seconds())))

				if direction < 0 {
					fmt.Println("DIR MENOR QUE 0 DIR:", direction)
					direction += 360
				}
				if vel < 0 {
					vel = -vel
				}

				fmt.Println("vel: ", (vel), "dir: ", (direction), "rot", rot, "\n")

				coms.SendCommandToESP(coms.CMD_all, (vel), (rot), direction, 100, 100, 0)
				coms.SetLoopTime(int(receive_time_now.Sub(receive_last_time).Milliseconds()))
				receive_last_time = receive_time_now
				receive_time_now = time.Now()
			}

			//time.Sleep(10 * time.Millisecond)

		}
	}
}
