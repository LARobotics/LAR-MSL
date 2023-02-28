package main

import (
	"os"
	GK "player/GK_vision"
	coms "player/communication"
	"sync"
	"time"
)

// WaitGroup is used to wait for the program to finish goroutines.
var WG sync.WaitGroup
var goroutines_nmr = 2

func main() {
	WG.Add(goroutines_nmr)
	serial_port_name := os.Args[1]

	// Start communication program
	go coms.Communication(serial_port_name)
	// Wait for every connection
	time.Sleep(500 * time.Millisecond)
	// Start goalkeeper vision
	go GK.GK_vision()
	WG.Wait()
}
