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

const numberOfRobots = 5
const robot_number = 4 //pc ->1

// serial port init variables
const ttyUSB_NAME = "/dev/ttyUSB0"
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
	Orientation int
	Status      int
	Ball        bool
}
type Ball_st struct {
	Coords position
	Z      int
}
type LocalDB struct {
	Team     [5]Robot_st
	Opponent [5]Robot_st
	Ball     Ball_st
	Battery  int
}

// struct variables for communication with Basestation
type address struct {
	ip   string
	port string
}

type position struct {
	X float64
	Y float64
}

type robot struct {
	adr   address
	pos   position
	state int
}

// struct with variables to receive from esp32 - HM controller
type EspToMsi struct {
	Battery_        int
	Bussola_bearing int
	OMNI_temp       int
	Dips_X          int
	Dips_Y          int
}

// struct with variables to send to esp32 - HM controller
type MsiToEsp struct {
	Velocity  int
	Angular   int
	Direction int
	Dribbler1 int
	Dribbler2 int
	KickTime  int
}

// Variables for all robots informations and ball
var database LocalDB
var get_data = EspToMsi{0, 0, 0, 0, 0}
var set_data = MsiToEsp{0, 0, 0, 0, 0, 0}

var dtbase_mutex sync.Mutex
var ESP_mutex sync.Mutex
var esp_com_mutex sync.Mutex
var basestaion_mutex sync.Mutex

// Port variable for serial communication
var port serial.Port

var Esp_commands = []string{"driblers", "omni_speed", "omni_gains", "all"}

//192.168.31.79 meu IP

// variables for vommunication with Basesetation
var serverAdrString = address{ip: "172.16.49.156", port: "21020"}
var robotAdrString = []address{{ip: "172.16.49.120", port: "20120"},
	{ip: "10.0.0.28", port: "20002"},
	{ip: "10.0.0.28", port: "20003"},
	{ip: "10.0.0.28", port: "20004"},
	{ip: "10.0.0.28", port: "20005"}}
var LocalAdrString = []address{{ip: "172.16.49.120", port: "21021"}}

var robotAddresses = [numberOfRobots]*net.UDPAddr{}
var serverAddress *net.UDPAddr
var New_BS_command bool

var BS_commands [2]string
var idx_exel int

// function definition for receive commands from Basestation and store them on a string array
func recieve(conn *net.UDPConn) {
	buffer := make([]byte, 1024)
	for strings.Compare(string(buffer), "q") == -1 {
		buffer = make([]byte, 1024)
		_, addr, _ := conn.ReadFromUDP(buffer)
		fmt.Println(addr.IP, " ", addr.Port)
		//fmt.Println(string(buffer))
		BS_commands[0] = BS_commands[1]
		BS_commands[1] = string(buffer)
		New_BS_command = true
		//fmt.Print("received pack    ")
		//fmt.Println(BS_commands[1])
	}

}

func recieve2(conn *net.UDPConn) {
	fmt.Println("📡️  Basestation callback")
	buffer := make([]byte, 1024)
	for {
		for strings.Compare(string(buffer), "q") == -1 {
			buffer = make([]byte, 1024)
			//_, addr, _ := conn.ReadFromUDP(buffer)
			_, _, _ = conn.ReadFromUDP(buffer)
			//fmt.Println(addr.IP, " ", addr.Port)
			//fmt.Println('\n', string(buffer))
			//BS_commands[0] = BS_commands[1]
			basestaion_mutex.Lock()
			BS_commands[1] = string(buffer)
			basestaion_mutex.Unlock()
			New_BS_command = true
		}
	}
}

func GetBS_params() (int, int, int, int) {

	splittedString := strings.Split(BS_commands[1], ", ")

	dx, _ := strconv.Atoi(splittedString[1])
	dy, _ := strconv.Atoi(splittedString[2])
	ori, _ := strconv.Atoi(splittedString[3])
	kick, _ := strconv.Atoi(splittedString[4])

	return dx, dy, ori, kick
}

// function definition for receive commands from Basestation
func GetBS_Command(BS_cmd *string) {
	basestaion_mutex.Lock()
	*BS_cmd = BS_commands[1]
	basestaion_mutex.Unlock()
}

// function to put player default
func (ldb LocalDB) Set_default(idx int) {
	if idx > 4 {
		dtbase_mutex.Lock()
		ldb.Opponent[idx-5].Coords.X = float64(-9999)
		ldb.Opponent[idx-5].Coords.Y = float64(-9999)
		dtbase_mutex.Unlock()
		return
	}
	dtbase_mutex.Lock()
	ldb.Team[idx].Coords.X = float64(-9999)
	ldb.Team[idx].Coords.Y = float64(-9999)
	dtbase_mutex.Unlock()

}

func SetBallPosition(ball Ball_st) {
	dtbase_mutex.Lock()
	database.Ball = ball
	dtbase_mutex.Unlock()
}

func SetRobotsPositions(robots_t [5]Robot_st, robots_o [5]Robot_st) {

	dtbase_mutex.Lock()
	database.Team = robots_t
	database.Opponent = robots_o
	dtbase_mutex.Unlock()

}
func SetRobotPosition(idx int, robot Robot_st) {
	if (robot != Robot_st{}) {
		if idx > 4 {
			dtbase_mutex.Lock()
			database.Opponent[idx-5] = robot
			dtbase_mutex.Unlock()
			return
		}
		dtbase_mutex.Lock()
		database.Team[idx] = robot
		dtbase_mutex.Unlock()
	}
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
func GetTeamOfRobots(idx bool, robots *[5]Robot_st) {
	dtbase_mutex.Lock()
	if idx {
		*robots = database.Opponent
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
	defer ESP_mutex.Unlock()

	return get_data.Bussola_bearing
}

func GetDisplacement() (int, int) {
	ESP_mutex.Lock()
	defer ESP_mutex.Unlock()

	return get_data.Dips_X, get_data.Dips_Y
}

func SendESP_Parameters(aux MsiToEsp) {

	set_data = aux

	command := "R" + strconv.Itoa(aux.Velocity) + "," + strconv.Itoa(aux.Angular) +
		"," + strconv.Itoa(aux.Direction)
	sendPackage(command)
}

func SendCommandToESP(cmd_type int, params ...interface{}) {

	switch cmd_type {

	case 0: //driblers values
		{ // db1, db2
			command := fmt.Sprintf("D,%v,%v\n", params[0], params[1])
			sendPackage(command)
		}
	case 1: //omni speeds values
		{ //linear speed, rotational speed, direction
			command := fmt.Sprintf("M,%v,%v,%v\n", params[0], params[1], params[2])
			sendPackage(command)
		}
	case 2: //omni speeds values
		{ //Kp, Ki , Kd
			command := fmt.Sprintf("P,%v,%v,%v\n", params[0], params[1], params[2])
			sendPackage(command)
		}
	case 3: //omni, dribserverConnectionlers, kick values
		{ //linear speed, rotational speed, direction, db1, db2, KickTime
			//fmt.Println(".........sending............ ")
			command := fmt.Sprintf("%v,%v,%v,%v,%v,%v\n", params[0], params[1], params[2], params[3], params[4], params[5])
			sendPackage(command)

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

func OpenServerConnection(remoteAddr_, LocalAddr_, ServerAddr_ *net.UDPAddr) (*net.UDPConn, *net.UDPConn, bool) {
	var err error

	/*for i := 0; i < numberOfRobots; i++ {
		robotAddresses[i], _ = net.ResolveUDPAddr("udp", robotAdrString[i].ip+":"+robotAdrString[i].port)
		fmt.Println(robotAddresses[i])
	}*/
	//fmt.Println("TA")
	//serverConnection, _ := net.ListenUDP("udp", serverAddress)
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
	database.Set_default(0)
	database.Set_default(1)
	database.Set_default(2)
	database.Set_default(3)
	database.Set_default(4) //
	database.Set_default(5)
	database.Set_default(6)
	database.Set_default(7)
	database.Set_default(8)
	database.Set_default(9)

	return Conn, Conn_, true
}

func sendPackage(msg string) {
	esp_com_mutex.Lock()
	//fmt.Println("passou mutex send package")
	_, err := port.Write([]byte(msg))

	if err != nil {
		esp_com_mutex.Unlock()
		log.Fatal(err)
	}
	esp_com_mutex.Unlock()
}

func Communication(ttyUSB_NAME_ string) {
	fmt.Println("Communication Initialized " + ttyUSB_NAME_)

	var remoteAddr, LocalAddr, ServerAddr *net.UDPAddr
	var BS_coms_flag bool

	//create new .xlsx file (exel)
	/*
		file := excelize.NewFile()
		idx := file.NewSheet("Sheet1")
	*/
	idx := 0
	//OpenSerial("/dev/" + ttyUSB_NAME_)
	for !OpenSerial("/dev/"+ttyUSB_NAME_) && idx < 10 {
		idx++
	}
	if idx >= 9 {
		fmt.Println("Communication not initialized")
	}

	Conn_Tx, Conn_Rx, valid := OpenServerConnection(remoteAddr, LocalAddr, ServerAddr)
	BS_coms_flag = false
	if valid {
		fmt.Println("VALID.............................")
		BS_coms_flag = true
		go recieve2(Conn_Rx)
	}
	scanner := bufio.NewScanner(port)
	//recieve(Conn_)

	go espScanner(scanner)
	//timercom := time.NewTimer(50 * time.Millisecond ) // init timer communication to db
	for {
		time.Sleep(time.Millisecond * 50)
		//<-timercom.C // run each 50 ms
		if BS_coms_flag {
			//fmt.Println("AQUI")
			sendCmdToBasestation(Conn_Tx)
		}
		/*if scanner.Scan() {
			esp_com_mutex.Lock()
			updateLocalDB(string(scanner.Text()))
			esp_com_mutex.Unlock()
			}
		}*/
	}
}

func espScanner(scanner *bufio.Scanner) {

	for {
		if scanner.Scan() {

			esp_com_mutex.Lock()
			updateLocalDB(string(scanner.Text()))
			esp_com_mutex.Unlock()
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
func encodeBstationMsg() string {
	n := 20
	var new, old [3]string
	new[0] = ","
	new[1] = "["
	new[2] = "]"

	old[0] = " "
	old[1] = "{"
	old[2] = "}"

	variable := 0
	// protect database
	dtbase_mutex.Lock()
	if database.Team[robot_number].Ball {
		variable = 1
	}

	str := fmt.Sprintf("%v;%v;%v;%v;[[%v;%v;%v;%v];[%v;%v;%v;%v;%v]]", database.Team[0].Coords,
		database.Team[0].Orientation, database.Ball.Coords, variable,
		database.Team[1].Coords, database.Team[2].Coords, database.Team[3].Coords,
		database.Team[4].Coords, database.Opponent[0].Coords, database.Opponent[1].Coords,
		database.Opponent[2].Coords, database.Opponent[3].Coords, database.Opponent[4].Coords)

	// unlock database
	dtbase_mutex.Unlock()
	if len(str) > 0 {
		str = strings.Replace(str, old[0], new[0], n)
		str = strings.Replace(str, old[1], new[1], n)
		str = strings.Replace(str, old[2], new[2], n)
	}

	return str
}

var splittedString []string

func updateLocalDB(package_ string) {

	splittedString = strings.Split(package_, ",")
	if len(splittedString) > 4 {

		ESP_mutex.Lock()

		get_data.Bussola_bearing, _ = strconv.Atoi(splittedString[0])
		get_data.Battery_, _ = strconv.Atoi(splittedString[1])
		get_data.OMNI_temp, _ = strconv.Atoi(splittedString[2])
		get_data.Dips_X, _ = strconv.Atoi(splittedString[3])
		get_data.Dips_Y, _ = strconv.Atoi(splittedString[4])
		database.Battery = get_data.Battery_
		ESP_mutex.Unlock()

	}
}

func updateLocalDB2(package_ string, file *excelize.File, idx int) {
	esp_com_mutex.Unlock()
	splittedString = strings.Split(package_, ",")

	Bussola_bearing, _ := strconv.Atoi(splittedString[0])
	get_data.Battery_, _ = strconv.Atoi(splittedString[1])
	//temp, _ := strconv.Atoi(splittedString[2])
	Dips_X, _ := strconv.Atoi(splittedString[3])
	Dips_Y, _ := strconv.Atoi(splittedString[4])
	database.Battery = get_data.Battery_

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
