package skills

import (
	"fmt"
	"image"
	"image/color"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/moethu/gosand/server/freenect"
	"gocv.io/x/gocv"

	coms "player/communication"
)

// Minium hsv values for ball filter
var M_hue = 5.0 //25.0
var M_sat = 10.0
var M_value = 100.0

// Maxium hsv values for ball filter
var m_hue = 45.0 //65.0
var m_sat = 255.0
var m_value = 255.0

var freenect_device *freenect.FreenectDevice
var led_sleep_time time.Duration
var image_quality = 100
var freenect_device_present = false

type skill_ interface {
	Oientation()
	remoteControl()
}

func getCommandParameters(package_ string, dx_ *int, dy_ *int, ori_ *int) {
	splittedString := strings.Split(package_, ",")

	*dx_, _ = strconv.Atoi(splittedString[0])
	*dy_, _ = strconv.Atoi(splittedString[1])
	*ori_, _ = strconv.Atoi(splittedString[2])
	//,_ := strconv.Atoi(splittedString[3])

}

func Skills() {
	fmt.Println("Skills")
	/*BS_channel := make(chan string)
	var command string
	var dx, dy, ori int
	*/
	for {
		/*if coms.New_BS_command {
			coms.GetBS_Command(BS_channel)
			command = <-BS_channel

			getCommandParameters(command, &dx, &dy, &ori)

			remoteControl(dx, dy, ori)
		}*/
		var dx, dy, ori int

		fmt.Scanf("%d", &dx)
		fmt.Scanf("%d", &dy)
		fmt.Scanf("%d", &ori)

		remoteControl(dx, dy, ori)
	}
}
func remoteControl(dx, dy, ori int) {
	rot, ori_aux, dir_aux := 0, 0, 0
	data_st := new(coms.MsiToEsp)
	dir_atual := dy

	ang := math.Atan2(float64(dy), float64(dx))

	vel := float64(dy) / math.Sin(ang)
	dir := ((ang * 180) / math.Pi) - float64(dir_atual)

	dir_aux = dir_atual
	ori_aux = ori

	if ori < 0 {
		ori_aux = ori + 360
	}
	if dir_atual < 0 {
		dir_aux = dir_atual + 360
	}

	if ori_aux > dir_aux {
		if ori_aux-dir_aux > 180 {
			rot = (360 - ori_aux) + dir_aux
			rot = -rot
		} else {
			rot = ori_aux - dir_aux
		}
	} else {
		if dir_aux-ori_aux > 180 {
			rot = (360 - dir_aux) + ori_aux
		} else {
			rot = dir_aux - ori_aux
			rot = -rot
		}
	}

	fmt.Print("vel: ")
	fmt.Print(vel)
	fmt.Print("   dir: ")
	fmt.Print(dir)
	fmt.Print("   rot: ")
	fmt.Println(rot)

	data_st.Velocity = int(vel)
	data_st.Angular = int(rot)
	data_st.Direction = int(dir)
	data_st.Dribbler1 = 0
	data_st.Dribbler2 = 0
	data_st.KickTime = 0

	//coms.SendESP_Parameters(*data_st)
}
func Orientation() {
	fmt.Println("Orientation")
	hsv := gocv.NewMat()
	window := gocv.NewWindow("original")
	window2 := gocv.NewWindow("Filtered2")
	window3 := gocv.NewWindow("Filtered3")
	red := color.RGBA{255, 0, 0, 0}
	cx := 0
	cy := 0
	//webcam, _ := gocv.VideoCaptureFile("testbola.mp4")
	freenect_device := freenect.NewFreenectDevice(0)

	//img := gocv.NewMat()
	if freenect_device.GetNumDevices() != 1 {
		log.Println("no single kinect device found. Starting in debug mode only.")
		freenect_device_present = false
	} else {
		fmt.Println(freenect_device)
		//ledStartup(freenect_device)
		freenect_device_present = true
	}

	if freenect_device_present {
		//ledShutdown(freenect_device)
		freenect_device.Stop()
		freenect_device.Shutdown()
	}

	img := gocv.NewMat()
	for {

		//webcam.Read(&img)
		frame := freenect_device.RGBAFrame()
		img, _ = gocv.ImageToMatRGBA(frame)
		gocv.CvtColor(img, &img, gocv.ColorBGRAToBGR)
		fmt.Printf("IMGsize:")
		fmt.Println(img.Size())
		window2.IMShow(img)
		window2.WaitKey(2)

		///////////////////////////////////left,top,right,bottom
		//croppedMat := img.Region(image.Rect(100, 250, 540, 480))
		//img = croppedMat.Clone()
		fmt.Println(img.Size())
		if img.Empty() {
			//fmt.Printf("Failed to read image: %s\n", imgPath)
			os.Exit(1)
		}

		gocv.CvtColor(img, &hsv, gocv.ColorBGRToHSV)
		img_rows, img_cols := hsv.Rows(), hsv.Cols() //hue    sat   val
		lower := gocv.NewMatWithSizeFromScalar(gocv.NewScalar(M_hue, M_sat, M_value, 0.0), img_rows, img_cols, gocv.MatTypeCV8UC3)
		upper := gocv.NewMatWithSizeFromScalar(gocv.NewScalar(m_hue, m_sat, m_value, 0.0), img_rows, img_cols, gocv.MatTypeCV8UC3)

		mask := gocv.NewMat()
		gocv.InRange(hsv, lower, upper, &mask)

		ballMask := gocv.NewMat()
		gocv.Merge([]gocv.Mat{mask, mask, mask}, &ballMask)
		gocv.BitwiseAnd(img, ballMask, &img)

		gocv.CvtColor(img, &img, gocv.ColorHSVToRGB)
		gocv.CvtColor(img, &img, gocv.ColorBGRToGray)
		window.IMShow(img)
		window.WaitKey(2)

		kernel := gocv.GetStructuringElement(gocv.MorphRect, image.Pt(10, 10))
		gocv.Dilate(img, &img, kernel)
		kernel.Close()
		//window2.WaitKey(2)

		kernel = gocv.GetStructuringElement(gocv.MorphRect, image.Pt(15, 15))
		gocv.Erode(img, &img, kernel)
		kernel.Close()
		window3.IMShow(img)
		window3.WaitKey(2)

		cnts := gocv.FindContours(img.Clone(), gocv.RetrievalExternal, gocv.ChainApproxSimple)
		fmt.Printf("GET IN thre lw\n")
		//if cnts.Size() > 0 {
		for c := 0; c < cnts.Size(); c++ {
			if gocv.ContourArea(cnts.At(c)) > 1000 {
				fmt.Println("BOLA--------------------------|!!!!!")
				//cnt := cnts.At(c)
				M := gocv.Moments(img, false)

				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])

			}
		}

		gocv.CvtColor(img, &img, gocv.ColorGrayToBGR)
		fmt.Printf("X=%d    Y=%d\n", cx, cy)
		gocv.Line(&img, image.Pt(cx, 480), image.Pt(cx, 0), red, 1)
		gocv.Line(&img, image.Pt(0, cy), image.Pt(848, cy), red, 1)
		fmt.Printf("erro:")
		fmt.Println(cx - 170)

		erro := cx - 170
		message := "R," + strconv.Itoa(erro) + "\n"
		fmt.Println("sending ... " + message)

		//coms.SendPackage(message)

	}
}

/*
	if ori_aux-dir_aux < 180 && ori_aux-dir_aux > -180 {
		rot = ori_aux - dir_aux
		rot = -rot
	} else {

		rot = dir_atual - ori
		rot = -rot
	}
*/
