package skills

import (
	"context"
	"fmt"
	"math"
	coms "player/communication"
	pb "player/pb"
	"time"
)

const KICK_LOOP_TIMEOUT = 40

/* ------------------------------------ Kick ------------------------------------
Command: 3 Tx Ty P/K Dx Dy
Tx -> target x coordinate
Ty -> target y coordinate
P/K -> pass(0) or kick(0)
Dx -> Previous displacement on x Axis
Dy -> Previous displacement on y Axis
------------------------------------------------------------------------------ */

var kick_orientation = NewPid(Kp_kick, Ki_kick, Kd_kick, 0.05, outputLimit_PID_kick)

// -------------------- Orientation PIDs --------------------

var Activate_Kick bool

// ----------------------------------------------------------
// ----------------------- Team Side ------------------------
//var blue_shirt = true // We are blue team
// ----------------------------------------------------------

// Distance between the goal and the target to score in meters
var dist_goal = 0.15

// Variable that verify if the robot is align with the target
var target_check = false

// PID timers
var current_time, old_time time.Time

// Target variables
var target position
var target_dist float64

// Variable of the robot rotation
var rot int

// Variables related to the team and opponent robots
var team_Robot position
var opponent_Robots []coms.Robot_st
var robot coms.Robot_st

// Variables realted to the goal
var goal coms.Robot_st
var goals []coms.Robot_st
var change_goal = false
var iterations int

// Variables for the kinect neural network
var resp *pb.Response_Kinect

var last_erro float64

func getObjectDetected(kick bool) {
	if kick {
		// Check every object
		for i := 0; i < len(resp.Objects); i++ {
			switch resp.Objects[i].Id {
			case 1: // Blue Shirt
				if robot_shirt == RED_SHIRT { // if the team is playing in red
					// Get the coordinates and distance of the robot
					robot.Coords.X = float64(resp.Objects[i].X)
					robot.Coords.Y = float64(resp.Objects[i].Y)
					robot.Distance = int(resp.Objects[i].Dist)
					// Save the robot in the array
					opponent_Robots = append(opponent_Robots, robot)
				}
				break

			case 2: // Goal
				// Get the coordinates and distance of the goal
				goal.Coords.X = float64(resp.Objects[i].X)
				goal.Coords.Y = float64(resp.Objects[i].Y)
				goal.Distance = int(resp.Objects[i].Dist)
				// Save the goal in the array
				goals = append(goals, goal)
				break

			case 4: // Red shirt
				if robot_shirt == BLUE_SHIRT { // if the team is playing in blue
					// Get the coordinates and distance of the robot
					robot.Coords.X = float64(resp.Objects[i].X)
					robot.Coords.Y = float64(resp.Objects[i].Y)
					robot.Distance = int(resp.Objects[i].Dist)
					// Save the robot in the array
					opponent_Robots = append(opponent_Robots, robot)
				}
				break

			case 5: // Robot
				// Get the coordinates and distance of the robot
				robot.Coords.X = float64(resp.Objects[i].X)
				robot.Coords.Y = float64(resp.Objects[i].Y)
				robot.Distance = int(resp.Objects[i].Dist)
				// Save the robot in the array
				opponent_Robots = append(opponent_Robots, robot)
				break
			}
		}
	} else {
		// Check every object
		for i := 0; i < len(resp.Objects); i++ {
			// Verify if there is a robot in the middle of the image
			switch resp.Objects[i].Id {
			case 1: // Blue Shirt
				if robot_shirt == BLUE_SHIRT { // if the team is playing in blue
					robot.Coords.X = float64(resp.Objects[i].X)
					robot.Coords.Y = float64(resp.Objects[i].Y)
					robot.Distance = int(resp.Objects[i].Dist)
					if 270 < team_Robot.X && team_Robot.X < 370 {
						team_Robot.X = robot.Coords.X
						team_Robot.Y = robot.Coords.Y
						break
					}
				}
				break
			case 4: // Red shirt
				if robot_shirt == RED_SHIRT { // if the team is playing in red
					robot.Coords.X = float64(resp.Objects[i].X)
					robot.Coords.Y = float64(resp.Objects[i].Y)
					robot.Distance = int(resp.Objects[i].Dist)
					if 270 < team_Robot.X && team_Robot.X < 370 {
						team_Robot.X = robot.Coords.X
						team_Robot.Y = robot.Coords.Y
						break
					}
				}
				break
			}
		}
	}
}

func kick_ball() {
	// Check every object
	getObjectDetected(true)
	fmt.Println("kick_ball")
	// If the robot can see a goal
	if goals != nil {
		// The first target will be the second goal detected (the further one)
		// If there the robot only sees one, he aims for that
		// Change goal is the variable that define if the robot needs to go for the other goal
		if len(goals) > 1 && !change_goal {
			// Update target position and distance
			target.X = goals[1].Coords.X
			target.Y = goals[1].Coords.Y
			target_dist = float64(goals[1].Distance)
		} else {
			// Update target position and distance
			target.X = goals[0].Coords.X
			target.Y = goals[0].Coords.Y
			target_dist = float64(goals[0].Distance)
		}
		//obtain the angle of the other robot relative to the robot
		target.Angle = getAngleRelativeToRobot(target.X, target.Y, 10)

		// If the target is in the right side, it means that the robot needs to aim a little to the left, otherwise, to the right
		if target.X > 320 {
			// dist goal is the distance to the goal that we want the robot to shoot
			target.Angle = target.Angle + math.Atan2(dist_goal, target_dist)
		} else {
			target.Angle = target.Angle - math.Atan2(dist_goal, target_dist)
		}

		// Calculate the rotational speed of the robot to aim to the target
		current_time = time.Now()
		rot = int(kick_orientation.Update(target.Angle, float64(current_time.Sub(old_time).Seconds())))
		old_time = current_time

		fmt.Println("Target: ", target.X, target.Y)
		fmt.Println("Target angle: ", target.Angle)
		fmt.Println("Rotational:  ", -rot)

		// If the robot is already looking to the target
		if -5 < target.Angle && target.Angle < 5 {
			// Verify if there is no robots on the way
			if opponent_Robots != nil {
				for i := 0; i < len(opponent_Robots); i++ {
					// If there is, the robot will change the target to the other goal
					if 290 < opponent_Robots[i].Coords.X && opponent_Robots[i].Coords.X < 350 {
						if change_goal {
							change_goal = false
							target_check = false
						} else {
							change_goal = true
							target_check = false
						}
					} else { // Otherwise it will shoot
						rot = 0
						coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 1, 15)
						// The ball is no longer with the robot
					}
				}
			}
		}
	} else {
		target_check = false
	}
}

func pass_ball() (float64, bool) {
	team_Robot.X = -1
	team_Robot.Y = -1

	// Check every object
	getObjectDetected(false)
	fmt.Println("pass_ball")

	// If there is a robot, go for the pass
	if team_Robot.X != -1 && team_Robot.Y != -1 {
		//obtain the angle of the robot relative to us
		team_Robot.Angle = getAngleRelativeToRobot(team_Robot.X, team_Robot.Y, 10)

		// Calculate the rotational speed of the robot to aim to the target
		/*current_time = time.Now()
		rot = int(kick_orientation.Update(team_Robot.Angle, float64(current_time.Sub(old_time).Seconds())))
		old_time = current_time*/

		fmt.Println("Target: ", team_Robot.X, team_Robot.Y)
		fmt.Println("Target angle: ", team_Robot.Angle)
		fmt.Println("Rotational:  ", -rot)

	} else {
		// Otherwise, orient again to the target via OmniVision
		target_check = false
	}
	return team_Robot.Angle, false
}

func target_omnivs(target position, DB coms.LocalDB) (float64, bool) { //(rot int)
	var erro float64
	last_erro = erro
	// Get the target coordinates
	// Calculate the error for PID controller
	fmt.Println("targetY ", target.Y, "Y ", DB.Team[0].Coords.Y, "targetX ", target.X, "X ", DB.Team[0].Coords.X)

	erro = math.Atan2(target.Y-DB.Team[0].Coords.Y, target.X-DB.Team[0].Coords.X) * 180 / math.Pi
	erro -= float64(DB.Team[0].Orientation)
	// Get the time for the interval
	fmt.Println("target_omnivs erro: ", erro, "orientation", float64(DB.Team[0].Orientation))
	//fmt.Println("Rotation: ", rot)

	if last_erro*erro < 0 {
		fmt.Println("----------------KICKREADY-------------")
		return erro, true

	}

	// Check if the robot has already aim to the target
	if erro < 5 && erro > -5 {
		//fmt.Println("-------------------iterations  ", iterations)
		if iterations == 2 {
			rot = 0
			return erro, true

		}
		iterations++
		//target_check = true
	} else {
		iterations = 0

	}
	return erro, false
}

func skKick(args_ [7]int, quit chan int) {
	// Receive the arguments
	arg := args_
	//vare := arg[0]
	fmt.Println("----------------------------- KICK -----------------------------")
	kick_done := false
	// Variable of the DataBase
	var DB coms.LocalDB
	kick := 0
	// Inicialize the target
	target.X = -1
	target.Y = -1

	coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 1, 0)
	//Update PIDs of kinect and OmniVision
	var ball_pos position
	fmt.Println(ball_pos)
	state_Kick := "POSITIONING"
	//resp, err := client.Send_Kinect(context.Background(), &req)
	kick_time_now := time.Now()
	kick_last_time := current_time

	var erro_orientation float64
	// Inicialize the cycle
	var vel int
	var ideal_target position
	var direction int
	for {
		// Verify if is time to quit
		select {
		case <-quit:
			fmt.Println("----------------------------- Quit -----------------------------")
			wait_4_skill.Done()
			return
		default:
			//fmt.Println("INICIO ROTINA ")
			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()
			//fmt.Println("INICIO ROTINA 2")
			// Update Database values
			coms.GetDatabase(&DB)
			//fmt.Println("target_check", target_check, !(float64(loop_time_now.Sub(loop_last_time).Milliseconds()) < 40))
			// If the robot havent reached the target yet
			loop_time_now = time.Now()
			//fmt.Println("__________KICK")

			if !(float64(loop_time_now.Sub(loop_last_time).Milliseconds()) < KICK_LOOP_TIMEOUT) {
				target.X = float64(arg[0])
				target.Y = float64(arg[1])

				ideal_target.X = float64(arg[3])
				ideal_target.Y = float64(arg[4])

				ideal_target.Angle = math.Atan2((ideal_target.Y)-float64(DB.Team[0].Coords.Y), (float64(ideal_target.X))-float64(DB.Team[0].Coords.X))
				fmt.Println("INICIO ROTINA 3")
				//resp, err := client.Send_Kinect(context.Background(), &req)
				fmt.Println("INICIO ROTINA ")
				ball_detected := false
				fmt.Println(ball_detected)
				/*if err == nil && resp.Objects != nil {
					for _, OBJ := range resp.Objects {
						if OBJ.Id == 0 {
							ball_detected = true
							ball_pos.X = float64(OBJ.X)
							ball_pos.Y = float64(OBJ.Y)

							break
						}
					}
				}*/
				fmt.Println("------------CA DENTRO: ")

				loop_last_time = loop_time_now
				//fmt.Println("target_check", target_check, !(float64(loop_time_now.Sub(loop_last_time).Milliseconds()) < 40))
				//fmt.Println("\nskkick")

				switch state_Kick {
				case "POSITIONING":
					{
						if DB.Team != nil && coms.GetBallStatus() != 0 {
							vel = 0
							// Get the target coordinates
							//fmt.Println("Target coordinates : ", target.X, target.Y)

							var Activate_Kick bool
							// Function to orient the robot to the target
							erro_orientation, Activate_Kick = target_omnivs(target, DB)
							for erro_orientation > 180 {
								erro_orientation -= 360
							}
							for erro_orientation <= -180 {
								erro_orientation += 360
							}

							direction = int(ideal_target.Angle)
							
							//vel = int(math.Sqrt(math.Pow(ideal_target.Y-float64(DB.Team[0].Coords.Y), 2) + math.Pow(ideal_target.X-float64(DB.Team[0].Coords.X), 2)))
							if Activate_Kick {
								vel = 5
								state_Kick = "FINALIZE"
							}
							team_Robot.X = -1
							team_Robot.Y = -1

							// Check every object
							/*getObjectDetected(false)
							if team_Robot.X != -1 && team_Robot.Y != -1 {
								if arg[2] == 0 && ball_detected {
									// Function for the pass
									state_Kick = "PASS"
								} else if arg[2] == 1 && ball_detected {
									// Function for the kick
									state_Kick = "KICK"
								}
							}*/
						}
						kick = 0

					}
				case "PASS":
					{

						// Open Kinect and the respective objects

						// If there was no error and the kinect is detecting objects
						if resp.Objects != nil {
							fmt.Println(resp)
							// Function for the pass
							var detection_ok bool
							erro_orientation, detection_ok = pass_ball()
							if !detection_ok {
								state_Kick = "POSITIONING"
							} else if -5 < erro_orientation && erro_orientation < 5 {
								// If the robot is already looking to the target
								state_Kick = "FINALIZE"
							}
						}
					}

				case "KICK":
					{
						// Open Kinect and the respective objects
						resp, _ = client.Send_Kinect(context.Background(), &req)

						// If there was no error and the kinect is detecting objects
						if resp.Objects != nil {
							fmt.Println(resp)
							// Function for the kick
							kick_ball()

						}

					}
				case "FINALIZE":
					{

						if !kick_done {
							fmt.Println("Inside Kick done", coms.GetBallStatus())
							kick = 9
							if arg[2] == 1 {
								fmt.Println("Inside Kick done")
								kick = 15
							}
							//if coms.GetBallStatus() == 3 {
							//kick_done = true
							//}
							fmt.Println(".....", kick_done, kick)

							//coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 1, kick)
							
							
						} else {
							fmt.Println("else Kick done", coms.GetBallStatus())
							erro_orientation = 0
							kick = 0
						}
					}
				}

				current_time := time.Now()
				fmt.Println("starte on kick: ", state_Kick)
				// Calculate the rotation
				rot = int(kick_orientation.Update(float64(erro_orientation), float64(current_time.Sub(old_time).Seconds())))
				old_time = current_time
				//fmt.Println("state_Kick", state_Kick, "coms.GetBallStatus()", coms.GetBallStatus())
				fmt.Println("vel: ", vel, "dir: ", direction, "rot", rot,coms.GetBallStatus())
				if coms.GetBallStatus()>2 {
					kick=0
					vel=0
					rot=0	
					kick_done=true	
					fmt.Println("entrei aqui...... ")				
				}
				coms.SendCommandToESP(coms.CMD_all, vel, rot, 0, 1, kick)
				fmt.Println("skickingdvsd ")
				
				kick_time_now = time.Now()
				//fmt.Println("loop time", float64(kick_time_now.Sub(kick_last_time).Milliseconds()), "\n")
				//fmt.Println("PID in Use:", kick_orientation.kP, kick_orientation.kI, kick_orientation.kD, kick_orientation.outputLimit)
				kick_last_time = kick_time_now
				fmt.Println("FIM ROTINA ")
				coms.SetLoopTime(int(kick_time_now.Sub(kick_last_time).Milliseconds()))

			}
		}
	}
}
