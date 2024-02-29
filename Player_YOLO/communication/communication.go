package communication

import (
	//"bufio"

	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/xuri/excelize/v2"
	"go.bug.st/serial"
)

const BS_COMS_TIMEOUT = 40

// serial port init variables
const baudrate = 115200

const (
	CMD_driblers   int = 0
	CMD_omni_speed int = 1
	CMD_omni_gains int = 2
	CMD_all        int = 3
)

// each robots variables
type Robot_st struct {
	Coords      position
	Orientation int //PROPRIO - bussola
	Angle       int // Relative ANGLE
	Distance    int // Relative Distance
	Conf        int //Confidence

	//Ball        bool
}
type Ball_st struct {
	Coords position
	Angle  int
	Dist   int
	Status int // DRIBBLER STATE
	Conf   int //Confidence
}
type LocalDB struct {
	Team       []Robot_st
	Opponent   []Robot_st
	Ball       Ball_st
	Relocation bool
	Shirt      bool
	Side       bool
}

// struct variables for communication with Basestation
type address struct {
	ip   string
	port string
}

type position struct {
	X float64
	Y float64
	Z float64
}

type robot struct {
	adr   address
	pos   position
	state int
}

// struct with variables to receive from esp32 - HM controller
type EspToMsi struct {
	Battery_12v     int //SEND TO BS
	Battery_24v     int //SEND TO BS
	QC1             int //SEND TO BS
	QComni          int //SEND TO BS
	Cap             int //SEND TO BS
	Bussola_bearing int
	vel_db_r        int
	vel_db_l        int
	disp_db_r       int
	disp_db_l       int
	OMNI_temp       int
	Dips_X          int
	Dips_Y          int
	Ball_status     int
	Buttons         int //3 bits MSB Relocation -> Dribblers -> Repair  LSB
}

// struct with variables to send to esp32 - HM controller
type MsiToEsp struct {
	Velocity  int
	Angular   int
	Direction int
}
type Data_ESP_st struct {
	EspToMsi_info EspToMsi
	MsiToEsp_info MsiToEsp
}
type BS_sync_st struct {
	sync.Mutex
	Data string

	Cond *sync.Cond
}

// Variables for all robots informations and ball
var database LocalDB
var Data_ESP Data_ESP_st
var dtbase_mutex sync.Mutex
var ESP_mutex sync.Mutex // ESP -> PC

var basestaion_mutex sync.Mutex

// Port variable for serial communication
var port serial.Port
var pi_port serial.Port

var Esp_commands = []string{"driblers", "omni_speed", "omni_gains", "all"}

//192.168.31.79 meu IP
//

// variables for vommunication with Basesetation
var serverAdrString address
var robotAdrString []address
var LocalAdrString []address
var my_send_ports = []string{"21011", "21021", "21031", "21041", "21051"}
var bs_send_ports = []string{"21010", "21020", "21030", "21040", "21050"}
var receive_ports = []string{"20110", "20120", "20130", "20140", "20150"}

var New_BS_command bool

var BS_commands string
var idx_exel int
var delta_cicle_coms float64
var commit_ID int
var coms_test int

var Skill_loop_time int

//var BS_commands_chan = make(chan string, 10)

var BS_sync = NewCondVar()

// function definition for receive commands from Basestation and store them on a string array
func NewCondVar() *BS_sync_st {
	r := BS_sync_st{}
	r.Cond = sync.NewCond(&r)
	return &r
}
func SetLoopTime(time_aux int) {
	Skill_loop_time = time_aux
}

func recieve(conn *net.UDPConn) {
	fmt.Println("📡️  Basestation callback")
	//var receive_now time.Time
	//var receive_time time.Time

	buffer := make([]byte, 1024)
	for {
		//fmt.Println(  strings.Compare(string(buffer), "q"))
		for strings.Compare(string(buffer), "q") == -1 {
			buffer = make([]byte, 1024)

			_, _, coms_error := conn.ReadFromUDP(buffer)

			if coms_error != nil {
				for {
					fmt.Println("❌️🔔️", coms_error)
				}
			}

			//fmt.Println("receive", string(buffer))

			BS_sync.Lock()
			BS_sync.Data = string(buffer)
			BS_sync.Unlock()

			BS_sync.Cond.Signal()
			//fmt.Println("----------after receive---------")

		}
	}
}

func GetBS_params() (int, int, int, int) {

	splittedString := strings.Split(BS_commands, ", ")

	dx, _ := strconv.Atoi(splittedString[1])
	dy, _ := strconv.Atoi(splittedString[2])
	ori, _ := strconv.Atoi(splittedString[3])
	kick, _ := strconv.Atoi(splittedString[4])

	return dx, dy, ori, kick
}

// function definition for receive commands from Basestation
func GetBS_Command(BS_cmd *string) {
	basestaion_mutex.Lock()
	*BS_cmd = BS_commands
	basestaion_mutex.Unlock()
	//fmt.Print("BaseStation_cmd")
	//fmt.Println(*BS_cmd)
}

// function to put player default

func SetBallPosition(ball Ball_st) {
	dtbase_mutex.Lock()
	database.Ball = ball
	dtbase_mutex.Unlock()
}

func SetFlagsBS(side bool, shirt bool) {
	dtbase_mutex.Lock()
	database.Side = side
	database.Shirt = shirt
	dtbase_mutex.Unlock()
}

func GetBallStatus() int {
	ESP_mutex.Lock()
	defer ESP_mutex.Unlock()

	return Data_ESP.EspToMsi_info.Ball_status
}

func GetButtons(buttons *int, shirt *bool, side *bool) {
	ESP_mutex.Lock()
	*buttons = Data_ESP.EspToMsi_info.Buttons
	ESP_mutex.Unlock()
	dtbase_mutex.Lock()
	*side = database.Side
	*shirt = database.Shirt
	dtbase_mutex.Unlock()
}

func SetRobotsPositions(robots_t []Robot_st, robots_o []Robot_st) {

	dtbase_mutex.Lock()
	database.Team = robots_t
	database.Opponent = robots_o
	dtbase_mutex.Unlock()

}

func SetDatabase(db LocalDB) {

	dtbase_mutex.Lock()
	database = db
	dtbase_mutex.Unlock()
}

// idx goes from 0 to 9, where teammates from 0 to 4 and opponents from 5 to 9
func GetRobot(idx int, robot *Robot_st) {
	dtbase_mutex.Lock()
	*robot = database.Team[idx]
	dtbase_mutex.Unlock()
}

// idx goes from 0 to 9, where teammates from 0 to 4 and opponents from 5 to 9
func GetTeamOfRobots(idx bool, robots *[]Robot_st) {
	dtbase_mutex.Lock()
	if idx {
		*robots = database.Opponent
		dtbase_mutex.Unlock()
		return
	}
	*robots = database.Team
	dtbase_mutex.Unlock()

}

func GetDatabase(db *LocalDB) {
	dtbase_mutex.Lock()
	*db = database
	dtbase_mutex.Unlock()
}

func GetBallPosition(pos *Ball_st) {
	dtbase_mutex.Lock()
	*pos = database.Ball
	dtbase_mutex.Unlock()

}

func Get_bussola() int {
	ESP_mutex.Lock()

	aux := Data_ESP.EspToMsi_info.Bussola_bearing
	ESP_mutex.Unlock()

	return aux

}

func GetDisplacement() (int, int) {
	ESP_mutex.Lock()
	defer ESP_mutex.Unlock()
	rtn_x := Data_ESP.EspToMsi_info.Dips_X
	rtn_y := Data_ESP.EspToMsi_info.Dips_Y
	Data_ESP.EspToMsi_info.Dips_X = 0 //Clean Encoders value
	Data_ESP.EspToMsi_info.Dips_Y = 0
	return rtn_x, rtn_y
}

func SendESP_Parameters(aux MsiToEsp) {

	command := "R" + strconv.Itoa(aux.Velocity) + "," + strconv.Itoa(aux.Angular) +
		"," + strconv.Itoa(aux.Direction)
	sendPackage(command)
}

func SendCommandToESP(cmd_type int, params ...interface{}) {

	switch cmd_type {

	case 0: //driblers values
		{ // db1, db2
			command := fmt.Sprintf("D,%v\n", params[0].(int))
			sendPackage(command)
		}
	case 1: //omni speeds values
		{ //linear speed, rotational speed, direction
			command := fmt.Sprintf("M,%v,%v,%v\n", params[0].(int), params[1].(int), params[2].(int))
			sendPackage(command)
		}
	case 2: //omni speeds values
		{ //Kp, Ki , Kd
			command := fmt.Sprintf("P,%v,%v,%v\n", params[0].(int), params[1].(int), params[2].(int))
			sendPackage(command)
		}
	case 3: //omni, dribserverConnectionlers, kick values
		{ //linear speed, rotational speed, direction, db1, db2, KickTime

			dribblers_en := params[3].(int)
			if params[3].(int) != 1 {
				dribblers_en = 0
			}
			command := fmt.Sprintf("C,%v,%v,%v,%v,%v\n", params[0].(int), params[1].(int), params[2].(int), dribblers_en, params[len(params)-1].(int))
			//fmt.Println(".........sending............ ", command)
			sendPackage(command)
			Data_ESP.MsiToEsp_info.Velocity = params[0].(int)  //strconv.Atoi(string(params[0], 10, 0)
			Data_ESP.MsiToEsp_info.Angular = params[1].(int)   //strconv.Atoi(params[1])
			Data_ESP.MsiToEsp_info.Direction = params[2].(int) //strconv.Atoi(params[2])
			//command := "R" + strconv.Itoa(aux.Velocity) + "," + strconv.Itoa(aux.Angular) +
			//	"," + strconv.Itoa(aux.Direction)
		}
	}

}

func OpenSerial(ttyUSB_NAME_ string) bool {
	var err error
	port, err = serial.Open(ttyUSB_NAME_, &serial.Mode{})
	if err != nil {
		fmt.Println("Error: ", err)
		return false
	}

	//config serial communication with esp32 parameters
	config := serial.Mode{
		BaudRate: baudrate,
		Parity:   serial.NoParity,
		DataBits: 8,
		StopBits: serial.OneStopBit,
	}

	err = port.SetMode(&config)
	if err != nil {
		fmt.Println("Error: ", err)
		return false
	}
	fmt.Println("📲️ Serial Comunication initialized")
	return true
}

func OpenPiPico() bool {
	var err error
	pi_port, err = serial.Open("/dev/ttyACM0", &serial.Mode{})
	if err != nil {
		fmt.Println("Error: ", err)
	}

	//config serial communication with esp32 parameters
	config := serial.Mode{
		BaudRate: baudrate,
		Parity:   serial.NoParity,
		DataBits: 8,
		StopBits: serial.OneStopBit,
	}

	err = pi_port.SetMode(&config)
	if err != nil {
		fmt.Println("Error: ", err)
		return false
	}
	fmt.Println("📲️🍓 Serial Comunication with Pi Pico initialized")
	return true
}

func InitWorldIps(my_id string, my_ip string, bs_ip string) {

	id, _ := strconv.Atoi(my_id)
	serverAdrString = address{ip: bs_ip, port: bs_send_ports[id-1]}
	robotAdrString = []address{{ip: my_ip, port: receive_ports[id-1]}}

	LocalAdrString = []address{{ip: my_ip, port: my_send_ports[id-1]}}

}

func OpenServerConnection(remoteAddr_, LocalAddr_, ServerAddr_ *net.UDPAddr) (*net.UDPConn, *net.UDPConn, bool) {
	var err error

	ServerAddr_, err = net.ResolveUDPAddr("udp", serverAdrString.ip+":"+serverAdrString.port)
	if err != nil {
		fmt.Println("Error: ", err)
		return nil, nil, false
	}
	//fmt.Println("TA2")
	remoteAddr_, err = net.ResolveUDPAddr("udp", robotAdrString[0].ip+":"+robotAdrString[0].port)
	if err != nil {
		fmt.Println("Error: ", err)
		return nil, nil, false
	}
	//fmt.Println("TA3")
	LocalAddr_, err = net.ResolveUDPAddr("udp", LocalAdrString[0].ip+":"+LocalAdrString[0].port)
	if err != nil {
		fmt.Println("Error: ", err)
		return nil, nil, false
	}
	//fmt.Println("TA4")
	Conn, err := net.DialUDP("udp", LocalAddr_, ServerAddr_)
	if err != nil {
		fmt.Println("Error: ", err)
		return nil, nil, false
	}
	//fmt.Println("TA5")
	Conn_, _ := net.ListenUDP("udp", remoteAddr_)
	fmt.Println("📡️ Connected to Basestation")

	//set all players default

	return Conn, Conn_, true
}

func sendPackage(msg string) {
	//esp_com_mutex.Lock()
	//fmt.Println("passou mutex send package", msg)
	if port != nil {
		_, err := port.Write([]byte(msg))
		if err != nil {
			//esp_com_mutex.Unlock()
			log.Fatal(err)
			fmt.Println("passou mutex send ")
		}
	}
	//esp_com_mutex.Unlock()
}

func SendDefend(msg string) {
	//esp_com_mutex.Lock()
	//fmt.Println("passou mutex send package", msg)
	if pi_port != nil {
		_, err := pi_port.Write([]byte(msg))
		fmt.Print(pi_port.Write([]byte(msg)))
		if err != nil {
			log.Fatal(err)
		}
	}
	//esp_com_mutex.Unlock()
}

func Communication(ttyUSB_NAME_ string, my_id string, my_ip string, basestation_ip string, mode int) {
	fmt.Println("Communication initialized" + ttyUSB_NAME_)
	var Conn_Tx *net.UDPConn
	var remoteAddr, LocalAddr, ServerAddr *net.UDPAddr
	var BS_coms_flag bool
	//time.Sleep(100 * time.Millisecond)
	idx := 0
	ok := OpenSerial("/dev/" + ttyUSB_NAME_)
	for !ok {
		fmt.Println("Trying to open port" + "/dev/" + ttyUSB_NAME_)
		time.Sleep(500 * time.Millisecond)
		ok = OpenSerial("/dev/" + ttyUSB_NAME_)
	}

	if my_id == "1" {
		ok = OpenPiPico()
		for !ok {
			fmt.Println("Trying to open Pipico port" + "/dev/" + ttyUSB_NAME_)
			time.Sleep(500 * time.Millisecond)
			ok = OpenPiPico()
		}
		SendDefend("Defend\n\r")
	}

	if idx >= 9 {
		fmt.Println("Communication not initialized")
	}
	//var AUX_Conn_Rx *net.UDPConn
	if mode == 1 {
		InitWorldIps(my_id, my_ip, basestation_ip)
		//fmt.Println("mode == 1 . westheyrrrrrrrrryhe5yhersdfg4w.")
		Conn_Tx_aux, Conn_Rx, valid := OpenServerConnection(remoteAddr, LocalAddr, ServerAddr)
		Conn_Tx = Conn_Tx_aux
		//AUX_Conn_Rx = Conn_Rx
		BS_coms_flag = false
		if valid {
			fmt.Println("🖥️🔗️ BaseStation Conected sucessfully", Conn_Rx)
			BS_coms_flag = true
			go recieve(Conn_Rx)
		}
	}
	scanner := bufio.NewScanner(port)
	//recieve(Conn_)
	//fmt.Print(scanner, BS_coms_flag)
	go espScanner(scanner)
	//timercom := time.NewTimer(50 * time.Millisecond ) // init timer communication to db
	var last_time time.Time
	var time_now time.Time

	//ticker := time.NewTicker(BS_COMS_TIMEOUT * time.Millisecond)
	//defer ticker.Stop()

	for {
		//<-ticker.C

		//fmt.Println("Triggered at", time.Now(), BS_coms_flag)
		//fmt.Println("\ntime lap Basestation communication ", float64(time_now.Sub(last_time).Milliseconds()))
		time_now = time.Now()
		if BS_coms_flag && !(float64(time_now.Sub(last_time).Milliseconds()) < 40) {
			delta_cicle_coms = float64(time_now.Sub(last_time).Milliseconds())
			last_time = time_now
			sendCmdToBasestation(Conn_Tx)
		}

		/*if scanner.Scan() {
			updateLocalDB(string(scanner.Text()))
		}*/
	}

}

func espScanner(scanner *bufio.Scanner) {
	//fmt.Println("espScanner.............................")
	//var old_time time.Time
	//var current_time time.Time
	for {
		if scanner.Scan() {
			//esp_com_mutex.Lock()
			//current_time = time.Now()
			//fmt.Println("espScanner  ANTES")
			updateLocalDB(string(scanner.Text()))
			//fmt.Println("espScanner  DEPOIS")
			//fmt.Println("tempo coms:", float64(current_time.Sub(old_time).Seconds()))
			//old_time = time.Now()
			//esp_com_mutex.Unlock()
		}
	}
}

func sendCmdToBasestation(Conn *net.UDPConn) {
	i := 0

	//for {
	message := encodeBstationMsg()
	i++
	buf := []byte(message)
	_, err := Conn.Write(buf)
	//fmt.Println("Sending to B.station...\t\n", buf)
	if err != nil {
		fmt.Println("\n📡️😡️  ", err)
	}
	//time.Sleep(time.Second * 1)
	//}
}

/*
Battery_12v        int //SEND TO BS
Battery_24v        int //SEND TO BS
QC1		   int //SEND TO BS
QComni		   int //SEND TO BS
Cap                int //SEND TO BS
Bussola_bearing	   int
linear_vel	   int
angular_vel 	   int
direction int
vel_db_r int
vel_db_l int
disp_db_r int
disp_db_l int
OMNI_temp       int
Dips_X          int
Dips_Y          int
*/
func encodeBstationMsg() string {

	dtbase_mutex.Lock()
	copy_database := database
	dtbase_mutex.Unlock()

	ESP_mutex.Lock()
	copy_Data_ESP := Data_ESP
	ESP_mutex.Unlock()

	coms_test++
	coms_test &= 127
	// BALL -> X, Y, Z, Angle, Distance Ball State
	str := fmt.Sprintf("[%v,%v,%v,%v,%v,%v];[",
		copy_database.Ball.Coords.X,
		copy_database.Ball.Coords.Y,
		copy_database.Ball.Conf,
		copy_database.Ball.Angle,
		copy_database.Ball.Dist,
		Data_ESP.EspToMsi_info.Ball_status)
	// TEAM -> X, Y, Z, Confidence (Orientation), Angle(0), Distance(0)   () = self-robot
	for _, Player := range copy_database.Team {
		str += fmt.Sprintf("[%v,%v,%v,%v,%v,%v],",
			Player.Coords.X,
			Player.Coords.Y,
			Player.Conf,
			Player.Orientation,
			Player.Angle,
			Player.Distance)
	}

	str += "];["
	// OPPONENT -> X, Y, Z, Confidence, Angle, Distance
	for _, Player := range copy_database.Opponent {
		str += fmt.Sprintf("[%v,%v,%v,%v,%v,%v],",
			Player.Coords.X,
			Player.Coords.Y,
			Player.Conf,
			Player.Orientation,
			Player.Angle,
			Player.Distance)
	}

	// EXTRA

	str += fmt.Sprintf("];[%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v]",
		copy_Data_ESP.EspToMsi_info.Battery_12v,
		copy_Data_ESP.EspToMsi_info.Battery_24v,
		copy_Data_ESP.EspToMsi_info.QC1,
		copy_Data_ESP.EspToMsi_info.QComni,
		copy_Data_ESP.EspToMsi_info.Cap,
		copy_Data_ESP.EspToMsi_info.Bussola_bearing,
		copy_Data_ESP.MsiToEsp_info.Velocity,
		copy_Data_ESP.MsiToEsp_info.Angular,
		copy_Data_ESP.MsiToEsp_info.Direction,
		copy_Data_ESP.EspToMsi_info.vel_db_r,
		copy_Data_ESP.EspToMsi_info.vel_db_l,
		copy_Data_ESP.EspToMsi_info.disp_db_r,
		copy_Data_ESP.EspToMsi_info.disp_db_l,
		copy_Data_ESP.EspToMsi_info.OMNI_temp,
		copy_Data_ESP.EspToMsi_info.Buttons, // avisar nandinho
	)
	//fmt.Println(str)
	str += fmt.Sprintf(";[%v,%v,%v,%v,%v,%v,%v,%v,%v]",
		int(get_CPU()),
		get_TempCPU(),
		get_GPU(),
		get_TempGPU(),
		get_PC_Battery(),
		Skill_loop_time,
		getCommitID(),
		coms_test,
		delta_cicle_coms)
	//fmt.Println("\n", str, "\n")
	return str
}

var splittedString []string

func updateLocalDB(package_ string) {
	//fmt.Println("espScanner.  .. ")
	splittedString = strings.Split(package_, ",")

	if len(splittedString) > 5 {
		var aux_Data_ESP Data_ESP_st
		//fmt.Println("espScanner.............................")
		aux_Data_ESP.EspToMsi_info.Bussola_bearing, _ = strconv.Atoi(splittedString[0])
		aux_Data_ESP.EspToMsi_info.Battery_12v, _ = strconv.Atoi(splittedString[1])
		aux_Data_ESP.EspToMsi_info.Battery_24v, _ = strconv.Atoi(splittedString[2])
		aux_Data_ESP.EspToMsi_info.OMNI_temp, _ = strconv.Atoi(splittedString[3])
		aux_Data_ESP.EspToMsi_info.Dips_X, _ = strconv.Atoi(splittedString[4])
		aux_Data_ESP.EspToMsi_info.Dips_Y, _ = strconv.Atoi(splittedString[5])
		aux_Data_ESP.EspToMsi_info.disp_db_l, _ = strconv.Atoi(splittedString[6])
		aux_Data_ESP.EspToMsi_info.disp_db_r, _ = strconv.Atoi(splittedString[7])
		aux_Data_ESP.EspToMsi_info.vel_db_l, _ = strconv.Atoi(splittedString[8])
		aux_Data_ESP.EspToMsi_info.vel_db_r, _ = strconv.Atoi(splittedString[9])
		aux_Data_ESP.EspToMsi_info.Ball_status, _ = strconv.Atoi(splittedString[10])
		aux_Data_ESP.EspToMsi_info.Buttons, _ = strconv.Atoi(splittedString[11])

		/*dtbase_mutex.Lock()
		database.Ball.Status = aux_Data_ESP.EspToMsi_info.Ball_status
		dtbase_mutex.Unlock()*/
		ESP_mutex.Lock()
		Data_ESP.EspToMsi_info = aux_Data_ESP.EspToMsi_info
		ESP_mutex.Unlock()

	}
}

func updateLocalDB2(package_ string, file *excelize.File, idx int) {

	splittedString = strings.Split(package_, ",")

	Bussola_bearing, _ := strconv.Atoi(splittedString[0])
	Data_ESP.EspToMsi_info.Battery_12v, _ = strconv.Atoi(splittedString[1])
	//temp, _ := strconv.Atoi(splittedString[2])
	Dips_X, _ := strconv.Atoi(splittedString[3])
	Dips_Y, _ := strconv.Atoi(splittedString[4])

	A := "A" + strconv.Itoa(idx_exel)
	B := "B" + strconv.Itoa(idx_exel)
	C := "C" + strconv.Itoa(idx_exel)
	//D := "D" + strconv.Itoa(idx_exel)
	E := "E" + strconv.Itoa(idx_exel)
	file.SetCellValue("Sheet1", A, Bussola_bearing)

	file.SetCellValue("Sheet1", B, Dips_X)
	file.SetCellValue("Sheet1", C, Dips_Y)
	idx_exel++
	fmt.Println(E)
	if idx_exel > 5 {
		file.SetActiveSheet(idx)
		if err := file.SaveAs("names.xlsx"); err != nil {
			log.Fatal(err)
		}
		os.Exit(0)
	}
}

/*for range ticker.C {
	buff := make([]byte, 32)
	if n, err := port.Read(buff); err == nil && n > 10 {
		message := string(buff)
		command := message[:strings.IndexByte(message, '\n')]
		//a correct command has always more then 10 bytes
		if len(command) > 10 {
			updateLocalDB(command)
		}
	}
}*/
