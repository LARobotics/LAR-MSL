package main

import (
	"fmt"
	"os"

	coms "player/communication"
	"strconv"
	"sync"

	"time"

	//cll "player/LocalDB"
	OmniVision "player/OmniVision_pkg"

	skills "player/skills"
)

// WaitGroup is used to wait for the program to finish goroutines.
var WG sync.WaitGroup
var goroutines_nmr = 2

func main() {
	fmt.Println("START")
	//SendPackage()
	//go cll.Lacl()

	// Add a count of three, one for each goroutine.
	WG.Add(goroutines_nmr)
	fmt.Println(os.Args)
	serial_port_name := os.Args[1]
	skills_mode, _ := strconv.Atoi(os.Args[2])
	my_id := os.Args[3]
	my_ip := os.Args[4]

	basestation_ip := "172.16.49.136" //os.Args[5]

	fmt.Println("IPS........................", serial_port_name)

	fmt.Println(my_id,
		my_ip,
		basestation_ip)
	//time.Sleep(100 * time.Millisecond)
	go OmniVision.Run()
	//time.Sleep(1 * time.Millisecond)
	
	go skills.Skills(skills_mode)
	time.Sleep(100 * time.Millisecond)

	go coms.Communication(serial_port_name, my_id, my_ip, basestation_ip, skills_mode)

	// Wait for the goroutines to finish.
	WG.Wait()
	fmt.Println("END     END     END     END")
}
