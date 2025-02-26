package main

import (
	"fmt"
	coms "player/communication"
)

func main() {
	fmt.Println("START")
	//SendPackage()
	go coms.Communication()
	//go skills.Orientation()

	//go Driber()
	for {
	}
}
