package skills

import "fmt"

/*
**
*************Cover*************

Command: 5 X1 Y1 X2 Y2 E A

X1 -> target x coordinate
Y1 -> target y coordinate
X2 -> target x coordinate
Y2 -> target y coordinate
E ->
A ->
*************Cover*************
**
*/

func skCover(args_ [7]int, quit chan int) {
	arg := args_
	vare := arg[0]
	for {
		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return
		default:
			//fmt.Println("COVER")
			for len(Fns_args) > 0 && vare != -2 {
				arg = <-Fns_args
				//fmt.Println("ARGS        :", arg)
			}
		}
	}
}
