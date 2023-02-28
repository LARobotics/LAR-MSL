package OmniVision_pkg

// #cgo CFLAGS: -g -Wall -w
// #cgo CFLAGS: -I/opt/spinnaker/include/spinc
// #cgo LDFLAGS: -Wl,-Bdynamic -L/opt/spinnaker/lib -lSpinnaker -lSpinnaker_C
// #include "GetCamOmni.h"
import "C"

import (
	"fmt"
	"runtime"
	"time"
	"unsafe"

	"image"
	"image/color"
	"math"
	coms "player/communication"
	"strconv"

	"github.com/xuri/excelize/v2"
	"gocv.io/x/gocv"
	"gonum.org/v1/gonum/mat"
)

// Constant to tranform Cm in our Range X
const CM_RANGE_X float64 = 1000 / (A / 2.0)

// Constant to tranform Cm in our Range Y
const CM_RANGE_Y float64 = 1000 / (B / 2.0)

// Constant to tranform Pixels in our Range X
const PIXEL_RANGE_X float64 = 1000 / ((A / 2) / 10)

// Constant to tranform Pixels in our Range Y
const PIXEL_RANGE_Y float64 = 1000 / ((B / 2) / 10)

// Cm_to_OurRange tranform Centimeters in Range between -1000(Our final line) and 1000(Against team final line).
// The value can be out of the range because the robot can be out of the field.
//
// Parameters:
//
//   - `x` : float64 -> Cm in X
//   - `y` : float64 -> Cm in Y
//
// Returns:
//
//   - `x` : int -> Range in X
//   - `y` : int -> Range in Y
func Pixels_to_MM(x, y float64) (int, int) {
	return int(100 * -(y - 210)), int(100 * -(x - 170))
}
func Cm_to_Pixels(x, y float64) (int, int) {
	return int(-(y / 10) + 170), int(-(x / 10) + 210)
}

// Cm_to_OurRange tranform Centimeters in Range between -1000(Our final line) and 1000(Against team final line).
// The value can be out of the range because the robot can be out of the field.
//
// Parameters:
//
//   - `x` : float64 -> Cm in X
//   - `y` : float64 -> Cm in Y
//
// Returns:
//
//   - `x` : int -> Range in X
//   - `y` : int -> Range in Y
func Cm_to_OurRange(x, y float64) (int, int) {
	return int(CM_RANGE_X * x), int(CM_RANGE_Y * y)
}

// Pixels_to_OurRange tranform Pixels(10cm/pixel) in Range between -1000(Our final line) and 1000(Against team final line).
// The value can be out of the range because the robot can be out of the field.
// The function is prepared to receive OpenCV values (Vision values).
//
// Parameters:
//
//   - `x` : float64 -> Pixel in X
//   - `y` : float64 -> Pixel in Y
//
// Returns:
//
//   - `x` : int -> Range in X
//   - `y` : int -> Range in Y
func Pixels_to_OurRange(x, y float64) (int, int) {
	return int(PIXEL_RANGE_X * -(y - 210)), int(PIXEL_RANGE_Y * -(x - 170))
}

// OurRange_to_Pixels tranform Pixels(10cm/pixel) in Range between -1000(Our final line) and 1000(Against team final line).
// The value can be out of the range because the robot can be out of the field.
// The function is prepared to receive OpenCV values (Vision values).
//
// Parameters:
//
//   - `x` : float64 -> Pixel in X
//   - `y` : float64 -> Pixel in Y
//
// Returns:
//
//   - `x` : int -> Range in X
//   - `y` : int -> Range in Y
func OurRange_to_Pixels(x, y float64) (int, int) {
	return int(-(y / PIXEL_RANGE_Y) + 170), int(-(x / PIXEL_RANGE_X) + 210)
}

func PrintMemUsage() {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	// For info on each, see: https://golang.org/pkg/runtime/#MemStats

	fmt.Printf("Alloc = %v MiB", bToMb(m.Alloc))
	fmt.Printf("\tTotalAlloc = %v MiB", bToMb(m.TotalAlloc))
	fmt.Printf("\tSys = %v MiB", bToMb(m.Sys))
	fmt.Printf("\tNumGC = %v\n", m.NumGC)
	//m.Close()
}

func bToMb(b uint64) uint64 {
	return b / 1024 / 1024
}

// GetOmniFrame is a function to get the next frame of Omni Camera
//
// Parameters:
//
//   - `pointer` : *C.uint8_t ->  Pointer to image data
//
// Returns:
//
//   - `image` : gocv.Mat -> Image to manipulate with gocv

func GetOmniFrame(pointer *C.uint8_t) gocv.Mat {
	pointer = C.Get_Frame()
	img_bytes := C.GoBytes(unsafe.Pointer(pointer), C.int(480*480*3))
	img, _ := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
	return img
}

// GetRealField is a function that transform the real field and transform in real field
// The resolution is 10cm for pixel
// We consider that robots can view 6 meter in each direction
//
// Parameters:
//
//   - `image_field` : gocv.Mat ->  Binary Image of Field
//   - `readed_field` : gocv.Mat -> Matrix 120x120 to save real field
//
// Returns:
//
//   - `readed_field` : gocv.Mat -> Binary Image of lines in real distance (10cm/pixel)

func GetRealField(image_field *gocv.Mat, readed_field *gocv.Mat) {

	image_field_ptr, _ := image_field.DataPtrUint8()
	readed_field_ptr, _ := readed_field.DataPtrUint8()

	delta := 0
	const MIN_LINE_WIDTH = 6 //Min Abs 2
	const MAX_LINE_WIDTH = 30

	last_pixel_field := 0

	for a := 0; a < 480; a += 5 {
		last_pixel_field = 0
		//Vertical Verification of transations green-white-green
		for y := 0; y < 480; y++ {
			if image_field_ptr[y*480+a] == 0 {
				delta = y - last_pixel_field
				if MAX_LINE_WIDTH > delta && delta > MIN_LINE_WIDTH {
					x_dist := int(real_coordenates_omni[a][int(math.Round(float64(last_pixel_field+y)/2.0))][0]/10) + 80
					y_dist := -int(real_coordenates_omni[a][int(math.Round(float64(last_pixel_field+y)/2.0))][1]/10) + 80
					if 0 < x_dist && x_dist < 160 && 0 < y_dist && y_dist < 160 {
						readed_field_ptr[y_dist*160+x_dist] = 255
						last_pixel_field = y
					}
				} else {
					last_pixel_field = y
				}
			}
		}
		last_pixel_field = 0
		//Horizontal Verification of transations green-white-green
		for x := 0; x < 480; x++ {
			if image_field_ptr[a*480+x] == 0 {
				delta = x - last_pixel_field
				if MAX_LINE_WIDTH > delta && delta > MIN_LINE_WIDTH {
					x_dist := int(real_coordenates_omni[last_pixel_field+int(delta/2)][a][0]/10) + 80
					y_dist := -int(real_coordenates_omni[last_pixel_field+int(delta/2)][a][1]/10) + 80
					if 0 < x_dist && x_dist < 160 && 0 < y_dist && y_dist < 160 {
						readed_field_ptr[y_dist*160+x_dist] = 255
						last_pixel_field = x
					}
				} else {
					last_pixel_field = x
				}
			}
		}
	}
}

// Contain all variables needed in Kalman Filter
type Kalman struct {
	X      *mat.VecDense // State
	P      *mat.Dense    // Predict
	K      *mat.Dense    // Gain
	Q      *mat.Dense    // Step Down Filter Weight⁻¹ (1000)
	R      *mat.Dense    // Vision Weight⁻¹  (100)
	R2     *mat.Dense    // Encoders Weight⁻¹ (1)
	Enc_ac *mat.VecDense // Accumulated encoders (to understand the drift)

}

// Init_Kalman is a function that init all variables of kalman filter
//
// Parameters:
//
//   - `x` : float64 ->  Initial position in X
//   - `y` : float64 ->  Initial position in Y
func (vision *OmniVision) Init_Kalman(x, y float64) {
	var new_fk Kalman
	vision.Kalman = &new_fk

	vision.Kalman.Q = mat.NewDense(2, 2, []float64{
		0.5, 0,
		0, 0.5,
	})
	vision.Kalman.R = mat.NewDense(2, 2, []float64{
		3000, 0,
		0, 3000,
	})
	vision.Kalman.R2 = mat.NewDense(2, 2, []float64{
		1100, 0,
		0, 1100,
	})
	vision.Kalman.X = mat.NewVecDense(2, []float64{
		x, y,
	})
	vision.Kalman.Enc_ac = mat.NewVecDense(2, []float64{
		x, y,
	})
	vision.Kalman.K = mat.NewDense(2, 2, []float64{
		0, 0,
		0, 0,
	})
	const initp float64 = 1
	vision.Kalman.P = mat.NewDense(2, 2, []float64{
		initp, 0,
		0, initp,
	})

}

// Update_Kalman is a function that init all variables of kalman filter
//
// Parameters:
//
//   - `x` : float64 ->  Initial position in X
//   - `y` : float64 ->  Initial position in Y
func (vision *OmniVision) Update_Kalman(x_enc, y_enc float64) (float64, float64) {

	vision.Kalman.X = mat.NewVecDense(2, []float64{
		vision.Kalman.X.AtVec(0) + x_enc, vision.Kalman.X.AtVec(1) + y_enc,
	})
	vision_Mat := mat.NewVecDense(2, []float64{
		float64(vision.x_vision), float64(vision.y_vision),
	})

	//Predict:
	//Ppriori = A*lastP*A' + Q => P = P + Q
	vision.Kalman.P.Add(vision.Kalman.P, vision.Kalman.Q)

	var P_R mat.Dense
	var invP_R mat.Dense
	var K_V_X mat.VecDense
	var K_P mat.Dense
	var V_X mat.VecDense

	//Update Vision:
	//K = Ppriori*H'/(H*Ppriori*H'+R); => K = P/P+R
	P_R.Add(vision.Kalman.P, vision.Kalman.R)
	invP_R.Inverse(&P_R)
	vision.Kalman.K.Mul(vision.Kalman.P, &invP_R)

	//X = Xpriori + K*([visionX;visionY]-H*Xpriori); => X = X + K(vision-X)
	V_X.SubVec(vision_Mat, vision.Kalman.X)
	K_V_X.MulVec(vision.Kalman.K, &V_X)
	vision.Kalman.X.AddVec(vision.Kalman.X, &K_V_X)

	//  P = P - K*H*P; => P = P - K*P
	K_P.Mul(vision.Kalman.K, vision.Kalman.P)
	vision.Kalman.P.Sub(vision.Kalman.P, &K_P)
	vision.x = int(vision.Kalman.X.AtVec(0) / 10)
	vision.y = int(vision.Kalman.X.AtVec(1) / 10)
	//vision.Out_to_excel(float64(vision.x_vision), float64(vision.y_vision), float64(vision.Kalman.Enc_ac.AtVec(0)), float64(vision.Kalman.Enc_ac.AtVec(1)), float64(vision.x), float64(vision.y))
	return float64(vision.x), float64(vision.y)
}

// struct definition
type OmniVision struct {
	x                   int      // Position in x (-1000;1000)
	y                   int      // Position in y (-1000;1000)
	x_vision            int      // Position in x vision (cm)
	y_vision            int      // Position in y vision (cm)
	x_enc               int      // Displacement encoders in x (mm)
	y_enc               int      // Displacement encoders in y (mm)
	x_ball              int      // Position in x (cm)
	y_ball              int      // Position in y (cm)
	angle               int      // Orientation
	original_image      gocv.Mat // last RGB frame
	hsv_image           gocv.Mat // last HSV frame
	ideal_field         gocv.Mat // current field
	ideal_field_to_edit gocv.Mat // to debug
	viewed_field        gocv.Mat // to debug
	viewed_ball         gocv.Mat // to debug
	viewed_allies       gocv.Mat // to debug
	viewed_green        gocv.Mat // to debug
	calc_field          gocv.Mat // to debug
	calc_rotated_field  gocv.Mat // to debug
	mask                gocv.Mat
	maxLoc              image.Point       // to debug
	pointer_camera      *C.uint8_t        // pointer camera
	window              *gocv.Window      // to debug
	record              *gocv.VideoWriter // to record
	file                *excelize.File    // to save
	index_exc           int               // to debug
	Kalman              *Kalman           // Kalman Variables
}

// OmniVision.Init() is a function to open the camera and init all variables of OmniVision.
//
// Init Follow:
//   - `OmniVision.pointer_camera` : *C.uint8_t -> Poin
//   - `OmniVision.hsv_image` : gocv.Mat ->
//   - `image` : OmniVision.gocv.Mat -> Image to manipulate with gocv
func (vision *OmniVision) Init() {
	// Allocate the new pointer where the image from C is returned.
	y := 33
	vision.pointer_camera = (*C.uint8_t)(unsafe.Pointer(&y))
	//Calling C code to open Camera
	for C.CamOmni_Open(C.int(EXPOSURE_omni), C.int(GAIN_omni), C.int(SATURATION_omni)) == 0 {
		fmt.Println("🔁️📽️ Trying open OmniCamera...")
	}
	fmt.Println("✅️📽️ OmniCamera Openned!")
	//Init Variables
	vision.hsv_image = gocv.NewMat()
	white := gocv.NewScalar(255, 255, 255, 255)
	vision.mask = gocv.NewMatWithSizeFromScalar(white, 160, 160, gocv.MatTypeCV8UC1)
	vision.calc_field = gocv.NewMatWithSize(160, 160, gocv.MatTypeCV8UC1)
	vision.calc_rotated_field = gocv.NewMatWithSize(160, 160, gocv.MatTypeCV8UC1)
	vision.viewed_field = gocv.NewMat()
	vision.viewed_ball = gocv.NewMatWithSize(480, 480, gocv.MatTypeCV8UC1)
	vision.viewed_allies = gocv.NewMatWithSize(480, 480, gocv.MatTypeCV8UC1)
	vision.viewed_green = gocv.NewMatWithSize(480, 480, gocv.MatTypeCV8UC1)
	vision.ideal_field = gocv.IMRead("OmniVision_pkg/FIELD.png", gocv.IMReadGrayScale)
	vision.ideal_field_to_edit = gocv.IMRead("OmniVision_pkg/FIELD.png", gocv.IMReadGrayScale) // USE COPY insted
	vision.record, _ = gocv.VideoWriterFile("My_Record.avi", "MJPG", 30, 480, 480, true)
	vision.file = excelize.NewFile()
	vision.index_exc = vision.file.NewSheet("Sheet1")
	vision.window = gocv.NewWindow("MAP")
	vision.Init_Kalman(0.0, -2550.0) //Testar isto
	fmt.Println("✅️📉️ Kalman Initiated!")
}

// GetFrame is a function to get the next frame of OmniVision
func (vision *OmniVision) GetFrame() gocv.Mat {
	vision.pointer_camera = C.Get_Frame()
	img_bytes := C.GoBytes(unsafe.Pointer(vision.pointer_camera), C.int(691200))
	vision.original_image, _ = gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
	return vision.original_image
}

// GetFrame_hsv is a function to get the next frame in hsv of OmniVision
//
// Parameters:
//
//   - `pointer` : *C.uint8_t ->  Pointer to image data
//
// Returns:
//
//   - `image` : gocv.Mat -> Image to manipulate with gocv
func (vision *OmniVision) GetFrame_hsv() gocv.Mat {
	vision.original_image.Close()
	vision.angle = coms.Get_bussola() // Ver isto
	vision.pointer_camera = C.Get_Frame()
	img_bytes := C.GoBytes(unsafe.Pointer(vision.pointer_camera), C.int(691200)) // 480*480*3
	img, _ := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
	vision.original_image = img
	gocv.CvtColor(img, &vision.hsv_image, gocv.ColorBGRToHSV)
	return vision.hsv_image
}

// SaveFrame is a function to get the next frame in hsv of OmniVision
//
// Parameters:
//
//   - `pointer` : *C.uint8_t ->  Pointer to image data
//
// Returns:
//
//   - `image` : gocv.Mat -> Image to manipulate with gocv
func (vision *OmniVision) Record() {
	for i := 0; i < 900; i++ {
		vision.angle = coms.Get_bussola()
		//vision.x, vision.y = coms.GetDisplacement()
		vision.pointer_camera = C.Get_Frame()

		//fmt.Println(vision.angle)
		img_bytes := C.GoBytes(unsafe.Pointer(vision.pointer_camera), C.int(480*480*3))
		img, _ := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
		vision.original_image = img
		vision.record.Write(img)
		A := "A" + strconv.Itoa(vision.index_exc)
		B := "B" + strconv.Itoa(vision.index_exc)
		C := "C" + strconv.Itoa(vision.index_exc)

		vision.file.SetCellValue("Sheet1", A, vision.angle)
		vision.file.SetCellValue("Sheet1", B, vision.x)
		vision.file.SetCellValue("Sheet1", C, vision.y)

		vision.index_exc++
	}
	vision.record.Close()
	vision.file.SetActiveSheet(vision.index_exc)
	vision.file.SaveAs("Data.xlsx")

}

var maxLoc image.Point

func Rotate(original gocv.Mat, rotated *gocv.Mat, angle int) {
	cols, rows := original.Cols(), original.Rows()
	center := image.Point{cols / 2, rows / 2}
	rotation := gocv.GetRotationMatrix2D(center, float64(-angle), 1.0)
	gocv.WarpAffineWithParams(original, rotated, rotation, image.Point{cols, rows}, gocv.InterpolationNearestNeighbor, gocv.BorderConstant, color.RGBA{0, 0, 0, 0})
}

func (vision *OmniVision) Global_Localize() (x, y int) {

	ideal_field := gocv.IMRead("OmniVision_pkg/FIELD.png", gocv.IMReadGrayScale) // USE COPY insted
	defer ideal_field.Close()
	lowerMask := gocv.NewScalar(MIN_H_lines_omni, MIN_S_lines_omni, MIN_V_lines_omni, 0.0)
	upperMask := gocv.NewScalar(MAX_H_lines_omni, MAX_S_lines_omni, MAX_V_lines_omni, 0.0)
	vision.calc_field.SetTo(gocv.NewScalar(0, 0, 0, 0))
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask, upperMask, &vision.viewed_field)
	GetRealField(&vision.viewed_field, &vision.calc_field)
	result := gocv.NewMat()
	defer result.Close()

	vision.angle = coms.Get_bussola()
	Rotate(vision.calc_field, &vision.calc_rotated_field, vision.angle)
	gocv.MatchTemplate(ideal_field, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed

	_, _, _, maxLoc := gocv.MinMaxLoc(result)
	vision.x_vision = maxLoc.X + 80
	vision.y_vision = maxLoc.Y + 80
	vision.x_vision, vision.y_vision = Pixels_to_OurRange(float64(vision.x_vision), float64(vision.y_vision))
	vision.y_vision = -vision.y_vision

	return vision.x_vision, vision.y_vision
}
func (vision *OmniVision) Close_Localize() (x, y int) {

	vision.ideal_field.CopyTo(&vision.ideal_field_to_edit)
	x_vision, y_vision := Cm_to_Pixels(float64(vision.x), float64(vision.y))
	lowerMask := gocv.NewScalar(MIN_H_lines_omni, MIN_S_lines_omni, MIN_V_lines_omni, 0.0)
	upperMask := gocv.NewScalar(MAX_H_lines_omni, MAX_S_lines_omni, MAX_V_lines_omni, 0.0)
	vision.calc_field.SetTo(gocv.NewScalar(0, 0, 0, 0))
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask, upperMask, &vision.viewed_field)
	GetRealField(&vision.viewed_field, &vision.calc_field)
	result := gocv.NewMat()
	defer result.Close()
	ideal_field_roi := vision.ideal_field_to_edit.Region(image.Rect(x_vision-105, y_vision-105, x_vision+105, y_vision+105))
	Rotate(vision.calc_field, &vision.calc_rotated_field, vision.angle)
	gocv.MatchTemplate(ideal_field_roi, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed
	_, _, _, maxLoc_roi := gocv.MinMaxLoc(result)
	vision.x_vision, vision.y_vision = Pixels_to_MM(float64(maxLoc_roi.X+x_vision-25), float64(maxLoc_roi.Y+y_vision-25))
	vision.y_vision = -vision.y_vision
	gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+x_vision-25, maxLoc_roi.Y+y_vision-25), 3, color.RGBA{155, 155, 155, 0}, -1)
	return vision.x_vision, vision.y_vision
}

var x_last_ball int
var y_last_ball int

// Temporary function... Waiting for YOLO...
func (vision *OmniVision) Get_Ball() (x, y, xr, yr int, angle float64) {
	lowerMask1 := gocv.NewScalar(MIN_H_ball_omni, MIN_S_ball_omni, MIN_V_ball_omni, 0.0)
	upperMask1 := gocv.NewScalar(MAX_H_ball_omni, MAX_S_ball_omni, MAX_V_ball_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask1, upperMask1, &vision.viewed_ball)
	contours := gocv.FindContours(vision.viewed_ball, gocv.RetrievalExternal, gocv.ChainApproxNone)
	n_balls := contours.Size()
	angle_ball := 0.0
	x_closest := 0
	y_closest := 0
	if n_balls > 0 {

		distance_closest := 100000.0
		x_closest := x_last_ball
		y_closest := y_last_ball
		n_balls_area := 0
		for index := 0; index < n_balls; index++ {
			Area := gocv.ContourArea(contours.At(index))
			if Area >= float64(MIN_Area_ball_omni) && Area <= float64(MAX_Area_ball_omni) {
				n_balls_area = 1
				rect := gocv.FitEllipse(contours.At(index))
				if rect.Center.X > 0 && rect.Center.X < 479 && rect.Center.Y > 0 && rect.Center.Y < 479 {
					distance := float64(real_coordenates_omni_ball[rect.Center.X][rect.Center.Y][2])
					if distance < distance_closest {
						distance_closest = distance
						x_closest = rect.Center.X
						y_closest = rect.Center.Y
					}
				}
			}
		}
		x := 0
		y := 0

		if n_balls_area == 1 {
			angle_ball = math.Atan2(float64(x_closest-239), -float64(y_closest-239))
			gocv.Circle(&vision.viewed_ball, image.Pt(int(x_closest), int(y_closest)), 8, color.RGBA{155, 155, 155, 0}, -1)
			angle_ball_world := angle_ball + (float64(vision.angle) * (math.Pi / 180.0))
			x_closest2 := 239 - x_closest
			y_closest2 := 239 - y_closest
			dist_closest := math.Sqrt(float64(x_closest2*x_closest2 + y_closest2*y_closest2))
			x = int(math.Round(math.Sin(angle_ball_world)*dist_closest)) + 239
			y = int(math.Round(math.Cos(angle_ball_world)*dist_closest)) + 239
			if x > 0 && x < 479 && y > 0 && y < 479 {
				x_cm := float64(real_coordenates_omni_ball[x][y][0])
				y_cm := float64(real_coordenates_omni_ball[x][y][1])
				x_last_ball = x_closest
				y_last_ball = y_closest
				vision.x_ball, vision.y_ball = Cm_to_OurRange(y_cm, x_cm)
				return vision.x_ball, vision.y_ball, x_closest, y_closest, angle_ball * 180.0 / math.Pi
			}

		}
	}
	return vision.x_ball, vision.y_ball, x_closest, y_closest, angle_ball * 180 / math.Pi
}

// Temporary function... Waiting for YOLO...
func (vision *OmniVision) Get_Allies(x_or, y_or int) (robots [5]coms.Robot_st) {
	lowerMask1 := gocv.NewScalar(MIN_H_blueshirt_omni, MIN_S_blueshirt_omni, MIN_V_blueshirt_omni, 0.0)
	upperMask1 := gocv.NewScalar(MAX_H_blueshirt_omni, MAX_S_blueshirt_omni, MAX_V_blueshirt_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask1, upperMask1, &vision.viewed_allies)
	gocv.Circle(&vision.viewed_allies, image.Pt(240, 240), 45, color.RGBA{0, 0, 0, 0}, -1)
	lowerMask2 := gocv.NewScalar(MIN_H_field_omni, MIN_S_field_omni, MIN_V_field_omni, 0.0)
	upperMask2 := gocv.NewScalar(MAX_H_field_omni, MAX_S_field_omni, MAX_V_field_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask2, upperMask2, &vision.viewed_green)
	contours := gocv.FindContours(vision.viewed_allies, gocv.RetrievalExternal, gocv.ChainApproxNone)
	n_allies := contours.Size()
	if n_allies > 0 {
		n_allies_area := 0
		image_allies_ptr, _ := vision.viewed_allies.DataPtrUint8()
		image_green_ptr, _ := vision.viewed_green.DataPtrUint8()
		for index := 0; index < n_allies; index++ {
			Area := gocv.ContourArea(contours.At(index))
			if Area >= float64(150) {
				rect := gocv.FitEllipse(contours.At(index))
				if rect.Center.X > 0 && rect.Center.X < 480 && rect.Center.Y > 0 && rect.Center.Y < 480 {
					x := 240 - rect.Center.X
					y := 240 - rect.Center.Y
					angle_allie := math.Atan2(float64(y), float64(x)) //ver quadrantes
					x_m := math.Cos(angle_allie)                      // SLope for X
					y_m := math.Sin(angle_allie)                      // Slope for Y
					h := 0.0
					x_to_view := rect.Center.X + int(math.Round(x_m*h))
					y_to_view := rect.Center.Y + int(math.Round(y_m*h))
					for x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 && image_green_ptr[y_to_view*480+x_to_view] == 0 {
						image_allies_ptr[y_to_view*480+x_to_view] = 155
						h += 1
						x_to_view = rect.Center.X + int(math.Round(x_m*h))
						y_to_view = rect.Center.Y + int(math.Round(y_m*h))

					}
					if x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 && n_allies_area < 4 {
						distance := float64(real_coordenates_omni[x_to_view][y_to_view][2])

						angle_allie_world := angle_allie + (float64(vision.angle) * (math.Pi / 180.0))

						n_allies_area += 1
						x_final, y_final := Cm_to_OurRange(math.Sin(angle_allie_world)*distance, math.Cos(angle_allie_world)*distance)
						angle_allie = angle_allie * (180.0 / math.Pi)
						robots[n_allies_area].Coords.X = float64(x_or + x_final)
						robots[n_allies_area].Coords.Y = float64(y_or - y_final)
						robots[n_allies_area].Angle = angle_allie

						vision.x_allie = robots[n_allies_area].Coords.X * 0.75
						vision.y_allie = robots[n_allies_area].Coords.Y
						vision.angle_allie = angle_allie
					}
				}
			}
		}
	}
	return robots
}

// Temporary function... Waiting for YOLO...
func (vision *OmniVision) Get_Opponent(x_or, y_or int) (robots [5]coms.Robot_st) {
	lowerMask1 := gocv.NewScalar(MIN_H_redshirt_omni, MIN_S_redshirt_omni, MIN_V_redshirt_omni, 0.0)
	upperMask1 := gocv.NewScalar(MAX_H_redshirt_omni, MAX_S_redshirt_omni, MAX_V_redshirt_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask1, upperMask1, &vision.viewed_allies)
	gocv.Circle(&vision.viewed_allies, image.Pt(240, 240), 45, color.RGBA{0, 0, 0, 0}, -1)
	lowerMask2 := gocv.NewScalar(MIN_H_field_omni, MIN_S_field_omni, MIN_V_field_omni, 0.0)
	upperMask2 := gocv.NewScalar(MAX_H_field_omni, MAX_S_field_omni, MAX_V_field_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask2, upperMask2, &vision.viewed_green)
	contours := gocv.FindContours(vision.viewed_allies, gocv.RetrievalExternal, gocv.ChainApproxNone)
	n_allies := contours.Size()
	if n_allies > 0 {
		n_allies_area := 0
		image_allies_ptr, _ := vision.viewed_allies.DataPtrUint8()
		image_green_ptr, _ := vision.viewed_green.DataPtrUint8()
		for index := 0; index < n_allies; index++ {
			Area := gocv.ContourArea(contours.At(index))
			if Area >= float64(200) {
				rect := gocv.FitEllipse(contours.At(index))
				if rect.Center.X > 0 && rect.Center.X < 480 && rect.Center.Y > 0 && rect.Center.Y < 480 {

					x := 240 - rect.Center.X
					y := 240 - rect.Center.Y
					angle_allie := math.Atan2(float64(y), float64(x)) //ver quadrantes
					x_m := math.Cos(angle_allie)                      // SLope for X
					y_m := math.Sin(angle_allie)                      // Slope for Y
					h := 0.0
					x_to_view := rect.Center.X + int(math.Round(x_m*h))
					y_to_view := rect.Center.Y + int(math.Round(y_m*h))
					for x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 && image_green_ptr[y_to_view*480+x_to_view] == 0 {
						image_allies_ptr[y_to_view*480+x_to_view] = 155
						h += 1
						x_to_view = rect.Center.X + int(math.Round(x_m*h))
						y_to_view = rect.Center.Y + int(math.Round(y_m*h))

					}
					if x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 {
						distance := float64(real_coordenates_omni[x_to_view][y_to_view][2])
						angle_allie_world := angle_allie + (float64(vision.angle) * (math.Pi / 180.0))
						n_allies_area += 1
						x_final, y_final := Cm_to_OurRange(math.Sin(angle_allie_world)*distance, math.Cos(angle_allie_world)*distance)
						robots[n_allies_area].Coords.X = float64(x_or + x_final)
						robots[n_allies_area].Coords.Y = float64(y_or - y_final)
						robots[n_allies_area].Angle = angle_allie * 180 / math.Pi
					}
				}
			}
		}
	}
	return robots
}

func Run() {

	var omnivision OmniVision
	omnivision.Init()
	omnivision.GetFrame_hsv()
	fmt.Println("🔛️🌍️ Global localization!")
	omnivision.Global_Localize()
	fmt.Println("✅️🌍️ Localization Ready!")
	window := gocv.NewWindow("Localization")
	window2 := gocv.NewWindow("Localization2")
	now := time.Now()
	last := now.UnixNano()
	fmt.Println("✅️📽️ OmniVision Ready!")
	last_ms := 0.0
	var robots_t [5]coms.Robot_st
	var robots_o [5]coms.Robot_st
	for {
		now = time.Now()
		current := now.UnixNano()
		ms := (current - last) / 1000000
		last_ms = last_ms*0.95 + float64(ms)*0.05
		fmt.Println("ℹ️ ⏱️ FPS:", 1000.0/last_ms)
		last = current

		//Get encoders
		x_enc, y_enc := coms.GetDisplacement()
		omnivision.x_enc = int(float64(x_enc))
		omnivision.y_enc = int(float64(y_enc))

		// Get Frame HSV
		omnivision.GetFrame_hsv()
		//Localize close to position
		omnivision.Close_Localize()
		//Kalman
		x, y := omnivision.Update_Kalman(float64(omnivision.x_enc), float64(omnivision.y_enc))
		x_or, y_or := Cm_to_OurRange(x/10, y/10)

		//Temporary functions... Waiting for YOLO
		x_ball, y_ball, x_closest2, y_closest2, angle_ball := omnivision.Get_Ball()
		robots_t = omnivision.Get_Allies(x_or, y_or)
		robots_o = omnivision.Get_Opponent(x_or, y_or)

		var my_ball coms.Ball_st
		my_ball.Coords.X = float64(x_or - x_ball)
		my_ball.Coords.Y = float64(y_or + y_ball)
		my_ball.Coords_rel.X = float64(x_closest2)
		my_ball.Coords_rel.Y = float64(y_closest2)
		my_ball.Z = int(angle_ball)

		//Set ball position on DB
		coms.SetBallPosition(my_ball)

		//Set robots position on DB
		coms.SetRobotsPositions(robots_t, robots_o)
		var my_robot coms.Robot_st
		my_robot.Coords.X = float64(x_or)
		my_robot.Coords.Y = float64(y_or)
		my_robot.Orientation = omnivision.angle
		//Set self position on DB
		coms.SetRobotPosition(0, my_robot)

		window.IMShow(omnivision.viewed_ball)
		window.WaitKey(5)
		window2.IMShow(omnivision.viewed_allies)
		window2.WaitKey(5)
	}

}
