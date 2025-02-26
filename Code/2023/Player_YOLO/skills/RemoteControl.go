package skills

import (
	"fmt"
	"math"
	coms "player/communication"
	"time"
)

/*
**
*************Remote Control*************

Command: 7 Dx Dy Ori P/K

Dx -> target x coordinate
Dy -> target y coordinate
Ori ->
P/K ->

*************Remote Control*************
**
*/
var rmt_ctrl_orientation = NewPid(Kp_remoteControl, Ki_remoteControl, Kd_remoteControl, 0.0, outputLimit_PID_remoteControl)

func skRemoteControl(args_ [7]int, quit chan int) { //args_ [7]int
	/*
		*
		*
		testar oritentacao
		*
		*
	*/
	//rot, ori_aux, dir_aux := 0, 0, 0
	fmt.Println("RemoteControl")
	ang_ref := 0
	data_st := new(coms.MsiToEsp)
	var dx, dy int //ori
	var rot float64
	arg := args_
	//vare := arg[0]
	//ori_pid := NewPid(1, 0.0, 0.1, 0.05, 20)

	var current_time time.Time
	var old_time time.Time
	//var flg bool
	for { //flg= <- fns_chan[7]       args_ := range Fns_args

		select {
		case <-quit:
			fmt.Println("quit")
			wait_4_skill.Done()
			return
		default:
			/*for len(Fns_args) > 0 && vare != -1 {
				arg = <-Fns_args
				fmt.Println("ARGS        :", arg)
			}*/
			BS_args_mutex.Lock()
			arg = BS_args
			BS_args_mutex.Unlock()

			dx = arg[1]
			dy = arg[0]
			ang_ref = arg[2]
			kick := arg[3]
			dir_atual := coms.Get_bussola()
			var vel, dir float64

			ang := math.Atan2(float64(dy), float64(dx))
			//fmt.Println("ang", ang, "   dx", dx, "dy   ", dy)

			//vel = float64(dy) / math.Sin(ang)
			dx2 := float64((dx * dx))
			dy2 := float64((dy * dy))
			vel = math.Sqrt(dx2 + dy2)
			///fmt.Println(dx, '\t', dy, '\t', vel)
			dir = ((ang * 180) / math.Pi) //- float64(dir_atual)

			if dir < 0 {
				//fmt.Println("dirasasa", 360+dir)
				dir = dir + 360
			}
			kick = kick * 7

			ori_erro := ang_ref - dir_atual
			old_time = current_time
			current_time = time.Now()
			rot = rmt_ctrl_orientation.Update(float64(ori_erro), float64(current_time.Sub(old_time).Seconds()))

			data_st.Velocity = int(vel)
			data_st.Angular = int(rot)
			data_st.Direction = int(dir)
			//coms.SendCommandToESP(coms.CMD_all, data_st.Velocity, data_st.Angular, data_st.Direction, 0, 0, 0)
		}
	}
}
