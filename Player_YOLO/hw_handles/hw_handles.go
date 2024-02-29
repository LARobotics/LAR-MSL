package hw_handles

import (
	"encoding/json"
	"fmt"
	"os/exec"
	bt "player/hw_handles/battery"
	cpu "player/hw_handles/cpu"
	"runtime"
	"strconv"
	"strings"

	"time"
)

var robot_number = 2

// Struct for the connection validation
type Connection_t struct {
	CMPS, Omni_Vision, Kinect, ESP, Encoder_1, Encoder_2, Encoder_3 bool
}

// Struct for the CMPS
type CMPS_t struct {
	Bussola, Pitch, Roll, Yaw int
}

// Struct for the bateries percentage
type Battery_t struct {
	Batery_1, Batery_2 int
}

// Struct for the dribblers PWM velocity
type Dribblers_t struct {
	Dribbler_1, Dribbler_2 int
}

// Struct related to the motors
type Motors_t struct {
	Linear_Velocity, Rotational_Velocity, Direction, Encoder_1, Encoder_2, Encoder_3 int
}

// Struct related to the allies detected
type Allies_t struct {
	Number   int
	Angle    [5]int
	Distance [5]int
}

// Struct related to the enemies detected
type Enemies_t struct {
	Number   int
	Angle    [5]int
	Distance [5]int
}

// Struct related to the ball
type Ball_t struct {
	Detection                   bool
	Angle, Distance, Possession int
}

// Struct related to the computer
type Computer_t struct {
    CPU, Cores []float64
	RAM, Loop_Time float64
	GPU, GPU_Temp, CPU_Temp, Batery int
}

// Struct related to the ESP
type ESP_t struct {
	PWM_1, PWM_2, PWM_3, PWM_4            int
	ADC_1, ADC_2, ADC_3, ADC_4, Loop_Time float64
}

// Struct related to the SKILLS
type Skills_t struct {
	Error_Linear, Error_Angular, Loop_Time float64
	X_Target, Y_Target                     int
}

// Struct related to the GoalKeeper
type GoalKeeper_t struct {
	Ball_Side                                          bool
	Absolute_Position, Desired_Position, Ball_Distance int
}

// Every information to send in a struct
type Information struct {
    Robot               int
	Connection          Connection_t
	CMPS                CMPS_t
	Battery             Battery_t
	Dribblers           Dribblers_t
	Capacitor_voltage   int
	Motors              Motors_t
    Allies              Allies_t
    Enemies             Enemies_t
    Ball                Ball_t
	Computer            Computer_t
	ESP                 ESP_t
	Skills              Skills_t
	GK                  GoalKeeper_t
}

func get_GPU() (int){
    // execute nvidia-smi command to get GPU usage
	cmd := exec.Command("nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader")
	out, err := cmd.Output()
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}

	// parse the output and get GPU usage percentage
	usageStr := strings.TrimSpace(string(out))
	var usage float64
	_, err = fmt.Sscanf(usageStr, "%f %%", &usage)
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}

	//fmt.Printf("GPU usage: %d%%\n", int(usage))
    return int(usage)
}

var Core_d []float64
var CPU_d []float64
var i int

func get_CPU() {
    if i > 100 {
        i = 0
        CPU_d, _ = cpu.Percent(0, false) //false gives one value (CPU) and true gives every core
        Core_d, _ = cpu.Percent(0, true)
    } else {
        i++
    }
}

func get_TempCPU() (int){
    // execute command to get CPU temperature on Linux
	cmd := exec.Command("cat", "/sys/class/thermal/thermal_zone0/temp")
    // execute command to get CPU temperature on Windows
	//cmd := exec.Command("powershell", "Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty Temperature | Measure-Object -Average | Select-Object -ExpandProperty Average")
	out, err := cmd.Output()
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}

	// convert output to float and print CPU temperature
	tempStr := strings.TrimSpace(string(out))
	temp, err := strconv.ParseFloat(tempStr, 64)
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}
    //Linux
    //fmt.Printf("CPU temperature: %d°C\n", int(temp/1000.0))
    return int(temp/1000.0)
    //Windows
	//fmt.Printf("CPU temperature: %d°C\n", int(temp/10.0))
    //return int(temp/10.0)
}

func get_TempGPU() (int){
    cmd := exec.Command("nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader")

	out, err := cmd.Output()
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}

	// convert output to float and print GPU temperature
	tempStr := strings.TrimSpace(string(out))
	temp, err := strconv.ParseFloat(tempStr, 64)
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}
	//fmt.Printf("GPU temperature: %d°C\n", int(temp))
    return int(temp)
}

var memStats runtime.MemStats

func get_RAM() (float64) {
    runtime.ReadMemStats(&memStats)
    //fmt.Printf("RAM usage: %.2f MB\n", float64(memStats.Alloc)/1000000)
    return float64(memStats.Alloc)/1000000
}

func get_Data() (data Information){
    get_CPU()
    // get memory statistics
    data = Information{
        Robot:              robot_number,
        Connection: Connection_t{
            CMPS:           true,
            Omni_Vision:    true,
            Kinect:         false,
            ESP:            true,
            Encoder_1:      true,
            Encoder_2:      true,
            Encoder_3:      false,
        },
        CMPS: CMPS_t{
            Bussola:        32,
            Pitch:          0,
            Roll:           0,
            Yaw:            0,
        },
        Battery: Battery_t{
            Batery_1:       82,
            Batery_2:       30,
        },
        Dribblers: Dribblers_t{
            Dribbler_1:     10,
            Dribbler_2:     10,
        },
        Capacitor_voltage:  100,
        Motors: Motors_t{
            Linear_Velocity:        20,
            Rotational_Velocity:    0,
            Direction:              90,
            Encoder_1:              0,
            Encoder_2:              50,
            Encoder_3:              32,
        },
        Allies: Allies_t{
            Number:         2,    
	        Angle:          [5]int{40,72,0,0,0},
	        Distance:       [5]int{200,452,0,0,0},
        },
        Enemies: Enemies_t{
            Number:         2,    
	        Angle:          [5]int{248,0,0,0,0},
	        Distance:       [5]int{821,0,0,0,0},
        },
        Ball: Ball_t{
            Detection:      true,
            Angle:          248,
            Distance:       821,
            Possession:     2,
        },
        Computer: Computer_t{
            GPU:            get_GPU(),
            CPU:            CPU_d,
            RAM:            get_RAM(),
            Cores:          Core_d,
            Loop_Time:      14.6,
            GPU_Temp:       get_TempGPU(),
            CPU_Temp:       get_TempCPU(),
            Batery:         64,
        },
        ESP: ESP_t{
            PWM_1:          23,
            PWM_2:          28,
            PWM_3:          89,
            PWM_4:          65,
            ADC_1:          2.5,
            ADC_2:          2.8,
            ADC_3:          1.2,
            ADC_4:          5.8,
            Loop_Time:      9.5,
        },
        Skills: Skills_t{
            Error_Linear:   0.2,
            Error_Angular:  0.7,
            Loop_Time:      13.2,
	        X_Target:       20,
            Y_Target:       38,
        },
        GK: GoalKeeper_t{
            Ball_Side:          true,
	        Absolute_Position:  120,
            Desired_Position:   182,
            Ball_Distance:      200,
        },
	}
    return data
}

var File []byte
var v Information
var data Information

func HW_handles(){
	fmt.Println("------------Start------------")
    batteries, err := bt.GetAll()
	if err != nil {
		fmt.Println("Could not get battery info!")
	}
	for i, battery := range batteries {
		fmt.Printf("Bat%d\n", i)
		fmt.Printf("state: %s\n", battery.State.String())
		fmt.Printf("current capacity: %f mWh\n", battery.Current)
		fmt.Printf("last full capacity: %f mWh\n", battery.Full)
		fmt.Printf("design capacity: %f mWh\n", battery.Design)
		fmt.Printf("charge rate: %f mW\n", battery.ChargeRate)
		fmt.Printf("voltage: %f V\n", battery.Voltage)
		fmt.Printf("design voltage: %f V\n", battery.DesignVoltage)
	}
    for {
        time.Sleep(10 * time.Millisecond)
        data = get_Data()
        File, _ = json.Marshal(data)
        //_ = os.WriteFile("Hardware_Handles.json", File, 0644)
        json.Unmarshal(File, &v)
    }
}
