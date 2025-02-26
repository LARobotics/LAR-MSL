package main

import (
	"fmt"
	"os"
	"time"

	OmniVision "player/OmniVision_pkg"
	coms "player/communication"
	"strconv"
	"sync"

	skills "player/skills"
)

// ✅️❌️
// WaitGroup is used to wait for the program to finish goroutines.
var WG sync.WaitGroup
var goroutines_nmr = 2

func main() {
	fmt.Println("🤖️⚽️ - START Player")
	//SendPackage()
	//go cll.Lacl()
	time.Sleep(100 * time.Millisecond)
	// Add a count of three, one for each goroutine.
	WG.Add(goroutines_nmr)
	//fmt.Println("os.Args[1]", os.Args[3])
	/*fmt.Println("os.Args[2]", os.Args[2])
	fmt.Println("os.Args[3]", os.Args[3])
	fmt.Println("os.Args[4]", os.Args[4])
	fmt.Println("os.Args[5]", os.Args[5])
	fmt.Println("os.Args[6]", os.Args[6])*/
	serial_port_name := os.Args[1]
	skills_mode, _ := strconv.Atoi(os.Args[2])
	my_id := os.Args[3]
	my_ip := os.Args[4]
	basestation_ip := os.Args[5]
	my_grpc_ip := os.Args[6]
	shirt, _ := strconv.Atoi(os.Args[7]) //0 red_shirt 1 blue shirt
	ID, _ := strconv.Atoi(my_id)
	//basestation_ip := "172.16.49.88" //os.Args[5]

	//fmt.Println(serial_port_name, my_id, my_ip, basestation_ip, skills_mode, s}hirt)

	go coms.Communication(serial_port_name, my_id, my_ip, basestation_ip, skills_mode)

	time.Sleep(10 * time.Millisecond)
	go OmniVision.Run(shirt == 1, my_grpc_ip, ID)
	//time.Sleep(1 * time.Millisecond)

	go skills.Skills(skills_mode, my_id, my_ip, basestation_ip, my_grpc_ip, shirt)
	//time.Sleep(100 * time.Millisecond)

	// Wait for the goroutines to finish.
	WG.Wait()
	fmt.Println("END     END     END     END")
}
