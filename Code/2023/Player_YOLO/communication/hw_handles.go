package communication

import (
	"fmt"
	"io/ioutil"
	"os/exec"

	cpu "player/communication/cpu"
	bt "player/hw_handles/battery"
	"runtime"
	"strconv"
	"strings"

	"github.com/go-git/go-git/v5"
)

const batteryPath = "/sys/class/power_supply/BAT0/capacity"

// Struct related to the computer
type Computer_t struct {
	CPU, Cores                      []float64
	RAM, Loop_Time                  float64
	GPU, GPU_Temp, CPU_Temp, Batery int
}

func get_GPU() int {
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

var interation int
var CPU_d []float64

func get_CPU() float64 {
	//fmt.Println("getCPU", interation)

	if interation > 100 {
		interation = 0
		CPU_d, _ = (cpu.Percent(0, false)) //false gives one value (CPU) and true gives every core

	} else {
		interation++
	}
	if CPU_d == nil {
		CPU_d = append(CPU_d, 0.0)
	}
	return CPU_d[0]
}

func get_TempCPU() int {
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
	return int(temp / 1000.0)
	//Windows
	//fmt.Printf("CPU temperature: %d°C\n", int(temp/10.0))
	//return int(temp/10.0)
}

func get_TempGPU() int {
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

func get_RAM() float64 {
	runtime.ReadMemStats(&memStats)
	//fmt.Printf("RAM usage: %.2f MB\n", float64(memStats.Alloc)/1000000)
	return float64(memStats.Alloc) / 1000000
}
func get_PC_Battery() (batteryPercentage string) {

	content, err := ioutil.ReadFile(batteryPath)
	if err != nil {
		fmt.Printf("Failed to read battery percentage: %v\n", err)

	}

	batteryPercentage = strings.TrimSpace(string(content))

	battery, err := bt.GetAll()
	if battery[0].State.String() == "Discharging" {
		return "-" + batteryPercentage
	}
	//fmt.Printf("Battery Percentage: %s%%\n", batteryPercentage)
	return batteryPercentage
}

var File []byte

func HW_handles() {
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

}

func getCommitID() string {
	repo, err := git.PlainOpen(".")
	if err != nil {
		return ""
	}

	headRef, err := repo.Head()
	if err != nil {
		return ""
	}

	return headRef.Hash().String()[:7]
}
