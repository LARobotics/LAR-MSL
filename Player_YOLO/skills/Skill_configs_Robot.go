package skills

/*
Atack variables
*/
const Kp_atack = 0.337
const Ki_atack = 0.062
const Kd_atack = 0.000
const outputLimit_PID_atack = 80.000
const Katracao_atack = 1.126
const Kintensidade_atack = 0.822
const outputLimit_atractor_atack = 80.000

/*
Receive variables
*/
const Kp_receive_rot = 0.450
const Ki_receive_rot = 0.050
const Kd_receive_rot = 0.000
const outputLimit_PID_receive_rot = 20.000
const Kp_receive_vel = 0.120
const Ki_receive_vel = 0.010
const Kd_receive_vel = 0.000
const outputLimit_PID_receive_vel = 70.000
const Katracao_receive = 0.000
const Kintensidade_receive = 0.000
const outputLimit_atractor_receive = 0.000

/*
Move variables
*/
const Kp_move = 0.200
const Ki_move = 0.000
const Kd_move = 0.000
const outputLimit_PID_move = 21.900
const Katracao_move = 0.186
const Kintensidade_move = 0.044
const outputLimit_atractor_move = 78.000

const Krepulsao_move = 9.310
const Kinfluencia_move = 4.260
const outputLimit_reppeller_move = 120.000

/*
Kick variables
*/
const Kp_kick = 0.195
const Ki_kick = 0.106
const Kd_kick = 0.054
const outputLimit_PID_kick = 16.300
const Katracao_kick = 0.000
const Kintensidade_kick = 0.000
const outputLimit_atractor_kick = 0.000

/*
Cover variables
*/
const Kp_cover = 0.000
const Ki_cover = 0.000
const Kd_cover = 0.000
const outputLimit_PID_cover = 0.000
const Katracao_cover = 0.000
const Kintensidade_cover = 0.000
const outputLimit_atractor_cover = 0.000


/*
Defend variables
*/
const A_ellipse = 900.000
const B_ellipse = 1400.000
const Katracao_place = 6.600
const Kintensidade_place = 0.040
const outputLimit_atractor_place = 30.000
const Katracao_defend = 0.040
const Kintensidade_defend = 0.085
const outputLimit_atractor_defend = 80.000


/*
Remote Control variables
*/
const Kp_remoteControl = 1.000
const Ki_remoteControl = 0.000
const Kd_remoteControl = 0.100
const outputLimit_PID_remoteControl = 30.000
const Katracao_remoteControl = 0.000
const Kintensidade_remoteControl = 0.000
const outputLimit_atractor_remoteControl = 0.000


