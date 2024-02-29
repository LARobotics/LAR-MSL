package skills

import "C"

import (
	"fmt"
	"image"
	"log"
	"math"
	"net"
	"os"
	coms "player/communication"
	"player/pb"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"

	"google.golang.org/grpc"
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

const ball_idx = 0
const teammate_idx = 1
const opponent_idx = 1
const goal_idx = 2

const Stop = 0
const Move = 0
const Atack = 0
const Kick = 0
const Receive = 0
const Cover = 0
const Defend = 0
const Control = 0

const RED_SHIRT = 0
const BLUE_SHIRT = 1

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
type Reppeller struct {
	Kreppeller  float64
	kinfluencia float64
	outputLimit float64
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

var skills_configs_mutex sync.Mutex

var loop_last_time time.Time
var loop_time_now time.Time

var args_calibration [11]float64

// var freenect_device *freenect.FreenectDevice
var led_sleep_time time.Duration
var image_quality = 100
var freenect_device_present = false

var fns []func(args_ [7]int, quit chan int)

// var fns_chan [8]chan bool
var fns_chan = make([]chan int, 10)

//var window3 = gocv.NewWindow("before dilated")

//var window1 = gocv.NewWindow("befo ilated")

// var window = gocv.NewWindow("dilated")
var ball_flag bool
var Fns_args = make(chan [7]int, 10)
var kick_flag = false
var KICK_DONE = false

/*
*
variables for kinect grpc
*
*/
var conn *grpc.ClientConn
var client pb.Yolo_KinectClient
var req pb.Request

var bs_send_ports_calib = []string{"30001", "30002", "30003", "30004", "30005"}
var receive_ports_calib = []string{"30011", "30012", "30013", "30014", "30015"}
var new_pid_received bool
var Robot_id int

var skill_loop_time = 0
var wait_4_skill sync.WaitGroup

var robot_shirt = 0

var BS_args [7]int
var BS_args_mutex sync.Mutex

func LoopTimePassed(tm_now time.Time, time_then time.Time) float64 {
	return float64(tm_now.Sub(time_then).Milliseconds())
}

func InitKinectGrpc(ID string) bool {
	addr := ID + ":40000"
	fmt.Println("Localhost IP:", addr)

	var err_grpc error
	conn, err_grpc = grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock())
	if err_grpc != nil {
		log.Fatal(err_grpc)
		return false
	}
	client = pb.NewYolo_KinectClient(conn)
	req = pb.Request{
		Check: true,
	}
	fmt.Println("InitKinectGrpc finished")

	return true
}

var Side bool
var Shirt bool

func getCommandParameters(package_ string, args_ *[7]int) int {

	splittedString := strings.Split(package_, ", ")
	splittedString1 := strings.Split(splittedString[0], "[")
	/*fmt.Println("\npackage_    ", package_)
	fmt.Println("\nsplittedString    ", splittedString)*/
	idx_cmd, _ := strconv.Atoi(splittedString1[1])
	args_[0], _ = strconv.Atoi(splittedString[1])
	args_[1], _ = strconv.Atoi(splittedString[2])
	args_[2], _ = strconv.Atoi(splittedString[3])
	args_[3], _ = strconv.Atoi(splittedString[4])
	args_[4], _ = strconv.Atoi(splittedString[5])
	args_[5], _ = strconv.Atoi(splittedString[6])
	splittedString2 := strings.Split(splittedString[7], "]")
	x, _ := strconv.Atoi(splittedString2[0])
	if x&2 == 2 {
		Side = true
	} else {
		Side = false
	}
	if x&1 == 1 {
		Shirt = true
	} else {
		Shirt = false
	}

	coms.SetFlagsBS(Side, Shirt)
	//fmt.Println("side", Side, Shirt, x, splittedString[7])
	robot_shirt = (x & 1)
	//fmt.Println(splittedString1[1], '\t', splittedString[1])
	/*fmt.Printf("%s,%s,%s,%s,%s\n", splittedString[1], splittedString[2],
	splittedString[3], splittedString[4], splittedString[5])*/
	return idx_cmd
}

func Skills(mode int, ID string, my_ip string, basestation_ip string, grpc_ip string, shirt int) {
	var s uint8

	fmt.Println("Skills")
	Robot_id, _ = strconv.Atoi(ID)

	OpenCalibrationConnection(my_ip, basestation_ip)

	//time.Sleep(100 * time.Millisecond)

	InitKinectGrpc(grpc_ip)
	defer conn.Close()
	fmt.Println("\n✅️🎥️  Kinect stream initialized", s, mode)

	/*if ID == "1" {
		go GK_P.GK_Position()
	}*/

	if mode == 0 {
		chan_quit := make(chan int)
		var args = [7]int{-2, -2, -2, -2, -2, -2, -2}
		fmt.Println("mode debug without basestation in")
		//skMove2(args, chan_quit)
		//skAtack(args, chan_quit)

		//skKick(args, chan_quit)
		////skAtack2()
		//skReceive(args, chan_quit)
		skDefend(args, chan_quit)
		//skRemoteControl()
	} else if mode == 1 {
		time.Sleep(5 * time.Second)

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
		fmt.Println("mode with basestation")
		first_time_running := true
		//wait_4_skill.Add(1)
		//	new_command := false
		for {
			//time.Sleep(1 * time.Millisecond)

			coms.BS_sync.Lock()
			coms.BS_sync.Cond.Wait()

			coms.BS_sync.Unlock()

			command = coms.BS_sync.Data
			//fmt.Println("skills", command)
			command_index := getCommandParameters(command, &args)

			//fmt.Println("--------skills--------", command_index, last_state)

			if command_index < 8 && command_index >= 0 {
				//fmt.Println("--------entrou1--------", command_index)
				if last_state != command_index || first_time_running {
					//fmt.Println("--------entrou2--------", command_index)
					last_state = command_index
					if !first_time_running {
						chan_quit <- 0
						fmt.Println("wainting skill exit")
						wait_4_skill.Wait()
					}

					//fmt.Println("entrou fiffrent skill")
					first_time_running = false
					wait_4_skill.Add(1)

					go fns[command_index](args, chan_quit)

				} else {

					//Fns_args <- args
					BS_args_mutex.Lock()
					BS_args = args
					BS_args_mutex.Unlock()
					//fmt.Println("entrou same skill")
					//fns_chan[command_index] <- false
					//fmt.Println("skill2345", len(Fns_args))
				}

			} else {
				fmt.Println("skill command value out of range", command_index)
			}
		}
		//}
	}
}

// NewPid() creates a new PID controller with the given constants and dt
func NewPid(kP, kI, kD, dt, outputLimit float64) *Pid {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	return &Pid{
		kP:          kP,
		kI:          kI,
		kD:          kD,
		dt:          dt,
		outputLimit: outputLimit,
	}
}

// SetPID() updates the PID controller variables with the given constants
func (p *Pid) SetPid(new_kP float64, new_kI float64, new_kD float64, new_outputLimit float64) {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	//fmt.Println("Old PID", *p)
	if new_kP < 0 {
		new_kP = 0
	}
	if new_kI < 0 {
		new_kI = 0
	}
	if new_kD < 0 {
		new_kD = 0
	}
	if new_outputLimit < 0 {
		new_outputLimit = 0
	} else if new_outputLimit > 100 {
		new_outputLimit = 100
	}
	p.kP = new_kP
	p.kI = new_kI
	p.kD = new_kD
	p.outputLimit = new_outputLimit
	//fmt.Println("New PID", *p)
}

// Update computes the new control output based on the current error and elapsed time
func (p *Pid) Update(erro float64, dt float64) float64 {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

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

// SetAtractor updates the atractor variables with the given constants
func (a *Atractor) SetAtractor(Katr float64, Kint float64, new_outputLimit float64) {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	//fmt.Println("Old Atractor", *a)
	if Katr < 0 {
		Katr = 0
	}
	if Kint < 0 {
		Kint = 0
	}
	if new_outputLimit < 0 {
		new_outputLimit = 0
	} else if new_outputLimit > 100 {
		new_outputLimit = 100
	}
	a.Katracao = Katr
	a.Kintensidade = Kint
	a.outputLimit = new_outputLimit
	//fmt.Println("New Atractor", *a)
}

// NewAtractor creates a new Atractor controller with the given constants and dt
func NewAtractor(Katracao, Kintensidade, outputLimit float64) *Atractor {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	return &Atractor{
		Katracao:     Katracao,
		Kintensidade: Kintensidade,
		outputLimit:  outputLimit,
	}
}

// Update computes the new control output based on the current error
func (a *Atractor) Update(erro float64) float64 {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	output := a.Katracao * math.Exp(erro*a.Kintensidade)

	if output > a.outputLimit {
		output = a.outputLimit
		fmt.Println(output, a.outputLimit)
	}

	return output
}

// SetReppeller updates the Reppeller variables with the given constants
func (r *Reppeller) SetReppeller(Krep float64, Kinf float64, new_outputLimit float64) {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	//fmt.Println("Old Atractor", *a)
	if Krep < 0 {
		Krep = 0
	}
	if Kinf < 0 {
		Kinf = 0
	}
	if new_outputLimit < 120 {
		new_outputLimit = 120
	}

	r.Kreppeller = Krep
	r.kinfluencia = Kinf
	r.outputLimit = new_outputLimit
	//fmt.Println("New Atractor", *a)
}

// NewPid creates a new PID controller with the given constants and dt
func NewReppeller(Kreppeller, kinfluencia, outputLimit float64) *Reppeller {
	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	return &Reppeller{
		Kreppeller:  Kreppeller,
		kinfluencia: kinfluencia,
		outputLimit: outputLimit,
	}
}

func (r *Reppeller) Update(obstacles []coms.Robot_st, target_dist int, direction int) int {
	//skills_configs_mutex.Lock()
	//defer skills_configs_mutex.Unlock()
	dir_desvio := 0.0

	for _, opp := range obstacles {
		//fmt.Println("opponent", idx, opp)
		if opp.Distance+50 < int(target_dist) {

			ang_desvio := direction - opp.Angle
			fmt.Println("ang_desvio", ang_desvio)
			if ang_desvio >= -2 && ang_desvio <= 2 {
				ang_desvio = 15
			}
			if ang_desvio > -50 && ang_desvio < 50 {
				dir_desvio -= (r.Kreppeller * float64(ang_desvio) *
					math.Exp(-(math.Pow(float64((ang_desvio)), 2) / (2 * math.Pow(r.kinfluencia, 2))))) *
					float64(150.0/(150.0+float64(opp.Distance)))
			}
		}
	}
	if dir_desvio > r.outputLimit {
		dir_desvio = r.outputLimit
	} else if dir_desvio < (-r.outputLimit) {
		dir_desvio = -r.outputLimit
	}
	fmt.Println("\n-------dir desvio", dir_desvio)
	fmt.Println("-------reppeller", *r)
	return (direction - int(dir_desvio))

}

func norm_rad(radianos *float64) {
	for *radianos > math.Pi {
		*radianos -= 2 * math.Pi
	}
	for *radianos < (-math.Pi) {

		*radianos += 2 * math.Pi
	}
}
func OrbitarBola(lado int, ball_angle int) int {

	angulo := (float64(ball_angle - 90.0)) * math.Pi / 180.0
	//  printf("\nangulo=%.4lf ", angulo*180.0/M_PI);

	switch lado {
	case 0: // na zona central do campo (lado mais perto)

		if angulo > math.Pi/2 || math.Pi < (-math.Pi/2) {
			angulo += math.Pi
		}
		break

	case 1: // lado direito
		angulo += math.Pi
		break
	case -1: // lado esquerdo
		break
	}
	norm_rad(&angulo)
	direccao := int((0.5 + angulo*180.0/math.Pi))
	if direccao < 0 {
		direccao += 360
	}
	return direccao
	// printf("lado=%d Nangulo=%.4f direccao=%d\n", lado, angulo*180.0/M_PI, direccao);
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

func (pid *Pid) sk_orientation2(time_ float64, ball_pos2 position) int {
	fmt.Println("Orientation2")
	//ori_pid_kinect := NewPid(0.045, 0.035, 0.015, 0.05, 80)

	if ball_pos2.X != -1 {

		erro := float64(ball_pos2.X - 315)
		rot := pid.Update(erro, time_)
		fmt.Println(" \nerro:  ", erro, rot)

		return int(rot)
	}
	return 0
}

func getAngleRelativeToRobot(objectX float64, objectY float64, depthMM float64) float64 {

	angle_per_pixel := 0.09375
	// Calculate angle in the horizontal plane
	var angle_ float64
	pixel_distance := objectX - 320
	angle_ = float64(pixel_distance) * angle_per_pixel
	//fmt.Println("Pixel", objectX, objectY, " corresponds to an angle of", angle_)
	return (-angle_)
}

func getRelativeAngleTrajectory(previousX float64, previousY float64, objectX float64, objectY float64) float64 {
	var dx float64
	var dy float64

	dx = previousX - objectX

	dy = previousY - objectY
	ang := math.Atan2(dx, dy)
	ang = ang * 180 / math.Pi
	fmt.Println("\ndx", dx, "dy", dy, "ang", ang)
	return ang
}

func reppelFromObstacles(direction int, displacement float64, obstacles []coms.Robot_st) int {
	//repeller implementation

	//if db.Opponent != nil || ball_as_repeller == 1 {
	/*fmt.Println("direction atractor", direction)
	fmt.Println("db.Opponent[0]", db.Opponent[0])
	fmt.Println("direction-db.Opponent[0].Angle", direction-db.Opponent[0].Angle)
	fmt.Println("db.Opponent[0].Angle", db.Opponent[0].Angle)
	fmt.Println("db.Opponent[0].Distance", db.Opponent[0].Distance)
	fmt.Println(float64(100.0 / (100.0 + float64(db.Opponent[0].Distance))))*/
	dir_desvio := 0.0

	//fmt.Println(obstacles)
	for _, opp := range obstacles {
		//fmt.Println("opponent", idx, opp)
		if opp.Distance+50 < int(displacement) {

			ang_desvio := direction - opp.Angle
			if ang_desvio >= -2 && ang_desvio <= 2 {
				ang_desvio = 10
			}
			if ang_desvio > -40 && ang_desvio < 40 {
				dir_desvio -= (4.5 * float64(ang_desvio) * math.Exp(-(math.Pow(float64((ang_desvio)), 2) / (2 * math.Pow(25, 2))))) * float64(150.0/(150.0+float64(opp.Distance)))
			}
		}
	}
	if dir_desvio > 100 {
		dir_desvio = 100
	} else if dir_desvio < (-100) {
		dir_desvio = -100
	}
	fmt.Println("------------------dir desvio", dir_desvio)
	return int(dir_desvio)
	//}end of reppeller implementation

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
func obtain_lateral(ball_1x float64, ball_2x float64, dist1 float64, dist2 float64) (ball_side float64, side int) {
	//inicialize variables
	var horizontal_dist1 = 0.0
	var horizontal_dist2 = 0.0
	var vertical_dist1 = 0.0
	var vertical_dist2 = 0.0

	//obtain the horizontal distance of the balls to the center of the image (pixels)
	var dist_middle_1 = -((640 / 2) - ball_1x)
	var dist_middle_2 = -((640 / 2) - ball_2x)

	//obtain the angle between the balls and the center
	var horizontal_degrees_1 = dist_middle_1 * horizontal_cam / 640
	var horizontal_degrees_2 = dist_middle_2 * horizontal_cam / 640

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

type address struct {
	ip   string
	port string
}

func OpenCalibrationConnection(my_ip string, basestation_ip string) {
	var err error

	fmt.Println("OHHHH bORRRRO")
	serverAdrString := address{ip: basestation_ip, port: bs_send_ports_calib[Robot_id-1]}
	robotAdrString := []address{{ip: my_ip, port: receive_ports_calib[Robot_id-1]}}
	fmt.Println(robotAdrString, serverAdrString)
	/*for i := 0; i < numberOfRobots; i++ {
		robotAddresses[i], _ = net.ResolveUDPAddr("udp", robotAdrString[i].ip+":"+robotAdrString[i].port)
		fmt.Println(robotAddresses[i])
	}*/
	//fmt.Println("TA")
	//serverConnection, _ := net.ListenUDP("udp", serverAddress)
	ServerAddr_, err := net.ResolveUDPAddr("udp", serverAdrString.ip+":"+serverAdrString.port)
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}
	//fmt.Println("TA2")
	remoteAddr_, err := net.ResolveUDPAddr("udp", robotAdrString[0].ip+":"+robotAdrString[0].port)
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}

	//fmt.Println("TA4")
	Conn, err := net.DialUDP("udp", remoteAddr_, ServerAddr_)
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}
	//fmt.Println("TA5")

	//set all players default
	go recieveCalibration(Conn, ServerAddr_)
}

func recieveCalibration(conn *net.UDPConn, ServerAddr_ *net.UDPAddr) {
	fmt.Println("📡️  Basestation callback recieveCalibration")
	buffer := make([]byte, 1024)

	for {
		buffer = make([]byte, 1024)
		//fmt.Println("                          fiqei")
		//n, addr, errororor := conn.ReadFrom(buffer)
		_, _, _ = conn.ReadFrom(buffer)

		//fmt.Println("fiqei", string(buffer))

		if buffer[0] == 54 && buffer[1] == 56 {
			SendPIDvalues(conn)
		} else if buffer[0] == 54 && buffer[1] == 57 {
			SaveSkillsCalibratedValues()
		} else {
			conn.Write(buffer)
			DecodePids(buffer, conn)
		}
	}
}

func DecodePids(buff []byte, conn *net.UDPConn) {
	//fmt.Println("\nreceive new pids", string(buff))
	splittedString := strings.Split(string(buff), ", ")
	splittedString1 := strings.Split(splittedString[0], "[")
	splittedString2 := strings.Split(splittedString[len(splittedString)-1], "]")

	//
	// fmt.Println("\npackage_    ", package_)
	// fmt.Println("\nsplittedString    ", splittedString)
	//
	idx_cmd, _ := strconv.Atoi(splittedString1[0])
	//idx_cmd := 0

	args_calibration[0], _ = strconv.ParseFloat(splittedString1[1], 64)

	for i := 1; i < len(splittedString)-1; i++ {
		args_calibration[i], _ = strconv.ParseFloat(splittedString[i], 64)
		//fmt.Println("args", i, args_calibration[i])
	}

	args_calibration[10], _ = strconv.ParseFloat(splittedString2[0], 64)

	switch idx_cmd {
	case 0: //Stop
		{
		}
	case 1: //Move
		{
			//aux_kP, aux_kI, aux_kD, aux_outputLimit := args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100

			move_orientation.SetPid(args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100)
			idx := 4
			speed_atractor.SetAtractor(args_calibration[idx+0], args_calibration[idx+1], args_calibration[idx+2]*100)
			idx = 7
			direction_reppeler.SetReppeller(args_calibration[idx+0]*10, args_calibration[idx+1]*10, args_calibration[idx+2]*100)
		}
	case 2: //Atack
		{
			atack_orientation.SetPid(args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100)
			idx := 4
			atack_atractor.SetAtractor(args_calibration[idx+0], args_calibration[idx+1], args_calibration[idx+2]*100)

		}
	case 3: //Kick
		{
			//fmt.Println("recienving new pid",args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100)
			kick_orientation.SetPid(args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100)
			//idx := 4
			//kick_atractor.SetAtractor(args_calibration[idx+0], args_calibration[idx+1], args_calibration[idx+2]*100)

		}
	case 4: //Receive
		{
			receive_orientation.SetPid(args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100)
			idx := 4
			receive_linear_mov.SetPid(args_calibration[idx+0], args_calibration[idx+1], args_calibration[idx+2], args_calibration[idx+3]*100)
		}
	case 5: //Cover
		{
			//SaveSkillsCalibratedValues2()
			SaveSkillsCalibratedValues()

		}
	case 6: //Defend
		{
			A = args_calibration[0] * 1000
			B = args_calibration[1] * 1000
			idx := 2
			place_atractor.SetAtractor(args_calibration[idx], args_calibration[idx+1], args_calibration[idx+2]*100)
			idx = 5
			defend_atractor.SetAtractor(args_calibration[idx+0], args_calibration[idx+1], args_calibration[idx+2]*100)

		}
	case 7: //Control
		{
			rmt_ctrl_orientation.SetPid(args_calibration[0], args_calibration[1], args_calibration[2], args_calibration[3]*100)
			idx := 4
			receive_linear_mov.SetPid(args_calibration[idx+0], args_calibration[idx+1], args_calibration[idx+2], args_calibration[idx+3]*100)

		}
	case 68:
		{
			SendPIDvalues(conn)
		}

	}
	new_pid_received = true

}

func SaveSkillsCalibratedValues() {
	filename := "skills/Skill_configs_Robot.go"
	fmt.Println("filename:", filename)
	//log.Fatal(err)
	f, err := os.OpenFile(filename, os.O_RDWR, 777)
	if err != nil {
		f, err = os.Create(filename)

		if err != nil {
			log.Fatal(err)
		}
		//fmt.Println(err.Error())
	}

	defer f.Close()

	skills_configs_mutex.Lock()
	defer skills_configs_mutex.Unlock()

	str := "package skills\n"

	str += "\n/*\nAtack variables\n*/\n"
	str += fmt.Sprintf("const Kp_atack = %.3f\nconst Ki_atack = %.3f\nconst Kd_atack = %.3f\nconst outputLimit_PID_atack = %.3f\nconst Katracao_atack = %.3f\nconst Kintensidade_atack = %.3f\nconst outputLimit_atractor_atack = %.3f\n",
		atack_orientation.kP,
		atack_orientation.kI,
		atack_orientation.kD,
		atack_orientation.outputLimit,
		atack_atractor.Katracao,
		atack_atractor.Kintensidade,
		atack_atractor.outputLimit)

	str += "\n/*\nReceive variables\n*/\n"
	str += fmt.Sprintf("const Kp_receive_rot = %.3f\nconst Ki_receive_rot = %.3f\nconst Kd_receive_rot = %.3f\nconst outputLimit_PID_receive_rot = %.3f",
		receive_orientation.kP,
		receive_orientation.kI,
		receive_orientation.kD,
		receive_orientation.outputLimit)

	str += fmt.Sprintf("\nconst Kp_receive_vel = %.3f\nconst Ki_receive_vel = %.3f\nconst Kd_receive_vel = %.3f\nconst outputLimit_PID_receive_vel = %.3f",
		receive_linear_mov.kP,
		receive_linear_mov.kI,
		receive_linear_mov.kD,
		receive_linear_mov.outputLimit)

	str += fmt.Sprintf("\nconst Katracao_receive = %.3f\nconst Kintensidade_receive = %.3f\nconst outputLimit_atractor_receive = %.3f\n",
		0.0,
		0.0,
		0.0)
	str += "\n/*\nMove variables\n*/\n"

	str += fmt.Sprintf("const Kp_move = %.3f\nconst Ki_move = %.3f\nconst Kd_move = %.3f\nconst outputLimit_PID_move = %.3f",
		move_orientation.kP,
		move_orientation.kI,
		move_orientation.kD,
		move_orientation.outputLimit)

	str += fmt.Sprintf("\nconst Katracao_move = %.3f\nconst Kintensidade_move = %.3f\nconst outputLimit_atractor_move = %.3f\n",
		speed_atractor.Katracao,
		speed_atractor.Kintensidade,
		speed_atractor.outputLimit)

	str += fmt.Sprintf("\nconst Krepulsao_move = %.3f\nconst Kinfluencia_move = %.3f\nconst outputLimit_reppeller_move = %.3f\n",
		direction_reppeler.Kreppeller,
		direction_reppeler.kinfluencia,
		direction_reppeler.outputLimit)
	str += "\n/*\nKick variables\n*/\n"

	str += fmt.Sprintf("const Kp_kick = %.3f\nconst Ki_kick = %.3f\nconst Kd_kick = %.3f\nconst outputLimit_PID_kick = %.3f",
		kick_orientation.kP,
		kick_orientation.kI,
		kick_orientation.kD,
		kick_orientation.outputLimit)
	str += fmt.Sprintf("\nconst Katracao_kick = %.3f\nconst Kintensidade_kick = %.3f\nconst outputLimit_atractor_kick = %.3f\n",
		0.0,
		0.0,
		0.0)
	str += "\n/*\nCover variables\n*/\n"

	str += fmt.Sprintf("const Kp_cover = %.3f\nconst Ki_cover = %.3f\nconst Kd_cover = %.3f\nconst outputLimit_PID_cover = %.3f",
		0.0,
		0.0,
		0.0,
		0.0)
	str += fmt.Sprintf("\nconst Katracao_cover = %.3f\nconst Kintensidade_cover = %.3f\nconst outputLimit_atractor_cover = %.3f\n\n",
		0.0,
		0.0,
		0.0)

	str += "\n/*\nDefend variables\n*/\n"

	str += fmt.Sprintf("const A_ellipse = %.3f\nconst B_ellipse = %.3f\nconst Katracao_place = %.3f\nconst Kintensidade_place = %.3f\nconst outputLimit_atractor_place = %.3f",
		A,
		B,
		place_atractor.Katracao,
		place_atractor.Kintensidade,
		place_atractor.outputLimit)
	str += fmt.Sprintf("\nconst Katracao_defend = %.3f\nconst Kintensidade_defend = %.3f\nconst outputLimit_atractor_defend = %.3f\n\n",
		defend_atractor.Katracao,
		defend_atractor.Kintensidade,
		defend_atractor.outputLimit)
	str += "\n/*\nRemote Control variables\n*/\n"

	str += fmt.Sprintf("const Kp_remoteControl = %.3f\nconst Ki_remoteControl = %.3f\nconst Kd_remoteControl = %.3f\nconst outputLimit_PID_remoteControl = %.3f",
		rmt_ctrl_orientation.kP,
		rmt_ctrl_orientation.kI,
		rmt_ctrl_orientation.kD,
		rmt_ctrl_orientation.outputLimit)
	str += fmt.Sprintf("\nconst Katracao_remoteControl = %.3f\nconst Kintensidade_remoteControl = %.3f\nconst outputLimit_atractor_remoteControl = %.3f\n\n",
		0.0,
		0.0,
		0.0)

	_, err2 := f.WriteString(str)
	if err2 != nil {
		log.Fatal(err2)
	}
	fmt.Println("done")
}

func SendPIDvalues(conn *net.UDPConn) {
	buffer := []byte(fmt.Sprintf("[%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v]",
		Kp_move,
		Ki_move,
		Kd_move,
		outputLimit_PID_move/100,
		Katracao_move,
		Kintensidade_move,
		outputLimit_atractor_move/100,
		Krepulsao_move/10,
		Kintensidade_receive/10,
		outputLimit_atractor_receive/100,
		0.0,

		Kp_atack,
		Ki_atack,
		Kd_atack,
		outputLimit_PID_atack/100,
		Katracao_atack,
		Kintensidade_atack,
		outputLimit_atractor_atack/100,
		0.0,
		0.0,
		0.0,
		0.0,

		Kp_kick,
		Ki_kick,
		Kd_kick,
		outputLimit_PID_kick/100,
		Katracao_kick,
		Kintensidade_kick,
		outputLimit_atractor_kick/100,
		0.0,
		0.0,
		0.0,
		0.0,

		Kp_receive_rot,
		Ki_receive_rot,
		Kd_receive_rot,
		outputLimit_PID_receive_rot/100,
		Kp_receive_vel,
		Ki_receive_vel,
		Kd_receive_vel,
		outputLimit_PID_receive_vel/100,
		Katracao_receive,
		Kintensidade_receive,
		outputLimit_atractor_receive/100,

		Kp_cover,
		Ki_cover,
		Kd_cover,
		outputLimit_PID_cover/100,
		Katracao_cover,
		Kintensidade_cover,
		outputLimit_atractor_cover/100,
		0.0,
		0.0,
		0.0,
		0.0,

		A_ellipse/1000,
		B_ellipse/1000,
		Katracao_place,
		Kintensidade_place,
		outputLimit_atractor_place/100,
		Katracao_defend,
		Kintensidade_defend,
		outputLimit_atractor_defend/100,
		0.0,
		0.0,
		0.0,

		Kp_remoteControl,
		Ki_remoteControl,
		Kd_remoteControl,
		outputLimit_PID_remoteControl/100,
		Katracao_remoteControl,
		Kintensidade_remoteControl,
		outputLimit_atractor_remoteControl/100,
		0.0,
		0.0,
		0.0,
		0.0,
	))

	_, _ = conn.Write(buffer)
	/*for validation != nil {
		fmt.Println(buffer)
		nmr, validation = conn.Write(buffer)
		fmt.Println(nmr, validation, "\n")
	}*/
}
