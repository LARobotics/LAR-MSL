package main

import (
	"fmt"
	//cll "player/LocalDB"
	//coms "player/communication"
	skills "player/skills"
)

func main() {
	fmt.Println("START")

	//SendPackage()
	//go cll.Lacl()
	defer skills.Skills()
	//defer coms.Communication()
	//go Driber()

}
