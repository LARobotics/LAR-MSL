package main

import (
	"fmt"
	"net"
	"strings"
)

const numberOfRobots = 5

type address struct {
	ip string
	port string
}

type position struct{
	x int
	y int
}

type robot struct {
	adr address
	pos position
	state int
}

var serverAdrString = address{ip:"192.168.31.249", port:"20000"}
var robotAdrString = []address{{ip:"10.0.0.28", port:"20001"},
						{ip:"10.0.0.28", port:"20002"},
						{ip:"10.0.0.28", port:"20003"},
						{ip:"10.0.0.28", port:"20004"},
						{ip:"10.0.0.28", port:"20005"},}
var robotAddresses = [numberOfRobots]*net.UDPAddr{}
var serverAddress *net.UDPAddr

func main() {
	serverAddress, _ = net.ResolveUDPAddr("udp", serverAdrString.ip+":"+serverAdrString.port)
	serverConnection, _ := net.ListenUDP("udp", serverAddress)
	recieve(serverConnection)
	// for i:=0; i < numberOfRobots; i++ {
	// 	robotAddresses[i], _ = net.ResolveUDPAddr("udp", robotAdrString[i].ip+":"+robotAdrString[i].port)
	// 	fmt.Println(robotAddresses[i])
	// }
	// fmt.Println("TA")

	// a := []int{2, 3, 4, 5, 6, 6}
	// fmt.Println(a)
	
	// //var a int = 1
	// a := 1
	// a = "string"

	// Addr, _ := net.ResolveUDPAddr("udp", "10.0.0.28:20001")
	
	// //connD, _ := net.DialUDP("udp", nil, serAddr)
	// connD, _ := net.ListenUDP("udp", serAddr)
	
	// for i := 1; i < 1000; i++{
	// 	_, _ = connD.WriteToUDP([]byte(string(strconv.Itoa(i))), udpAddr)
	// }
	// _, _ = connD.WriteToUDP([]byte("q"), udpAddr)
	
	// recieve(conn)
	
	//fmt.Print("vou enviar?")
	//_, _ = connL.WriteToUDP([]byte("teste"), serAddr)
	// time.Sleep(2)
	//fmt.Print("Enviei")*/
}

func recieve(conn *net.UDPConn) {

	buffer := make([]byte, 1024)
	for strings.Compare(string(buffer), "q") == -1{
		buffer = make([]byte, 1024)
		_, addr, _ := conn.ReadFromUDP(buffer)
		fmt.Println(addr.IP, " ", addr.Port)
		fmt.Println(string(buffer))
	}
	
}