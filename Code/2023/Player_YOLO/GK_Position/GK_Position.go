package GK_Position

import (
	"bufio"
	"fmt"
	"image"
	"image/color"
	"math"
	"os"
	"os/signal"
	"sync"

	TM "player/GK_Position/TM"
	URG "player/GK_Position/URG_04LX_SCIP2_0"
	coms "player/communication"

	"go.bug.st/serial"
	"gocv.io/x/gocv"
)

const PRINTAR bool = false

// Field Dimensions
const A = 22000 //22000
const B = 14000 //14000
// Robot & Lidar Properties
const BotRadius = 700 / 2 // Parameter
const BOT2LID = 200       // [mm] Parameter

type Lidar struct {
	Port         serial.Port
	Reader       *bufio.Reader
	Writer       *bufio.Writer
	Measurements []uint16
	Scale        int
	Matrix       gocv.Mat
	CenterPos    image.Point // Lidar Position
	Angle        float64
	Window       gocv.Window
}

// Mutex for the robot angle
var angle_mutex sync.Mutex

// Mutex for the robot position
var position_mutex sync.Mutex

func ArgMax(v []int) int {
	m := 0
	max_index := 0
	for i, e := range v {
		if i == 0 || e > m {
			m = e
			max_index = i
		}
	}
	return max_index
}
func Rotate(original gocv.Mat, rotated *gocv.Mat, angle int) {
	cols, rows := original.Cols(), original.Rows()
	center := image.Point{cols / 2, rows / 2}
	rotation := gocv.GetRotationMatrix2D(center, float64(-angle), 1.0)
	gocv.WarpAffineWithParams(original, rotated, rotation, image.Point{cols, rows}, gocv.InterpolationNearestNeighbor, gocv.BorderConstant, color.RGBA{0, 0, 0, 0})
}

func adjustAngle(image_r gocv.Mat) int {

	MIN_HISTOGRAM := -30
	MAX_HISTOGRAM := 30
	//window := gocv.NewWindow("ROTATIONS")
	//window2 := gocv.NewWindow("Original")
	cols, rows := image_r.Cols(), image_r.Rows()
	rotated := gocv.NewMat()
	var max_values []int

	for i := MIN_HISTOGRAM; i <= MAX_HISTOGRAM; i++ {
		Rotate(image_r, &rotated, i)
		rotated_ptr, _ := rotated.DataPtrUint8()
		var histH []int

		for x := 0; x < cols; x++ {
			count := 0
			for y := 0; y < rows; y++ {
				count += int(rotated_ptr[y*cols+x] / 255)
			}
			histH = append(histH, count)
		}

		var histV []int
		for y := 0; y < rows; y++ {
			count := 0
			for x := 0; x < cols; x++ {
				count += int(rotated_ptr[y*cols+x] / 255)
			}
			histV = append(histV, count)
		}
		//_, max_value_, _, maxLoc := gocv.MinMaxLoc(histH)
		//_, max_value_h, _, maxLoc := gocv.MinMaxLoc(histV)
		var histV_n []int
		for v := 1; v < rows-1; v++ {
			histV_n = append(histV_n, histV[v-1]+histV[v]+histV[v+1])
		}
		var histH_n []int
		for v := 1; v < cols-1; v++ {
			histH_n = append(histH_n, histH[v-1]+histH[v]+histH[v+1])
		}
		index_h := ArgMax(histH_n)
		index_v := ArgMax(histV_n)
		max_values = append(max_values, histH_n[index_h])
		max_values = append(max_values, histV_n[index_v])
		//fmt.Println("I",i)
		//
		//fmt.Println("H", histH_n, index_h)
		//fmt.Println("V", histV_n, index_v)

	}

	index := ArgMax(max_values) / 2

	//Rotate(image_r, &rotated, MIN_HISTOGRAM+index)
	//window2.IMShow(image_r)
	//window.IMShow(rotated)
	//window.WaitKey(10)
	//fmt.Println("Max Values:", max_values, index)
	//fmt.Println("########Ajuste", MIN_HISTOGRAM+index)
	return MIN_HISTOGRAM + index
}

var PosLidarRel image.Point
var posAbs image.Point
var PosAbsNorm image.Point
var PosRobotRel image.Point
var AngleR2G float64
var adjust_Angle int

type hough struct {
	threshold     int
	minLineLenght int
	maxLineGap    int
	maxLineLenght int
	angleAdjust   float64
}

func dist_PtA2PtB(A image.Point, B image.Point) (modularDist int) {
	modularDist = int(math.Sqrt(math.Pow(float64(B.X-A.X), 2) + math.Pow(float64(B.Y-A.Y), 2)))
	return modularDist
}
func LineAngle(line gocv.Veci) (angle float64) {
	var x0, x1, y0, y1 float64
	// if line[0] > line[2] {
	// 	fmt.Println("if")
	// 	x0 = float64(line[2])
	// 	y0 = float64(line[0])
	// 	x1 = float64(line[3])
	// 	y1 = float64(line[1])
	// } else {
	// fmt.Println("else")
	x0 = float64(line[0])
	y0 = float64(line[1])
	x1 = float64(line[2])
	y1 = float64(line[3])
	// }
	angle = math.Atan2(y1-y0, x1-x0) * 180 / math.Pi
	return angle
}

// maxLineLenght should be the size of the goal back surfice in Pixels
var lines gocv.Mat = gocv.NewMat()
var v gocv.Veci
var ptA, ptB image.Point
var distA2B int
var i, j int

func houghLine(edges *gocv.Mat, show *gocv.Mat, threshold int, minLineLenght float32, maxLineGap float32, maxLineLenght int) float64 {
	lines.SetTo(gocv.NewScalar(0, 0, 0, 0))
	//gocv.Canny(*edges, edges, 50, 200)
	// Run Probabilistic  Hough Line Transform
	// Binary edge map, lines matrix, rho-distance resolution, theta-angle resolution, threshold, minLineLengh, maxLineGap
	gocv.HoughLinesPWithParams(*edges, &lines, 1, math.Pi/180, threshold, minLineLenght, maxLineGap)

	if lines.Empty() {
		//fmt.Println("No lines detected")
		return 0
	}
	//fmt.Println("Detected", lines.Size()[0], "Lines")
	//fmt.Println(lines)

	for i = 0; i < lines.Rows(); i++ {
		v = lines.GetVeciAt(0, 0)
		for j = 0; j < 4; j++ {
			v = lines.GetVeciAt(j, i)
		}
		// Filter Lines out of frame
		if v[0] > 0 && v[2] > 0 && v[0] < int32(edges.Cols()) && v[2] < int32(edges.Cols()) && v[1] > 0 && v[3] > 0 && v[1] < int32(edges.Rows()) && v[3] < int32(edges.Cols()) {
			ptA = image.Point{int(v[0]), int(v[1])}
			ptB = image.Point{int(v[2]), int(v[3])}
			distA2B = dist_PtA2PtB(ptA, ptB)
			if distA2B < maxLineLenght {
				gocv.Line(show, ptA, ptB, color.RGBA{255, 20, 20, 255}, int(gocv.Line4))
				return LineAngle(v)
			}
		}
	}
	return 0 // assume the line is flat
}

func LineAngle_Standard(pt1 image.Point, pt2 image.Point) (angle float64) {
	angle = -math.Atan2(float64(pt2.Y-pt1.Y), float64(pt2.X-pt1.X)) * 180 / math.Pi
	return angle
}

func houghLine_Standard(edges *gocv.Mat, show *gocv.Mat, threshold int) (angle float64) {
	lines.SetTo(gocv.NewScalar(0, 0, 0, 0))
	// Run Standard Hough Line Transform

	gocv.HoughLines(*edges, &lines, 1, math.Pi/180, threshold)
	if lines.Empty() {
		//fmt.Println("No lines detected")
		return 0
	}
	//fmt.Println("Detected", lines.Rows(), "Standard Lines")
	//fmt.Println(lines)
	var rho_avg float64 = 0.0
	var theta_avg float64 = 0.0
	var pt1, pt2 image.Point = image.Pt(0, 0), image.Pt(0, 0)
	for i := 0; i < lines.Rows(); i++ {
		var rho float64 = float64(lines.GetFloatAt(i, 0))
		var theta float64 = float64(lines.GetFloatAt(i, 1))
		//votes := lines.GetIntAt(i, 2)

		ca := math.Cos(theta)
		co := math.Sin(theta)
		var pt0_X, pt0_Y float64 = ca * rho, co * rho
		//int(float64(img.Cols())
		pt1 = image.Point{int(pt0_X + 1000*(-co)), int(pt0_Y + 1000*ca)}
		pt2 = image.Point{int(pt0_X - 1000*(-co)), int(pt0_Y - 1000*ca)}

		gocv.Line(show, pt1, pt2, color.RGBA{255, 0, 0, 0}, 1)

		//fmt.Printf("rho: %.1f\ttheta: %.1f\tpt1: %v\tpt2: %v\tVotes: \n", rho, theta, pt1, pt2)

		//fmt.Printf("ca: %f\t co: %f\n", ca, co)
		// if v[0] > 0 && v[2] > 0 && v[0] < int32(edges.Cols()) && v[2] < int32(edges.Cols()) && v[1] > 0 && v[3] > 0 && v[1] < int32(edges.Rows()) && v[3] < int32(edges.Cols()) {
		theta_avg += theta
		rho_avg += rho
	}
	// Average lines found
	rho_avg = rho_avg / float64(lines.Rows())
	theta_avg = theta_avg / float64(lines.Rows())

	ca := math.Cos(theta_avg)
	co := math.Sin(theta_avg)
	var pt0_X, pt0_Y float64 = ca * rho_avg, co * rho_avg
	//int(float64(img.Cols())
	pt1 = image.Point{int(pt0_X + 1000*(-co)), int(pt0_Y + 1000*ca)}
	pt2 = image.Point{int(pt0_X - 1000*(-co)), int(pt0_Y - 1000*ca)}
	gocv.Line(show, pt1, pt2, color.RGBA{0, 255, 0, 0}, 1)
	// Run Standard Hough Line Transform
	return LineAngle_Standard(pt1, pt2)
}

var measure image.Point
var prevMeasure image.Point
var ang_rad float64 = 0
var angle float64 = 0

func (lidar *Lidar) PlaceMeasures() {
	// ********************** REPRESENT LIDAR MEASUREMENTS *********************
	//  Window Dimensions
	// As the point_thckness incresses the measument accuracy may decsrease
	//const plan_scale int = 3 // The processing efford increases as the plan_scale rises [1-32] 32*256 = 2*4095 <=> Two Times the LIDAR Range
	// Lowering plan_scale means losing some measument accuracy
	// Create new mat with respective size
	lidar.Matrix.SetTo(gocv.Scalar{0, 0, 0, 0})
	lidar.CenterPos = image.Pt(lidar.Matrix.Cols()/2, lidar.Matrix.Rows()/2)

	// Fill the window
	// Lidar Body represensentation in the lidar.CenterPos // FIX + Offset
	gocv.Circle(&lidar.Matrix, lidar.CenterPos, 4, color.RGBA{255, 255, 255, 255}, -1)
	// Robot Body represensentation
	//gocv.Circle(&lidar.Matrix, Lidar2RobotPosition(lidar.CenterPos, lidar.Angle), BotRadius, color.RGBA{255, 255, 255, 255}, 2)
	//gocv.Circle(&lidar.Matrix, Lidar2RobotPosition(lidar.CenterPos, lidar.Angle), 70/2, color.RGBA{255, 255, 255, 255}, 1)
	// Constansts
	//const ang_first float64 = 44 // First Measurement Angle

	//const ang_last uint16 = 725

	// Initial Values
	angle := URG.AngleRes*URG.StartStep - 45 + float64(lidar.Angle) // LIDAR angle resolution 0.3515625
	prevMeasure = image.Pt(0, 0)
	for i = 0; i < len(lidar.Measurements); i++ {
		// ** Determine X,Y of every measurement and ajust to image resolution **
		ang_rad = float64(angle) * math.Pi / 180
		measure.X = lidar.CenterPos.X + int(float64(lidar.Measurements[i])*math.Cos(ang_rad)*float64(lidar.CenterPos.X)/4095) // x = Lidar Position + cos(Measurement)
		measure.Y = lidar.CenterPos.Y - int(float64(lidar.Measurements[i])*math.Sin(ang_rad)*float64(lidar.CenterPos.Y)/4095)
		// ** Represent the measurements as white dots **

		//gocv.Circle(&lidar.Matrix, measure, 2, color.RGBA{255, 255, 255, 255}, 0)
		// ** Represent the measurements with lines in between **
		if i > 0 && dist_PtA2PtB(prevMeasure, measure) < 15 { // if the measurements distance away below the threshold
			gocv.Line(&lidar.Matrix, prevMeasure, measure, color.RGBA{255, 255, 255, 255}, 2)
		} else {
			gocv.Circle(&lidar.Matrix, measure, 1, color.RGBA{255, 255, 255, 255}, -1)
		}
		prevMeasure = measure

		// Show First, Mid, Last Measurements with a circle
		//if i == 0 || i == len(lidar)/2 || i == len(lidar)-1 {s
		//	gocv.Circle(&mat, measure, plan_scale*2, color.RGBA{255, 255, 255, 255}, 0)
		//}
		// ** Increment angle for the next measurement **
		angle += URG.AngleRes
	}
	//adjust_Angle += adjustAngle(lidar.Matrix)
}

// Convert
func pixel2MMeters(a *image.Point, scale int) {
	a.X = a.X * 4095 / ((256 * scale) / 2)
	a.Y = a.Y * 4095 / ((256 * scale) / 2)
}

// Receive the Center of the Goal Line
// Return the Relative position of the Lidar to that point
func RelativePosition_Rec(LP image.Point, GL_C image.Point, scale int) (LR image.Point) {
	LR = image.Pt(LP.X-GL_C.X, LP.Y-GL_C.Y) // With pixeis!!!!!!!!!!!!!!!!!
	pixel2MMeters(&LR, scale)               // Pixeis 2 MMeters
	return LR
}

var lr image.Point

func AbsolutePosition_Rec(LP image.Point, GL_C image.Point, scale int) (LA image.Point) {
	lr = RelativePosition_Rec(LP, GL_C, scale)
	LA = image.Pt(-A/2+lr.X, lr.Y)
	return LA
}

// Determines the Relative Position of the Robot from the Relative Position of the Lidar and Robot orientation(L)
var rad float64

// @Input Lidar Position ; Angle
// @Output Robot Position
func Lidar2RobotPosition(L image.Point, IMU float64) (R image.Point) {
	rad = float64(IMU) * math.Pi / 180
	R = image.Point{L.X + int(BOT2LID*math.Sin(rad)), L.Y + int(BOT2LID*math.Cos(rad))}
	return R
}

// Function to get the robot angle
func Get_robotAngle(DB coms.LocalDB) (this_angle float64) {
	//Lock the mutex
	/*angle_mutex.Lock()
	//If the Lidar is lost, get the angle from Database
	if TM.LidarLost {
		AngleR2G = float64(DB.Team[0].Orientation)
	}
	//Update the return angle
	this_angle = AngleR2G
	//Unlock the mutex
	angle_mutex.Unlock()*/
	this_angle = float64(DB.Team[0].Orientation)
	return
}

// Variables to filter the robot position (num_pos indicates the number of iterations)
const num_pos = 300

var position [num_pos]image.Point

func Get_robotPosition(DB coms.LocalDB, half_field int) (ret image.Point) {
	var sum float64

	//For every position, shift the array for the new position to enter
	for i := len(position) - 1; i > 0; i-- {
		position[i] = position[i-1]
	}

	/*//Verify if the Lidar is lost and get the position from Lidar or Database
	if !TM.LidarLost {
		position_mutex.Lock()
		position[0] = PosRobotRel
		position_mutex.Unlock()
	} else {
		position[0].Y = int(DB.Team[0].Coords.X*10) + half_field
		position[0].X = int(DB.Team[0].Coords.Y * 10)
	}*/
	position[0].Y = int(DB.Team[0].Coords.X*10) + half_field
	position[0].X = int(DB.Team[0].Coords.Y * 10)

	//Apply the filter for every position
	for i := 0; i < len(position); i++ {
		ret.X += position[i].X / (i + 1)
		ret.Y += position[i].Y / (i + 1)
		sum += 1 / float64(i+1)
	}

	//Return the position of the robot
	ret.X = int(float64(ret.X) / sum)
	ret.Y = int(float64(ret.Y) / sum)

	return ret
}

// Function for the omnivision. Data fusion
func Get_GKPosition(half_field_cm int) (int, int, float64) {
	var sum float64
	var ret image.Point
	var pos_robot image.Point

	for i := len(position) - 1; i > 0; i-- {
		position[i] = position[i-1]
	}

	if !TM.LidarLost {
		position_mutex.Lock()
		position[0] = PosRobotRel
		position_mutex.Unlock()
	} else {
		ret = image.Pt(999999, 999999)
		return ret.X, ret.Y, AngleR2G
	}

	for i := 0; i < len(position); i++ {
		pos_robot.X += position[i].X / (i + 1)
		pos_robot.Y += position[i].Y / (i + 1)
		sum += 1 / float64(i+1)
	}

	pos_robot.X = int(float64(pos_robot.X) / sum)
	pos_robot.Y = int(float64(pos_robot.Y) / sum)

	ret.X = (pos_robot.Y) - (half_field_cm * 10)
	ret.Y = pos_robot.X
	/* angle_mutex.Lock()
	angle = AngleR2G
	angle_mutex.Unlock() */
	return ret.X, ret.Y, AngleR2G
}

// func RelativePosition_Pol(LP image.Point, GL_C image.Point) (LR image.Point){}
func GK_Position() {
	fmt.Println("Hello Lidar!")

	//fmt.Printf("GoCV version: %s \n", gocv.Version())
	//var repWindow *gocv.Window = gocv.NewWindow("Represent Lidar")
	var hough_param hough = hough{55, 100, 45, 200, 0}
	/*repWindow.CreateTrackbarWithValue("HL_Threshold", &hough_param.threshold, 120)
	repWindow.CreateTrackbarWithValue("HL_MinL-Lenght", &hough_param.minLineLenght, 250)
	repWindow.CreateTrackbarWithValue("HL_MaxL-Gap", &hough_param.maxLineGap, 100)
	repWindow.CreateTrackbarWithValue("HL_MaxL-Lenght", &hough_param.maxLineLenght, 250)*/

	// ********* LIDAR INIT *********
	var lidar Lidar = Lidar{
		Port:         URG.Openserialport_Detailed(),
		Measurements: make([]uint16, URG.NumSteps), // 725-44+1 = 682
		Scale:        3,
		Matrix:       gocv.NewMat(),
		Angle:        0, //coms.getIMU()
		Window:       *gocv.NewWindow("LIDAR Representation"),
	}
	lidar.Matrix = gocv.NewMatWithSize(256*lidar.Scale, 256*lidar.Scale, 0)
	lidar.Writer = bufio.NewWriter(lidar.Port)
	lidar.Reader = bufio.NewReader(lidar.Port)
	// ******************************

	// Conect to LIDAR Serial Port
	//var port serial.Port = URG.Openserialport()

	// Array to store lidar measurements
	//lidar := make([]uint16, 682) //682 44-725

	//var imu_angle float64
	//var c int
	// ************** GENERATE TEMPLATE **************
	TM.CreateGoalModel(lidar.Scale)
	template := gocv.IMRead("GoalModelTemplate_Scaled2LIDAR.png", gocv.IMReadGrayScale)
	//TM.CreateGoalModel_FNR23(lidar.Scale) // SHOULD ONLY BE CALLED ONCE
	//template := gocv.IMRead("GoalModelTemplate_FNR.png", gocv.IMReadGrayScale) // Load Template for Template Match //FIX

	var close = false
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		for sig := range c {
			fmt.Printf("captured %v, stopping profiler and exiting..", sig)
			close = true
			lidar.Window.Close()
		}
	}()

	// ***********************************************
	var goalLineCenter image.Point
	var margin int = 30
	var representMat gocv.Mat = gocv.NewMat()
	//var start time.Time
	//var previous time.Time
	//var elapsed time.Duration
	//var key int
	for (lidar.Window.WaitKey(1)-27) != 0 && !close {

		//start = time.Now()
		// **** LIDAR COMMUNICATION ****
		//previous = time.Now()
		URG.SendCommand(lidar.Port, false)
		//URG.SendCommand_2(lidar.Writer, true)
		//elapsed = time.Since(previous)
		//fmt.Printf("⏰ SendCommand %vms\tFPS %.2f\n", elapsed.Milliseconds(), 1/elapsed.Seconds())

		//previous = time.Now()
		//URG.ReadCommandEcho(lidar.Port, true)
		URG.ReadCommandEcho_2(lidar.Reader, false)
		//elapsed = time.Since(previous)
		//fmt.Printf("⏰ ReadCommand %vms\tFPS %.2f\n", elapsed.Milliseconds(), 1/elapsed.Seconds())

		//previous = time.Now()
		//URG.ReadMeasure(lidar.Port, lidar.Measurements, false)
		URG.ReadMeasure_2(lidar.Reader, lidar.Measurements, false)
		//elapsed = time.Since(previous)
		//fmt.Printf("⏰ ReadMeasure %vms\tFPS %.2f\n", elapsed.Milliseconds(), 1/elapsed.Seconds())
		// *****************************
		// ********************** REPRESENT LIDAR MEASUREMENTS *********************
		//previous = time.Now()
		//float64(coms.Get_bussola())

		lidar.Angle -= hough_param.angleAdjust // Should be the current GK orientation
		//Lock angle mutex
		angle_mutex.Lock()
		if TM.LidarLost {
			lidar.Angle = AngleR2G // Use the OmniVision angle as reference for lidar representation
		} else {
			AngleR2G = lidar.Angle // Update angle to GK Vision
		}
		//Unlock angle mutex
		angle_mutex.Unlock()
		lidar.PlaceMeasures()
		//elapsed = time.Since(previous)
		//fmt.Println(template, goalLineCenter, margin)
		gocv.CvtColor(lidar.Matrix, &representMat, gocv.ColorGrayToBGR)
		//fmt.Printf("⏰ PlaceMeasure %vms\tFPS %.2f\n", elapsed.Milliseconds(), 1/elapsed.Seconds())
		/*
			ohthis := URG.ThisS{Auga: 1}
			fmt.Println(ohthis.Auga)
		*/

		//window.IMShow(mat)
		/*//Take a Sample
		if window.WaitKey(1)-112 == 0 {
			c++
			gocv.IMWrite("Frame"+fmt.Sprint(c)+".png", mat)
			fmt.Println("Saved printscreen as Frame" + fmt.Sprint(c))
		}
		*/

		// **************************************************************************
		// ***************************** Template Match *****************************
		//previous = time.Now()
		// ------------- DEBUG WITH STATIC HAZBULLA -------------
		//img := gocv.IMRead("TM/data/image.png", gocv.IMReadGrayScale)
		//template := gocv.IMRead("TM/data/template.png", gocv.IMReadGrayScale)
		// ------------------------------------------------------

		//TM.Show_All_Methods(&lidar.Matrix, template, thr)

		// Hide Noise
		if !TM.LidarLost {
			gocv.Rectangle(&lidar.Matrix, image.Rectangle{image.Point{0, 0}, image.Point{goalLineCenter.X - template.Cols()/2 - margin, lidar.Matrix.Rows()}}, color.RGBA{0, 0, 0, 0}, -1)
			gocv.Rectangle(&lidar.Matrix, image.Rectangle{image.Point{lidar.Matrix.Cols(), 0}, image.Point{goalLineCenter.X + template.Cols()/2 + margin, lidar.Matrix.Cols()}}, color.RGBA{0, 0, 0, 0}, -1)
			gocv.Rectangle(&lidar.Matrix, image.Rectangle{image.Point{0, lidar.Matrix.Rows()}, image.Point{lidar.Matrix.Cols(), goalLineCenter.Y + margin}}, color.RGBA{0, 0, 0, 0}, -1)
		} else {
			fmt.Println(" Lidar Lost: Stoped Filtering")
		}
		// Detect Goal orientation
		//hough_param.angleAdjust += 1 * houghLine(&lidar.Matrix, &representMat, hough_param.threshold, float32(hough_param.minLineLenght), float32(hough_param.maxLineGap), hough_param.maxLineLenght)
		//hough_param.angleAdjust += 1 * houghLine(&lidar.Matrix, &representMat, hough_param.threshold, float32(hough_param.minLineLenght), float32(hough_param.maxLineGap), hough_param.maxLineLenght)
		hough_param.angleAdjust = 1 * houghLine_Standard(&lidar.Matrix, &representMat, hough_param.threshold)
		gocv.PutText(&representMat, "lidar.Angle "+fmt.Sprintf("%f", lidar.Angle), image.Pt(20, 30), 1, 2, color.RGBA{255, 255, 255, 200}, 2)
		gocv.PutText(&representMat, "AngleAdjust "+fmt.Sprintf("%f", hough_param.angleAdjust), image.Pt(20, 70), 1, 2, color.RGBA{255, 255, 255, 200}, 2)
		Rotate(lidar.Matrix, &lidar.Matrix, int(hough_param.angleAdjust))
		// Ponto de referência na Baliza
		goalLineCenter = TM.Absolute_Locate_TM(&lidar.Matrix, template, TM.Methods[3], TM.Threshold, false)
		gocv.Circle(&representMat, goalLineCenter, 7, color.RGBA{20, 255, 255, 255}, -1)
		// Posição Relativa do Lidar relativamente à Baliza [Meters]
		PosLidarRel = RelativePosition_Rec(lidar.CenterPos, goalLineCenter, lidar.Scale)
		//fmt.Println("🥅 Lidar Relative Position to the Goal: ", PosLidarRel)
		// Posição Relativa do Robo relativamente à Baliza [Meters]
		position_mutex.Lock()
		PosRobotRel = Lidar2RobotPosition(PosLidarRel, lidar.Angle)
		position_mutex.Unlock()
		//fmt.Println("🥅 Robot Relative Position to the Goal: ", PosRobotRel)
		// Posição Absoluta do Lidar ( Relativamente ao Meio Campo ) [Meters]
		posAbs = AbsolutePosition_Rec(lidar.CenterPos, goalLineCenter, lidar.Scale)
		//fmt.Println("🌎 Absolute Position in Field: ", posAbs)
		// Normalizar Posição Absoluta [-1000, 1000]
		PosAbsNorm = image.Pt(posAbs.X*2000/A, posAbs.Y*2000/B)
		//fmt.Println("🗺 Normed Absolute Position in Field: ", PosAbsNorm)
		// **************************************************************************

		//key = lidar.Window.WaitKey(1)
		// ****************** Rotate ******************
		/*
			if key-'+' == 0 {
				fmt.Println(elapsed)
				lidar.Angle = lidar.Angle + 1
			} else if key-'-' == 0 {
				lidar.Angle = lidar.Angle - 1
			}
		*/
		//fmt.Println("🧭 IMU_Angle", lidar.Angle)

		// *******************************************
		// ************ Try Compass Angle ************
		/*
			if key-'*' == 0 {
				TM.Threshold += 0.01
				if TM.Threshold < 0 {
					TM.Threshold = 0
				}
			} else if key-'/' == 0 {
				TM.Threshold -= 0.01
				if TM.Threshold > 1 {
					TM.Threshold = 1
				}
			}
		*/
		//fmt.Println("🏴‍☠️ TM Threshold", TM.Threshold)
		// ********************************************
		lidar.Window.IMShow(lidar.Matrix)
		//repWindow.IMShow(representMat)
		//elapsed = time.Since(previous)
		//fmt.Printf("⏰ Represent %vms \tFPS %.2f\n", elapsed.Milliseconds(), 1/elapsed.Seconds())

		//elapsed = time.Since(start)
		//fmt.Printf("⏰ FullCycle %vms \tFPS %.2v\n", elapsed.Milliseconds(), 1/elapsed.Seconds())
	}
	lidar.Window.Close()
	//repWindow.Close()
	fmt.Println("🤢 End of the Trip!")
	os.Exit(1)
}
