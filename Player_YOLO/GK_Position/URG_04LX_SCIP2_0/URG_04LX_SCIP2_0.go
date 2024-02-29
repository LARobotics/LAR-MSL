package URG_04LX_SCIP2_0

import (
	"bufio"

	"fmt"
	"log"

	"go.bug.st/serial"
	"go.bug.st/serial/enumerator"
)

const BAUDRATE = 115200         //115200 750000
const lidar_USBID = "2e8a:0005" //"15d1:0000"

//var PEDIDO string = "MS0044072500001\r"

// Max -> 240º
// const StartStep = 44
// const endStep = 725
// 230º
const StartStep = 100
const endStep = 668

var PEDIDO string = "MS0100066800001\r"

const NumSteps = endStep - StartStep + 1
const numScans = 1
const DistRes = 4095
const AngleRes float64 = 360.0 / 1024.0

func GenerateCommand() string {
	PEDIDO = "MS00" + fmt.Sprint(StartStep) + "0" + fmt.Sprint(endStep) + "00001"
	fmt.Println(PEDIDO)
	return PEDIDO
}
func Openserialport() serial.Port {
	// Available Serial Ports List
	/* var port []string */
	ports, err := serial.GetPortsList()
	if err != nil {
		log.Fatal(err)
	}
	if len(ports) == 0 {
		log.Fatal("🔌 No serial ports found!")
	}
	for _, port := range ports {
		fmt.Printf("🔌 Found port: %v\n", port)
	}
	// Choose Serial Port
	/* 	var portsAmount uint = 0
	   	for _, port := range ports {
	   		portsAmount++
	   		fmt.Printf("#%d - %s\n", portsAmount, port)
	   	}
	   	var com string = "1"
	   	fmt.Println("Connect to port #?")

	   	fmt.Sscanf(com, "%d", com)
	   	fmt.Println(com) */
	// Open Serial Port
	// Default Mode : 9600_N81
	// Mode 115200_N81
	mode := &serial.Mode{
		BaudRate: BAUDRATE, //115200 750000
	}

	//port, err := serial.Open("COM7", mode)
	port, err := serial.Open(ports[0], mode)
	fmt.Printf("📤📥Serial Baudrate: %v\n", mode.BaudRate)

	if err != nil {
		log.Fatal(err)
	}
	return port
}
func Openserialport_Detailed() serial.Port {
	var portIndex = 0
	ports, err := enumerator.GetDetailedPortsList()
	if err != nil {
		log.Fatal(err)
	}
	if len(ports) == 0 {
		log.Fatal("🔌 No serial ports found!")
	}
	for i, port := range ports {
		fmt.Printf("🔌 Found port: %s\n", port.Name)
		if port.IsUSB {
			fmt.Printf("   USB ID     %s:%s\n", port.VID, port.PID)
			fmt.Printf("   USB serial %s\n", port.SerialNumber)
		}
		if port.PID == lidar_USBID {
			portIndex = i
		}
	}
	fmt.Println("portIndex: ", portIndex)
	// Connect to URG_04LX
	// Mode 115200_N81
	mode := &serial.Mode{
		BaudRate: BAUDRATE, //115200 750000
	}
	fmt.Printf("📤📥Serial Baudrate: %v\n", mode.BaudRate)

	//port, err := serial.Open("COM7", mode)
	port, err := serial.Open(ports[portIndex].Name, mode)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("🔌 Connected to port Named: %s Id: %s\n", ports[portIndex].Name, ports[portIndex].PID)
	return port
}

var n int
var err error

func SendCommand(port serial.Port, show bool) int {
	// SEND LIDAR CONFIG
	n, err = port.Write([]byte(PEDIDO))
	if err != nil {
		log.Fatal(err)
	}
	if show {
		fmt.Println(PEDIDO)
		fmt.Printf("Sent %v bytes\n", n)
	}
	return n
}
func SendCommand_2(bufio *bufio.Writer, show bool) int {
	// SEND LIDAR CONFIG
	//n, err := port.Write([]byte(PEDIDO))
	n, err := bufio.Write([]byte(PEDIDO))
	if err != nil {
		log.Fatal(err)
	}
	if show {
		fmt.Println(PEDIDO)
		fmt.Printf("Sent %v bytes\n", n)
	}
	return n
}

func ReadCommandEcho(port serial.Port, show bool) int {
	// REQUEST LIDAR ACK
	init := make([]byte, 25) //SHOULD BE 26 == MINIMUM SIZE OF REQUEST COMMAND ECHO
	var n int = 0
	var err error
	//for n < 25 {
	for n < len(init) {
		n, err = port.Read(init)
		if err != nil {
			log.Fatal(err)
			break
		}
	}
	if n == 0 {
		fmt.Println("\nEOF")
		return -1
	} else if show {
		init := string(init)
		fmt.Println(init)
		fmt.Printf("Read %v bytes\n", n)
	}
	return n
}

func ReadCommandEcho_2(reader *bufio.Reader, show bool) int {
	// REQUEST LIDAR ACK
	init := make([]byte, 47) //21+26=47 SHOULD BE 26 == MINIMUM SIZE OF REQUEST COMMAND ECHO
	var n int = 0
	var err error

	for n = 0; n < len(init); n++ {
		init[n], err = reader.ReadByte()
		if err != nil {
			log.Fatal(err)
			break
		}
		//fmt.Printf("%s", init)
	}
	if show {
		fmt.Println(string(init))
		fmt.Printf("Read %v bytes\n", n)
	}
	return n
}

var msb_max byte
var lsb_max byte
var lidar_max uint16
var msb byte
var lsb byte

func ReadMeasure(port serial.Port, lidar []uint16, show bool) int {
	msb_max = byte(0)
	lsb_max = byte(0)
	lidar_max = uint16(0)

	// NewReader
	reader := bufio.NewReader(port)
	for i := 0; i < len(lidar); i++ {

		msb, _ = reader.ReadByte()
		//fmt.Printf("%c", msb)
		lsb, _ = reader.ReadByte()
		//fmt.Printf("%c", msb)
		lidar[i] = (uint16(msb-0x30) << 6) | (uint16(lsb) - 0x30) // 2 Character Encoded Data
		if ((i + 1) % 32) == 0 {                                  // Every 64 bytes or 32 Measurements
			reader.Discard(2) // SUM + LF
		}
		//TEMP_START
		if show {
			if msb > msb_max {
				msb_max = msb - 0x30
			}
			if lsb > lsb_max {
				lsb_max = lsb - 0x30
			}
			if lidar[i] > lidar_max {
				lidar_max = lidar[i]
			}
			fmt.Printf("%d ► msb: %v\tmsb-0x30: %v\t(msb-0x30)<<6): %v\t", i, msb, (msb - 0x30), uint16(msb-0x30)<<6)
			fmt.Printf("lsb: %v\tlsb-0x30: %v\t ", lsb, (lsb - 0x30))
			fmt.Printf("(msb-0x30)<<6)|(lsb-0x30): %v\n", (uint16(msb-0x30)<<6)|(uint16(lsb-0x30)))

			if i == len(lidar) {
				fmt.Printf("msb_max: %v \t lsb_max: %v \t lidar_max: %v\n", msb_max, lsb_max, lidar_max)
				fmt.Printf("%v \t", lidar)
			}
		}
	}
	reader.Discard(3) // SUM + LF + LF

	return len(lidar)
}
func ReadMeasure_2(reader *bufio.Reader, lidar []uint16, show bool) int {
	msb_max = byte(0)
	lsb_max = byte(0)
	lidar_max = uint16(0)

	// NewReader
	for i := 0; i < len(lidar); i++ {
		//fmt.Printf("%v", i)
		msb, _ = reader.ReadByte()
		//fmt.Printf("%c", msb)
		lsb, _ = reader.ReadByte()
		//fmt.Printf("%c", msb)
		lidar[i] = (uint16(msb-0x30) << 6) | (uint16(lsb) - 0x30) // 2 Character Encoded Data
		if ((i + 1) % 32) == 0 {                                  // Every 64 bytes or 32 Measurements
			reader.Discard(2) // SUM + LF
		}
		//TEMP_START
		if show {
			if msb > msb_max {
				msb_max = msb - 0x30
			}
			if lsb > lsb_max {
				lsb_max = lsb - 0x30
			}
			if lidar[i] > lidar_max {
				lidar_max = lidar[i]
			}
			fmt.Printf("%d ► msb: %v\tmsb-0x30: %v\t(msb-0x30)<<6): %v\t", i, msb, (msb - 0x30), uint16(msb-0x30)<<6)
			fmt.Printf("lsb: %v\tlsb-0x30: %v\t ", lsb, (lsb - 0x30))
			fmt.Printf("(msb-0x30)<<6)|(lsb-0x30): %v\n", (uint16(msb-0x30)<<6)|(uint16(lsb-0x30)))

			if i == len(lidar) {
				fmt.Printf("msb_max: %v \t lsb_max: %v \t lidar_max: %v\n", msb_max, lsb_max, lidar_max)
				fmt.Printf("%v \t", lidar)
			}
		}
	}
	reader.Discard(3) // SUM + LF + LF
	//reader.Discard(reader.Buffered())

	return len(lidar)
}
