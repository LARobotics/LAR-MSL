package skills

import (
	"context"
	"fmt"
	coms "player/communication"
	"time"
)

func skStop(args_ [7]int, quit chan int) {
	fmt.Println(" Stop")
	arg := args_
	vare := arg[0]
	var last_time time.Time
	var time_now time.Time

	for {
		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return
		default:
			for len(Fns_args) > 0 && vare != -2 {
				fmt.Println("vou fiquei preso")
				arg = <-Fns_args
				fmt.Println("fiquei preso")
			}
			time_now = time.Now()
			//client.Send_Kinect(context.Background(), &req)
			if float64(time_now.Sub(last_time).Milliseconds()) > 40 {
				coms.SendCommandToESP(coms.CMD_all, 0, 0, 0, 100, 100, 0)
				last_time = time_now
				fmt.Println("🛑️🛑️ - Stopped....", arg, len(Fns_args))
				client.Send_Kinect(context.Background(), &req)
			}

		}
	}
}
