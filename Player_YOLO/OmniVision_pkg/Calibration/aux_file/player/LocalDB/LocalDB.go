package LocalDB

import (
	"fmt"
	coms "player/communication"
	"time"
)

func Lacl() {
	fmt.Println("START")
	C := make(chan [5]coms.Robot_st)
	B := make(chan coms.Ball_st)

	for {
		time.Sleep(1 * time.Second)
		DATA := coms.Robot_st{2, 32, 24, 25, false}

		var data coms.LocalDB

		data.Team[0] = DATA
		data.Team[1] = DATA
		data.Team[2] = DATA
		data.Team[3] = DATA
		data.Team[4] = DATA
		fmt.Println(233)

		go func() {
			C <- data.Team
			//C <- data.Team
		}()
		coms.SetRobotsPositions(0, C)

		go coms.GetTeamRobots(false, C)
		fmt.Println(<-C)

		go coms.GetBallPosition(B)
		fmt.Println(<-B)
	}
}
