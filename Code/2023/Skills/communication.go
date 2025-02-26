package communication

import (
	"fmt"
	"log"
	"strconv"
	"strings"
	"time"

	"go.bug.st/serial"
	//"github.com/goburrow/serial"
)

const ttyUSB_NAME = "/dev/ttyUSB1"

type EspToMsi struct {
	battery         int
	bussola_bearing int
	bussola_pitch   int
	bussola_roll    int
	distance        int
}

type MsiToEsp struct {
	velocity  int
	angular   int
	direction int
	dribbler1 int
	dribbler2 int
	KickTime  int
}

var get_data = EspToMsi{0, 0, 0, 0, 0}
var set_data = MsiToEsp{0, 0, 0, 0, 0, 0}

var (
	address  string
	baudrate int
	databits int
	stopbits int
	parity   string
	message  string
)
var port serial.Port

var new_msg bool
var array_FIFO [64]byte
var FIFO_write_index int
var FIFO_read_index int
var number_commands int

func Set_MsiToEsp(aux MsiToEsp) {
	set_data.velocity = aux.velocity
	set_data.angular = aux.angular
	set_data.direction = aux.direction
	set_data.dribbler1 = aux.dribbler1
	set_data.dribbler2 = aux.dribbler2
	set_data.KickTime = aux.KickTime
}
func Get_bussola() int {
	return get_data.bussola_bearing
}

func Get_Battery() int {
	return get_data.battery
}
func Get_distance() int {
	return get_data.distance
}

func OpenSerial() {

	var err error
	port, err = serial.Open(ttyUSB_NAME, &serial.Mode{})
	if err != nil {
		log.Fatal(err)
	}
	config := serial.Mode{
		BaudRate: 115200,
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

func isFIFOFreetoWrite() bool {
	aux := FIFO_read_index
	aux1 := FIFO_write_index

	if FIFO_read_index <= FIFO_write_index {
		if FIFO_write_index > 47 {
			return FIFO_read_index+(63-FIFO_write_index) >= 16
		}
		return 63-aux1 >= 16 // 63-aux >= 0

	}
	return aux-aux1 >= 16 //  63+aux1-aux > 20
}
func SendPackage(msg string) {
	_, err := port.Write([]byte(msg))
	if err != nil {
		log.Fatal(err)
	}
}

func Communication() {

	//buff := make([]byte, 100)
	FIFO_write_index = 0
	FIFO_read_index = 0
	number_commands = 0
	OpenSerial()
	fmt.Println("Communication")
	ticker := time.NewTicker(40 * time.Millisecond)

	for {

		fmt.Print("    Package    ")
		for range ticker.C {
			//fmt.Println(FIFO_write_index, "\t", FIFO_read_index, "\t", number_commands, "\t")
			//fmt.Println(isFIFOFreetoWrite() || first_time)
			buff := make([]byte, 32)

			//fmt.Println(FIFO_write_index, "     ", FIFO_read_index, "     ", n)

			if n, err := port.Read(buff); err == nil {
				if n != 0 {

					message := string(buff)
					command := message[:strings.IndexByte(message, '\n')]

					updateLocalDB(command)
				}
			}

		}

		//updateLocalDB(received_package)
	}

}

func updateLocalDB(package_ string) {
	splittedString := strings.Split(package_, ",")

	/*fmt.Print("    Package    ")
	fmt.Println(package_)
	*/
	get_data.bussola_bearing, _ = strconv.Atoi(splittedString[0])
	get_data.bussola_pitch, _ = strconv.Atoi(splittedString[1])
	get_data.bussola_roll, _ = strconv.Atoi(splittedString[2])
	get_data.battery, _ = strconv.Atoi(splittedString[3])
	get_data.distance, _ = strconv.Atoi(splittedString[4])

	fmt.Println(get_data)
}

/*kj
func getUnreadedBytesSize() int {

	if !(FIFO_write_index < FIFO_read_index) {
		size_ := 63 - FIFO_read_index
		size_ += FIFO_write_index
		return size_
	}
	return FIFO_write_index - FIFO_read_index
}

func isDataToRead() bool {
	return FIFO_read_index != FIFO_write_index
}*/
