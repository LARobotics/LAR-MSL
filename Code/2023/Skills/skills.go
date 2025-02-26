package skills

import (
	"fmt"
	"image"
	"image/color"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/moethu/gosand/server/freenect"
	"gocv.io/x/gocv"
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

func Orientation() {
	fmt.Println("START")
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
