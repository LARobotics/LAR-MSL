package communication

import (
	"fmt"
	"log"
	"net"
	"strconv"
	"strings"
	"time"

	"go.bug.st/serial"
)

const numberOfRobots = 5

// serial port init variables
const ttyUSB_NAME = "/dev/ttyUSB0"
const baudrate = 115200

// struct with variables to receive from esp32 - HM controller
type Robot_st struct {
	X           int
	Y           int
	Orientation int
	Status      int
	Ball        bool
}
type Ball_st struct {
	X int
	Y int
	Z int
}

// struct with variables to receive from esp32 - HM controller
type EspToMsi struct {
	Battery_        int
	Bussola_bearing int
	Bussola_pitch   int
	Bussola_roll    int
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
	x int
	y int
}

type robot struct {
	adr   address
	pos   position
	state int
}

// Variables for all robots informations and ball
var database LocalDB
var get_data = EspToMsi{0, 0, 0, 0, 0, 0}
var set_data = MsiToEsp{0, 0, 0, 0, 0, 0}

// Port variable for serial communication
var port serial.Port

// variables for vommunication with Basesetation
var serverAdrString = address{ip: "10.0.0.28", port: "20000"}
var robotAdrString = []address{{ip: "10.0.0.28", port: "20001"},
	{ip: "10.0.0.28", port: "20002"},
	{ip: "10.0.0.28", port: "20003"},
	{ip: "10.0.0.28", port: "20004"},
	{ip: "10.0.0.28", port: "20005"}}
var robotAddresses = [numberOfRobots]*net.UDPAddr{}
var serverAddress *net.UDPAddr
var New_BS_command bool

var BS_commands [2]string

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
	}

}

// function definition for receive commands from Basestation
func GetBS_Command(BS_chn chan string) {
	BS_chn <- BS_commands[1]

}

func SendESP_Parameters(aux MsiToEsp) {

	set_data = aux

	command := "R" + strconv.Itoa(aux.Velocity) + "," + strconv.Itoa(aux.Angular) +
		"," + strconv.Itoa(aux.Direction)
	sendPackage(command)
}

func SendCommandToESP(command string) {
	sendPackage(command)
}

func SetBallPosition(C chan Ball_st) {

	database.Ball = <-C

}

func SetRobotsPositions(idx int, C chan [5]Robot_st) {
	switch idx {
	case 0:
		{
			//idx = 0 teammates positions
			database.Team = <-C
		}
	case 1:
		{
			//idx = 1 opponents positions
			database.Opponent = <-C
		}
	case 2:
		{
			//idx = 2 teammates and opponents positions
			database.Team = <-C
			database.Opponent = <-C
		}
	default:
		break

	}
}

func SetRobotPosition(idx int, C chan Robot_st) {

	if idx > 4 {
		database.Opponent[idx-5] = <-C
	}
	database.Team[idx] = <-C
}
func SetDatabase(C chan LocalDB) {

	C <- database
}
func Get_bussola() (int, int, int) {
	return get_data.Bussola_bearing, get_data.Bussola_pitch, get_data.Bussola_roll
}

// idx goes from 0 to 9, where teammates from 0 to 4 and opponents from 5 to 9
func GetRobot(idx int, C chan Robot_st) {
	if idx > 4 {
		C <- database.Opponent[idx-5]
	}
	C <- database.Team[idx]
}

// idx goes from 0 to 9, where teammates from 0 to 4 and opponents from 5 to 9
func GetTeamRobots(idx bool, C chan [5]Robot_st) {
	if idx {
		C <- database.Opponent
	}
	C <- database.Team
}

func GetDatabase(C chan LocalDB) {
	C <- database
}

func GetBallPosition(C chan Ball_st) {

	C <- database.Ball

}
func GetDisplacement() (int, int) {
	return get_data.Dips_X, get_data.Dips_Y
}

func OpenSerial() {

	var err error

	//open serial port
	port, err = serial.Open(ttyUSB_NAME, &serial.Mode{})
	if err != nil {
		log.Fatal(err)
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
		log.Fatal(err)
	}

	err = port.SetReadTimeout(0)
	if err != nil {
		log.Fatal(err)
	}
}

func sendPackage(msg string) {
	_, err := port.Write([]byte(msg))
	if err != nil {
		log.Fatal(err)
	}
}

func Communication() {

	OpenSerial()
	fmt.Println("Communication initialized")

	ticker := time.NewTicker(40 * time.Millisecond)
	//init server communication
	serverAddress, _ = net.ResolveUDPAddr("udp", serverAdrString.ip+":"+serverAdrString.port)
	for i := 0; i < numberOfRobots; i++ {
		robotAddresses[i], _ = net.ResolveUDPAddr("udp", robotAdrString[i].ip+":"+robotAdrString[i].port)
		fmt.Println(robotAddresses[i])
	}
	fmt.Println("TA")
	serverConnection, _ := net.ListenUDP("udp", serverAddress)
	go recieve(serverConnection)
	for {

		for range ticker.C {
			buff := make([]byte, 32)

			if n, err := port.Read(buff); err == nil && n > 10 {

				message := string(buff)
				command := message[:strings.IndexByte(message, '\n')]
				//a correct command has always more then 10 bytes
				if len(command) > 10 {
					updateLocalDB(command)
				}
			}

		}

	}

}

func updateLocalDB(package_ string) {
	splittedString := strings.Split(package_, ",")

	get_data.Bussola_bearing, _ = strconv.Atoi(splittedString[0])
	get_data.Bussola_pitch, _ = strconv.Atoi(splittedString[1])
	get_data.Bussola_roll, _ = strconv.Atoi(splittedString[2])
	get_data.Battery_, _ = strconv.Atoi(splittedString[3])
	get_data.Dips_X, _ = strconv.Atoi(splittedString[4])
	get_data.Dips_Y, _ = strconv.Atoi(splittedString[5])
	database.Battery = get_data.Battery_
	//fmt.Println(get_data)
}
