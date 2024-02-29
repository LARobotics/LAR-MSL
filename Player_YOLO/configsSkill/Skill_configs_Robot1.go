//go:build 1
// +build 1
package skills

/*
Atack variables
*/
const Kp_atack = 0.45
const Ki_atack = 0
const Kd_atack = 0
const outputLimit_PID_atack = 80
const Katracao_atack = 0.55
const Kintensidade_atack = 0.03
const outputLimit_atractor_atack = 80
/*
Receive variables
*/
const Kp_receive_rot = 0.05
const Ki_receive_rot = 0
const Kd_receive_rot = 0,
const outputLimit_PID_receive_rot = 20const Kp_receive_vel = 0.12
const Ki_receive_vel = 0
const Kd_receive_vel = 0,
const outputLimit_PID_receive_vel = 40const Katracao_receive = 0
const Kintensidade_receive = 0
const outputLimit_atractor_receive = 0
/*
Move variables
*/
const Kp_move = 0.2
const Ki_move = 0
const Kd_move = 0,
const outputLimit_PID_move = 10
const Katracao_move = 0
const Kintensidade_move = 0
const outputLimit_atractor_move = 0
/*
Kick variables
*/
const Kp_kick = 0
const Ki_kick = 0
const Kd_kick = 0,
const outputLimit_PID_kick = 0const Katracao_kick = 0
const Kintensidade_kick = 0
const outputLimit_atractor_kick = 0
/*
Cover variables
*/
const Kp_cover = 0
const Ki_cover = 0
const Kd_cover = 0,
const outputLimit_PID_cover = 0const Katracao_cover = 0
const Kintensidade_cover = 0
const outputLimit_atractor_cover = 0
/*
Remote Control variables
*/
const Kp_remoteControl = 1
const Ki_remoteControl = 0
const Kd_remoteControl = 0.1,
const outputLimit_PID_remoteControl = 30const Katracao_remoteControl = 0
const Kintensidade_remoteControl = 0
const outputLimit_atractor_remoteControl = 0