// To start a new paragraph, add an empty line in the comment between the 2
// paragraphs.
//
// For example:
//
//	// Paragraph 1.
//	// Still paragraph 1.
//	//
//	// Paragraph 2.
//	// Still Paragraph 2.
//
// Results in:
//
// Paragraph 1.
// Still paragraph 1.
//
// Paragraph 2.
// Still Paragraph 2.
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
	"context"
        "log"
	//"bytes"
	"image"
	"image/color"
	"math"
	coms "player/communication"
	"strconv"
	pb "player/pb"
	"github.com/xuri/excelize/v2"
	"gocv.io/x/gocv"
	"gonum.org/v1/gonum/mat"
	"google.golang.org/grpc"
    
	//"golang.org/x/tour/pic"
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

/*
func Init_gRPC()( pb.Yolo_OmniClient, pb.Request){
	addr := "localhost:9999"
	conn, err := grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	client := pb.NewYolo_OmniClient(conn)
	req := pb.Request{
	 Check: true,
	}
	return client,req
}
*/

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

					//middle_point := last_pixel_field + int(delta/2)

					x_dist := int(real_coordenates_omni[a][int(math.Round(float64(last_pixel_field+y)/2.0))][0]/10) + 80
					y_dist := -int(real_coordenates_omni[a][int(math.Round(float64(last_pixel_field+y)/2.0))][1]/10) + 80
					//gocv.Circle(image_field, image.Pt(middle_point, a), 3, color.RGBA{155, 155, 155, 0}, -1)
					if 0 < x_dist && x_dist < 160 && 0 < y_dist && y_dist < 160 {
						//fmt.Println(int(real_coordenates_omni[last_pixel_field][a][0] / 10))
						//readed_field[x_dist][y_dist]= 255
						readed_field_ptr[y_dist*160+x_dist] = 255
						last_pixel_field = y
					}
				} else {
					last_pixel_field = y
				}
			}
		}
		last_pixel_field = 0
		// TODO:
		//
		// -> Preparar lona
		// -> Configurar Calibration para diferentes .go e fazer 3 matrizes:
		//    - float(modulo,angulo), int(X,Y) (Resolução ao centimetro) e uint8(X,Y) (Resolução ao decimetro)
		// -> Continuar este código e intregrar real_coordenates
		// -> Está quase...
		//Horizontal Verification of transations green-white-green
		for x := 0; x < 480; x++ {

			if image_field_ptr[a*480+x] == 0 {
				delta = x - last_pixel_field
				if MAX_LINE_WIDTH > delta && delta > MIN_LINE_WIDTH {
					//middle_point := last_pixel_field + int(delta/2)
					x_dist := int(real_coordenates_omni[last_pixel_field+int(delta/2)][a][0]/10) + 80
					y_dist := -int(real_coordenates_omni[last_pixel_field+int(delta/2)][a][1]/10) + 80
					//gocv.Circle(image_field, image.Pt(a, middle_point), 3, color.RGBA{155, 155, 155, 0}, -1)
					if 0 < x_dist && x_dist < 160 && 0 < y_dist && y_dist < 160 {
						//readed_field[x_dist][y_dist]= 255
						readed_field_ptr[y_dist*160+x_dist] = 255
						last_pixel_field = x
					}
				} else {
					last_pixel_field = x
				}
			}
		}
	}

	//image_field_ptr,_:= image_field.DataPtrUint8()
	//readed_field_ptr,_ := readed_field.DataPtrUint8()
	/*for y := 0; y < 480; y++ {
		for x := 0; x < 480; x++ {

			if(image_field_ptr[y*480+x]==255){
			x_dist := int(real_coordenates_omni[x][y][0]/10) + 80
			y_dist := -int(real_coordenates_omni[x][y][1]/10) + 80
			//gocv.Circle(image_field, image.Pt(a, middle_point), 3, color.RGBA{155, 155, 155, 0}, -1)
			if 0 < x_dist && x_dist < 160 && 0 < y_dist && y_dist < 160 {
				readed_field_ptr[y_dist*160+x_dist]= 255
				//readed_field.SetUCharAt(x_dist, y_dist, 255)

			}
			}
		}
	}*/
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
	//Predict:
	//Xpriori = A*lastX =>Removed
	/*enc := mat.NewVecDense(2, []float64{
		x_enc, y_enc,
	})*/
	/*vision.Kalman.Enc_ac = mat.NewVecDense(2, []float64{
		//x_enc + vision.Kalman.X.AtVec(0), y_enc + vision.Kalman.X.AtVec(1),
		x_enc + vision.Kalman.Enc_ac.AtVec(0), y_enc + vision.Kalman.Enc_ac.AtVec(1),
	})*/

	vision.Kalman.X = mat.NewVecDense(2, []float64{
		vision.Kalman.X.AtVec(0) + x_enc, vision.Kalman.X.AtVec(1) + y_enc,
	})
	vision_Mat := mat.NewVecDense(2, []float64{
		float64(vision.x_vision), float64(vision.y_vision),
	})

	//fmt.Println("Encoders:", x_enc,y_enc)
	//Ppriori = A*lastP*A' + Q => P = P + Q
	vision.Kalman.P.Add(vision.Kalman.P, vision.Kalman.Q)
	//Update Encoders (First than vision):
	//K = Ppriori*H'/(H*Ppriori*H'+R); => K = P/P+R
	var P_R mat.Dense
	//P_R.Add(vision.Kalman.P, vision.Kalman.R2)
	var invP_R mat.Dense
	//invP_R.Inverse(&P_R)
	//vision.Kalman.K.Mul(vision.Kalman.P, &invP_R)
	//X = Xpriori + K*([encX;encY]-H*Xpriori); => X = X + K(enc)
	var K_V_X mat.VecDense
	//K_V_X.MulVec(vision.Kalman.K, enc)
	//vision.Kalman.X.AddVec(vision.Kalman.X, &K_V_X)
	//  P = P - K*H*P; => P = P - K*P
	var K_P mat.Dense
	//K_P.Mul(vision.Kalman.K, vision.Kalman.P)
	//vision.Kalman.P.Sub(vision.Kalman.P, &K_P)
	//fmt.Println(mat.Formatted(vision.Kalman.X, mat.Prefix(""), mat.Excerpt(3)))
	//vision.x = int(vision.Kalman.X.AtVec(0))
	//vision.y = int(vision.Kalman.X.AtVec(1))

	//Update Vision:
	//K = Ppriori*H'/(H*Ppriori*H'+R); => K = P/P+R

	P_R.Add(vision.Kalman.P, vision.Kalman.R)

	invP_R.Inverse(&P_R)
	vision.Kalman.K.Mul(vision.Kalman.P, &invP_R)
	//X = Xpriori + K*([visionX;visionY]-H*Xpriori); => X = X + K(vision-X)
	var V_X mat.VecDense
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

// Update_Kalman is a function that init all variables of kalman filter
//
// Parameters:
//
//   - `x` : float64 ->  Initial position in X
//   - `y` : float64 ->  Initial position in Y
var last_position_x (float64)
var last_position_y (float64)

const GANHO_VISAO float64 = 0.02

func (vision *OmniVision) Update_SimpleFilter(x_enc, y_enc float64) (float64, float64) {
	position_x := x_enc + last_position_x
	position_y := y_enc + last_position_y

	position_x = position_x*(1-GANHO_VISAO) + float64(vision.x_vision)*GANHO_VISAO
	position_y = position_y*(1-GANHO_VISAO) + float64(vision.y_vision)*GANHO_VISAO
	vision.x = int(position_x / 10)
	vision.y = int(position_y / 10)
	last_position_x = position_x
	last_position_y = position_y
	return position_x, position_y
}

// struct definition
type OmniVision struct {
	x                   int     // Put in global
	y                   int     // Put in global
	x_vision            int     // Put in global
	y_vision            int     // Put in global
	x_enc               int     // Put in global
	y_enc               int     // Put in global
	x_ball              int     // Put in global
	y_ball              int     // Put in global
	x_allie             float64 //Para video
	y_allie             float64 //Para video
	angle_allie         float64
	x_allie2            float64 //Para video
	y_allie2            float64 //Para video
	angle_allie2        float64
	angle               int      // Put in global
	original_image      gocv.Mat // last RGB frame
	hsv_image           gocv.Mat // last RGB frame
	ideal_field         gocv.Mat //
	ideal_field_to_edit gocv.Mat
	viewed_field        gocv.Mat
	viewed_ball         gocv.Mat
	viewed_allies       gocv.Mat
	viewed_green        gocv.Mat
	calc_field          gocv.Mat
	calc_rotated_field  gocv.Mat
	mask                gocv.Mat
	maxLoc              image.Point
	pointer_camera      *C.uint8_t
	window              *gocv.Window
	record              *gocv.VideoWriter
	file                *excelize.File
	index_exc           int
	Kalman              *Kalman // Kalman Variables
}

// OmniVision.Init() is a function to open the camera and init all variables of OmniVision.
//
// Init Follow:
//   - `OmniVision.pointer_camera` : *C.uint8_t -> Poin
//   - `OmniVision.hsv_image` : gocv.Mat ->
//   - `image` : OmniVision.gocv.Mat -> Image to manipulate with gocv
func (vision *OmniVision) Init() {
	// Allocate the new pointer where the image from C is returned.
	/*y := 33
	vision.pointer_camera = (*C.uint8_t)(unsafe.Pointer(&y))
	//Calling C code to open Camera
	for C.CamOmni_Open(C.int(EXPOSURE_omni), C.int(GAIN_omni), C.int(SATURATION_omni)) == 0 {
		fmt.Println("🔁️📽️ Trying open OmniCamera...")
	}
	*/
	
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
	//fmt.Println("✅️📽️ Frame geted")
	img_bytes := C.GoBytes(unsafe.Pointer(vision.pointer_camera), C.int(691200))
	//fmt.Println("✅️📽️ Bytes geted")
	vision.original_image, _ = gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
	//fmt.Println("✅️📽️ New Mat From")
	//vision.original_image=img
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
	//fmt.Println("✅️📽️ Entry GetFrame")
	vision.original_image.Close()
	//fmt.Println("✅️📽️ Frame closed")
	vision.angle = coms.Get_bussola() // Ver isto
	//fmt.Println("✅️📽️ Get bussola")
	vision.pointer_camera = C.Get_Frame()
	//fmt.Println("✅️📽️ Frame geted")
	//fmt.Println(vision.angle)
	img_bytes := C.GoBytes(unsafe.Pointer(vision.pointer_camera), C.int(691200)) // 480*480*3
	//	fmt.Println("✅️📽️ NEW BYTES")
	img, _ := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
	//	fmt.Println("✅️📽️ NEW MATED")
	vision.original_image = img
	//Convert Color
	//hsv:=gocv.NewMat()
	//defer hsv.Close()
	gocv.CvtColor(img, &vision.hsv_image, gocv.ColorBGRToHSV)
	//fmt.Println("✅️📽️ CVTCOLOR")

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

// Fazer o Global
func (vision *OmniVision) Global_Localize() (x, y int) {

	ideal_field := gocv.IMRead("OmniVision_pkg/FIELD.png", gocv.IMReadGrayScale) // USE COPY insted
	defer ideal_field.Close()
	//real_field.SetTo(zero)
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
	//gocv.Circle(&ideal_field, image.Pt(vision.x, vision.y), 1, color.RGBA{155, 155, 155, 0}, -1)
	//fmt.Println("posição:", vision.x_vision, vision.y_vision)
	vision.x_vision, vision.y_vision = Pixels_to_OurRange(float64(vision.x_vision), float64(vision.y_vision))
	vision.y_vision = -vision.y_vision
	//fmt.Println("posição2:", vision.x, vision.y)
	//for{}
	return vision.x_vision, vision.y_vision
}
func (vision *OmniVision) Close_Localize() (x, y int) {
	//vision.ideal_field.Close()
	vision.ideal_field.CopyTo(&vision.ideal_field_to_edit)
	//vision.ideal_field = gocv.IMRead("OmniVision_pkg/FIELD.png", gocv.IMReadGrayScale) // USE COPY insted

	//cols, rows := vision.ideal_field.Cols(), vision.ideal_field.Rows()
	//defer ideal_field.Close()
	//real_field.SetTo(zero)
	x_vision, y_vision := Cm_to_Pixels(float64(vision.x), float64(vision.y))
	//fmt.Println("X2: ",vision.x)
	//fmt.Println("Y2: ",vision.y)

	//defer ideal_field.Close()
	//real_field.SetTo(zero)
	lowerMask := gocv.NewScalar(MIN_H_lines_omni, MIN_S_lines_omni, MIN_V_lines_omni, 0.0)
	upperMask := gocv.NewScalar(MAX_H_lines_omni, MAX_S_lines_omni, MAX_V_lines_omni, 0.0)
	//defer lowerMask.Close()
	//defer upperMask.Close()
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
	//vision.x_vision, vision.y_vision = Pixels_to_MM(float64(maxLoc_roi.X+80), float64(maxLoc_roi.Y+80))
	vision.y_vision = -vision.y_vision
	//fmt.Println("X: ", vision.x_vision)
	//fmt.Println("Y: ", vision.y_vision)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(x_vision, y_vision), 1, color.RGBA{255, 255, 255, 0}, -1)
	gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+x_vision-25, maxLoc_roi.Y+y_vision-25), 3, color.RGBA{155, 155, 155, 0}, -1)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+80, maxLoc_roi.Y+80), 3, color.RGBA{155, 155, 155, 0}, -1)
	//vision.window.IMShow(vision.ideal_field_to_edit)
	return vision.x_vision, vision.y_vision
}

func (vision *OmniVision) Get_Ball() (x, y int, angle float64) {
	lowerMask1 := gocv.NewScalar(MIN_H_ball_omni, MIN_S_ball_omni, MIN_V_ball_omni, 0.0)
	upperMask1 := gocv.NewScalar(MAX_H_ball_omni, MAX_S_ball_omni, MAX_V_ball_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask1, upperMask1, &vision.viewed_ball)
	contours := gocv.FindContours(vision.viewed_ball, gocv.RetrievalExternal, gocv.ChainApproxNone)
	//defer contour.Release()
	n_balls := contours.Size()
	angle_ball := 0.0
	if n_balls > 0 {
		//fmt.Println("ball: ",n_balls)
		distance_closest := 100000.0
		x_closest := 0
		y_closest := 0
		n_balls_area := 0

		for index := 0; index < n_balls; index++ {
			// area := gocv.ContourArea(c)

			Area := gocv.ContourArea(contours.At(index))
			//fmt.Println("area: ",Area)
			if Area >= float64(MIN_Area_ball_omni) && Area <= float64(MAX_Area_ball_omni) {
				n_balls_area = 1
				rect := gocv.FitEllipse(contours.At(index)) //-gocv.PointPolygonTest(contours.At(index),image.Point{239,239},true)
				if rect.Center.X > 0 && rect.Center.X < 479 && rect.Center.Y > 0 && rect.Center.Y < 479 {
					distance := float64(real_coordenates_omni_ball[rect.Center.X][rect.Center.Y][2])
					//real_coordenates_omni_ball[rect.Center.X][rect.Center.Y][1]
					//fmt.Println("distance: ",distance)
					if distance < distance_closest {
						distance_closest = distance
						x_closest = rect.Center.X
						y_closest = rect.Center.Y
					}
				}
			}
		}
		//fmt.Println("ball: ",n_balls)
		x := 0
		y := 0

		if n_balls_area == 1 {
			//rect:=gocv.FitEllipse(contours.At(index_closest))
			angle_ball = math.Atan2(float64(x_closest-239), -float64(y_closest-239)) //real_coordenates_omni_ball[x_closest][y_closest][3]//math.Atan2(float64(rect.Center.X-239), -float64(rect.Center.Y-239))
			//fmt.Println("angle",angle_ball*(180/math.Pi))
			//fmt.Println("loc bola2",x_closest,y_closest)
			gocv.Circle(&vision.viewed_ball, image.Pt(int(x_closest), int(y_closest)), 8, color.RGBA{155, 155, 155, 0}, -1)
			angle_ball_world := angle_ball + (float64(vision.angle) * (math.Pi / 180.0))
			//fmt.Println("ball",distance_closest, index_closest,(angle_ball)+float64(vision.angle*(math.Pi/180)),vision.angle)
			x_closest2 := 239 - x_closest
			y_closest2 := 239 - y_closest
			dist_closest := math.Sqrt(float64(x_closest2*x_closest2 + y_closest2*y_closest2))
			x = int(math.Round(math.Sin(angle_ball_world)*dist_closest)) + 239
			y = int(math.Round(math.Cos(angle_ball_world)*dist_closest)) + 239
			if x > 0 && x < 479 && y > 0 && y < 479 {
				//fmt.Println("loc bola2",x,y)
				//fmt.Println("loc bola2",x_closest2,y_closest2)
				//fmt.Println("loc bola2",x_closest,y_closest)
				x_cm := float64(real_coordenates_omni_ball[x][y][0]) //+(0.0007644274*float64(real_coordenates_omni[x][y][0])*-float64(real_coordenates_omni[x][y][0]))
				y_cm := float64(real_coordenates_omni_ball[x][y][1]) //+(0.0007644274*float64(real_coordenates_omni[x][y][1])*float64(real_coordenates_omni[x][y][1]))

				//fmt.Println("loc bola",x_cm,y_cm)
				vision.x_ball, vision.y_ball = Cm_to_OurRange(y_cm, x_cm)
				return vision.x_ball, vision.y_ball, angle_ball * 180.0 / math.Pi
			}

		}
	}
	return vision.x_ball, vision.y_ball, angle_ball * 180 / math.Pi
}

func (vision *OmniVision) Get_Allies(x_or, y_or int) (robots [5]coms.Robot_st) {
	//lowerMask1 := gocv.NewScalar(MIN_H_blueshirt_omni, MIN_S_blueshirt_omni, MIN_V_blueshirt_omni, 0.0)
	//upperMask1 := gocv.NewScalar(MAX_H_blueshirt_omni, MAX_S_blueshirt_omni, MAX_V_blueshirt_omni, 0.0)
	lowerMask1 := gocv.NewScalar(MIN_H_redshirt_omni, MIN_S_redshirt_omni, MIN_V_redshirt_omni, 0.0)
	upperMask1 := gocv.NewScalar(MAX_H_redshirt_omni, MAX_S_redshirt_omni, MAX_V_redshirt_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask1, upperMask1, &vision.viewed_allies)

	gocv.Circle(&vision.viewed_allies, image.Pt(240, 240), 100, color.RGBA{0, 0, 0, 0}, -1)

	lowerMask2 := gocv.NewScalar(MIN_H_field_omni, MIN_S_field_omni, MIN_V_field_omni, 0.0)
	upperMask2 := gocv.NewScalar(MAX_H_field_omni, MAX_S_field_omni, MAX_V_field_omni, 0.0)
	gocv.InRangeWithScalar(vision.hsv_image, lowerMask2, upperMask2, &vision.viewed_green)
	contours := gocv.FindContours(vision.viewed_allies, gocv.RetrievalExternal, gocv.ChainApproxNone)
	n_allies := contours.Size()
	robots[1].Coords.X = vision.x_allie
	robots[1].Coords.Y = vision.y_allie
	robots[1].Angle = vision.angle_allie
	robots[2].Coords.X = vision.x_allie2
	robots[2].Coords.Y = vision.y_allie2
	robots[2].Angle = vision.angle_allie2

	if n_allies > 0 {

		//fmt.Println("ball: ",n_balls)
		//distance_closest := 100000.0
		//x_closest := 0
		//y_closest := 0
		n_allies_area := 0
		image_allies_ptr, _ := vision.viewed_allies.DataPtrUint8()
		image_green_ptr, _ := vision.viewed_green.DataPtrUint8()
		for index := 0; index < n_allies && index < 5; index++ {
			// area := gocv.ContourArea(c)

			Area := gocv.ContourArea(contours.At(index))
			/*if Area > 1 {
				fmt.Println("areassss: ", Area)
			}*/
			if Area >= float64(200) {

				rect := gocv.FitEllipse(contours.At(index)) //-gocv.PointPolygonTest(contours.At(index),image.Point{239,239},true)
				//fmt.Println("Center ", rect.Center.X, rect.Center.Y)
				if rect.Center.X > 0 && rect.Center.X < 480 && rect.Center.Y > 0 && rect.Center.Y < 480 {

					x := 240 - rect.Center.X
					y := 240 - rect.Center.Y
					angle_allie := math.Atan2(float64(y), float64(x)) //ver quadrantes

					x_m := math.Cos(angle_allie) // SLope for X
					y_m := math.Sin(angle_allie) // Slope for Y

					h := 0.0
					x_to_view := rect.Center.X + int(math.Round(x_m*h))
					y_to_view := rect.Center.Y + int(math.Round(y_m*h))
					//fmt.Println("🐛️Y_to_view ",x_to_view,y_to_view)
					for x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 && image_green_ptr[y_to_view*480+x_to_view] == 0 {
						image_allies_ptr[y_to_view*480+x_to_view] = 155
						h += 1
						x_to_view = rect.Center.X + int(math.Round(x_m*h))
						y_to_view = rect.Center.Y + int(math.Round(y_m*h))

					}
					if x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 {
						//fmt.Println("Oponentpixel ",x_to_view,y_to_view)
						//fmt.Println("OponentCM ",real_coordenates_omni[x_to_view][y_to_view][0],real_coordenates_omni[x_to_view][y_to_view][1])
						distance := float64(real_coordenates_omni[x_to_view][y_to_view][2])

						angle_allie_world := angle_allie + (float64(vision.angle) * (math.Pi / 180.0))

						n_allies_area += 1
						x_final, y_final := Cm_to_OurRange(math.Sin(angle_allie_world)*distance, math.Cos(angle_allie_world)*distance)
						angle_allie = angle_allie * (180.0 / math.Pi)
						angle_allie -= 90
						if angle_allie <= -180 {
							angle_allie += 180
						}
						//fmt.Println("Angle👩‍🚀️ ", angle_allie)

						robots[n_allies_area].Coords.X = float64(x_or + x_final)
						robots[n_allies_area].Coords.Y = float64(y_or - y_final)
						robots[n_allies_area].Angle = angle_allie

						vision.x_allie = robots[n_allies_area].Coords.X * 0.75
						vision.y_allie = robots[n_allies_area].Coords.Y
						vision.angle_allie = angle_allie

						//fmt.Println("Oponent ",robots[n_allies_area].Coords.X,robots[n_allies_area].Coords.Y)
						//distance:=float64(real_coordenates_omni[rect.Center.X][rect.Center.Y][2])

						//real_coordenates_omni_ball[rect.Center.X][rect.Center.Y][1]
						//fmt.Println("distance: ",distance)
						/*if distance<distance_closest {
							distance_closest=distance
							x_closest=rect.Center.X
							y_closest=rect.Center.Y
						}*/
					}
				}
			}
		}

	}
	//fmt.Println("🔷️Allies: ", vision.x_allie2, vision.y_allie2)
	return robots
}

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
	//fmt.Println("🔶️Opponents: ",n_allies)
	if n_allies > 0 {
		//fmt.Println("ball: ",n_balls)
		//distance_closest := 100000.0
		//x_closest := 0
		//y_closest := 0
		n_allies_area := 0
		image_allies_ptr, _ := vision.viewed_allies.DataPtrUint8()
		image_green_ptr, _ := vision.viewed_green.DataPtrUint8()
		for index := 0; index < n_allies && index < 5; index++ {
			// area := gocv.ContourArea(c)

			Area := gocv.ContourArea(contours.At(index))
			//fmt.Println("area: ",Area)
			if Area >= float64(200) {

				rect := gocv.FitEllipse(contours.At(index)) //-gocv.PointPolygonTest(contours.At(index),image.Point{239,239},true)
				//fmt.Println("Center ",rect.Center.X, rect.Center.Y)
				if rect.Center.X > 0 && rect.Center.X < 480 && rect.Center.Y > 0 && rect.Center.Y < 480 {

					x := 240 - rect.Center.X
					y := 240 - rect.Center.Y
					angle_allie := math.Atan2(float64(y), float64(x)) //ver quadrantes
					//fmt.Println("Angle👩‍🚀️ ",angle_allie*(180.0/math.Pi))

					x_m := math.Cos(angle_allie) // SLope for X
					y_m := math.Sin(angle_allie) // Slope for Y

					h := 0.0
					x_to_view := rect.Center.X + int(math.Round(x_m*h))
					y_to_view := rect.Center.Y + int(math.Round(y_m*h))
					//fmt.Println("🐛️Y_to_view ", x_to_view, y_to_view)
					for x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 && image_green_ptr[y_to_view*480+x_to_view] == 0 {
						image_allies_ptr[y_to_view*480+x_to_view] = 155
						h += 1
						x_to_view = rect.Center.X + int(math.Round(x_m*h))
						y_to_view = rect.Center.Y + int(math.Round(y_m*h))

					}
					if x_to_view > 0 && x_to_view < 479 && y_to_view > 0 && y_to_view < 479 {
						//fmt.Println("Oponentpixel ",x_to_view,y_to_view)
						//fmt.Println("OponentCM ",real_coordenates_omni[x_to_view][y_to_view][0],real_coordenates_omni[x_to_view][y_to_view][1])
						distance := float64(real_coordenates_omni[x_to_view][y_to_view][2])

						angle_allie_world := angle_allie + (float64(vision.angle) * (math.Pi / 180.0))

						n_allies_area += 1
						x_final, y_final := Cm_to_OurRange(math.Sin(angle_allie_world)*distance, math.Cos(angle_allie_world)*distance)
						robots[n_allies_area].Coords.X = float64(x_or + x_final)
						robots[n_allies_area].Coords.Y = float64(y_or - y_final)
						robots[n_allies_area].Angle = angle_allie * 180 / math.Pi
						//fmt.Println("Oponent ",robots[n_allies_area].Coords.X,robots[n_allies_area].Coords.Y)
						//distance:=float64(real_coordenates_omni[rect.Center.X][rect.Center.Y][2])

						//real_coordenates_omni_ball[rect.Center.X][rect.Center.Y][1]
						//fmt.Println("distance: ",distance)
						/*if distance<distance_closest {
							distance_closest=distance
							x_closest=rect.Center.X
							y_closest=rect.Center.Y
						}*/
					}
				}
			}
		}
	}
	return robots
}

func (vision *OmniVision) Get_Frame_Routine(ch_localization, ch_ball, ch_obstacles, ch_localization_end, ch_ball_end, ch_obstacles_end chan bool) {
	now := time.Now()      // current local time
	last := now.UnixNano() // number of nanoseconds since January 1, 1970 UTC
	for {

		now = time.Now() // current local time
		current := now.UnixNano()
		fmt.Println("ℹ️ ⏱️ Time Stamp:", (current-last)/1000000)
		last = current
		//_ = <-ch_localization_end//, <-ch_ball_end//, <-ch_obstacles
		//fmt.Println("✅️📽️ Wait!")
		//Sorry for that, but is the fastest way to wait for 2 channels

		//_= <-ch_localization_end
		//_= <-ch_ball_end

		//fmt.Println("✅️📽️ Wait second!")

		//fmt.Println("✅️📽️ Run!")
		vision.GetFrame_hsv()
		ch_ball <- true
		ch_localization <- true

		//fmt.Println("✅️📽️ Send!")

		//
		//ch_obstacles <- true

	}
}

func (vision *OmniVision) Get_Localization_Routine(ch_localization, ch_localization_end, ch_localization_save chan bool) {
	for {
		//fmt.Println("✅️🌍️ Wait!")
		_ = <-ch_localization
		//fmt.Println("✅️🌍️ Run!")
		vision.Close_Localize()
		vision.Update_Kalman(float64(vision.x_enc), float64(vision.y_enc))
		//fmt.Println("✅️🌍️ Localization Get!")
		//ch_localization_end <- true
		//ch_localization_save <- true
		//fmt.Println("✅️🌍️ Localization Send!")
	}
}

func (vision *OmniVision) Get_Ball_Routine(ch_ball, ch_ball_end, ch_ball_save chan bool) {
	for {
		//fmt.Println("✅️⚽️ Wait!")
		_ = <-ch_ball
		//fmt.Println("✅️⚽️ Run!")
		vision.Get_Ball()
		//fmt.Println("✅️⚽️ Ball Get!")
		//ch_ball_end <- true
		//ch_ball_save <- true
		//fmt.Println("✅️⚽️ Ball Send!")
	}
}

func (vision *OmniVision) Save_Localization_Routine(ch_localization_save chan bool, ch_ball_save chan bool) {
	for {
		//Sorry for that but is the fastest way to wait for 2 channels

		select {
		case _ = <-ch_localization_save:
		case _ = <-ch_ball_save:

		}
		x_or, y_or := Cm_to_OurRange(float64(vision.x)/10, float64(vision.y)/10)
		//fmt.Println("ℹ️ 📉️ Kalman Position: ",x_or,y_or)
		//fmt.Println("Geted Ball")
		//fmt.Println(x_or,y_or)
		//fmt.Println(x/10,y/10)
		var my_robot coms.Robot_st
		my_robot.Coords.X = float64(x_or)
		my_robot.Coords.Y = float64(y_or)
		my_robot.Orientation = vision.angle
		coms.SetRobotPosition(0, my_robot)
		//fmt.Println("Seted Pos")
		var my_ball coms.Ball_st
		my_ball.Coords.X = float64(x_or - vision.x_ball)
		my_ball.Coords.Y = float64(y_or + vision.y_ball)
		coms.SetBallPosition(my_ball)
	}
}

func Run() {
	//fmt.Println("The number of CPU Cores:", runtime.GOMAXPROCS(0))
	var omnivision OmniVision
	omnivision.Init()
	//client, req :=Init_gRPC()
	addr := "localhost:9999"
	conn, err := grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	client := pb.NewYolo_OmniClient(conn)
	req := pb.Request{
	 Check: true,
	}
	//omnivision.GetFrame_hsv()
	fmt.Println("🔛️🌍️ Global localization!") //0.0, 0.0 //
	//omnivision.Global_Localize()
	fmt.Println("✅️🌍️ Localization Ready!")
	//window := gocv.NewWindow("Localization")
	//window2 := gocv.NewWindow("Detected Field")
	now := time.Now()      // current local time
	last := now.UnixNano() // number of nanoseconds since January 1, 1970 UTC
	fmt.Println("✅️📽️ OmniVision Ready!")
	//ch_localization := make(chan bool)	  //Channel to syncronize Camera with Localization
	//ch_ball := make(chan bool)	    	  //Channel to syncronize Camera with Ball
	//ch_obstacles := make(chan bool)   	  //Channel to syncronize Camera with Obstacles
	//ch_localization_end := make(chan bool)	  //Channel to syncronize Camera with Localization
	//ch_ball_end := make(chan bool)	    	  //Channel to syncronize Camera with Ball
	//ch_obstacles_end := make(chan bool)   	  //Channel to syncronize Camera with Obstacles
	//ch_localization_save := make(chan bool) //Channel to Save Localization
	//ch_ball_save := make(chan bool) //Channel to Save Localization
	//go omnivision.Get_Frame_Routine(ch_localization,ch_ball,ch_obstacles,ch_localization_end,ch_ball_end,ch_obstacles_end)
	//go omnivision.Get_Localization_Routine(ch_localization,ch_localization_end,ch_localization_save)
	//go omnivision.Get_Ball_Routine(ch_ball,ch_ball_end,ch_ball_save)
	//go omnivision.Save_Localization_Routine(ch_localization_save,ch_ball_save)
	//ch_localization_end<- true
	//ch_ball_end<- true
	//ch_obstacles <- true
	last_ms := 0.0
	//var robots_t [5]coms.Robot_st
	//var robots_o [5]coms.Robot_st
	angle_ball := 0.0
	x_ball_or := 0.0
	y_ball_or := 0.0 
	for {
		var robots_t [5]coms.Robot_st
		var robots_o [5]coms.Robot_st
		//PrintMemUsage()
		now = time.Now() // current local time
		current := now.UnixNano()
		ms := (current - last) / 1000000
		last_ms = last_ms*0.95 + float64(ms)*0.05
		//fmt.Println("ℹ️ ⏱️ FPS:", 1000.0/last_ms)
		last = current
		//omnivision.GetFrame()
		//window.IMShow(omnivision.original_image)//viewed_field)
		//window.WaitKey(10)
		//fmt.Println("Test ball",real_coordenates_omni_ball[160][309])
		//fmt.Println("Test ball",real_coordenates_omni[160][309])
		//ideal_field := gocv.IMRead("OmniVision_pkg/FIELD.png", gocv.IMReadGrayScale) // USE COPY insted
		//ideal_field.Close()
		//omnivision.angle= coms.Get_bussola()
		//x_enc, y_enc := coms.GetDisplacement()
		//fmt.Println("Geted Displacement")
		//omnivision.x_enc = int(float64(x_enc))
		//omnivision.y_enc = int(float64(y_enc))

		//omnivision.GetFrame_hsv()
		//window.IMShow(omnivision.original_image)//viewed_field)
		//window.WaitKey(10)
		//fmt.Println("Geted HSV")
		//_, _, _ = <-ch_localization, <-ch_ball, <-ch_obstacles

		//omnivision.Close_Localize()

		//fmt.Println("Geted Close")
		//x, y := omnivision.Update_Kalman(float64(omnivision.x_enc), float64(omnivision.y_enc))
		//x, y :=  omnivision.Update_SimpleFilter(float64(omnivision.x_enc), float64(omnivision.y_enc))

		//x_or, y_or := Cm_to_OurRange(x, y)
		//fmt.Println("Geted Update")

		//x_print, y_print := Cm_to_Pixels(x/10, y/10)

		//x_ball, y_ball, angle_ball := omnivision.Get_Ball()

		//fmt.Println("ℹ️ ⚽️ Ball Position: ", x_ball, y_ball)
		//robots_t = omnivision.Get_Allies(x_or, y_or)

		//ch_localization <- true
		//ch_ball <- true
		//ch_obstacles <- true
		//fmt.Println("ℹ️ ⚽️ Ball Position: ",x_ball,y_ball)
		//x_v_or, y_v_or :=Cm_to_OurRange(float64(omnivision.x_vision)/10,float64(omnivision.y_vision)/10)
		//fmt.Println("ℹ️ 🌍️ OmniVision Position: ",x_v_or,y_v_or)
		
		//fmt.Println("ℹ️ 📉️ Kalman Position: ",x_or,y_or)
		//fmt.Println("Geted Ball")
		//fmt.Println(x_or,y_or)
		//fmt.Println(x/10,y/10)
		//fmt.Println("ℹ️ 🏹️ Angle:", omnivision.angle)
		
	    resp, err := client.Send_Omni(context.Background(), &req)
	    if err != nil {
		 log.Fatal(err)
	    }
	    n_allies:=0
	    //image1, err := gocv.NewMatFromBytes(480,480,gocv.MatTypeCV8UC3,resp.Omni)
	    fmt.Println(resp.Objects)
	    var last_dist_ball int
	    
	    for idx,object := range resp.Objects{
	    	fmt.Println(idx,object.Id,object.X,object.Y)
	    	switch(object.Id){
	    		case 0: // BALL
	    		
	    		if (last_dist_ball>real_coordenates_omni[object.X][object.Y][2]){
	    			last_dist_ball = real_coordenates_omni[object.X][object.Y][2]
	    			x_ball, y_ball := Cm_to_OurRange(float64(real_coordenates_omni[object.X][object.Y][0]), float64(real_coordenates_omni[object.X][object.Y][1]))
	    			x_ball_or = float64(x_ball)
	    			y_ball_or = float64(y_ball)
	    			angle_ball = float64(real_coordenates_omni[object.X][object.Y][3])
	    			
	    			angle_ball-=90

	    			if angle_ball<=-180{
	    			angle_ball+=360}
	    			angle_ball=-angle_ball
	    		}
	    		case 1: // GOAL
	    			
	    		
	    		case 2: // PERSON
	    			
	    		
	    		case 3: // RED_SHIRT
	    			if(n_allies<5){
	    			n_allies++
	    			x ,y := Cm_to_OurRange(float64(real_coordenates_omni[object.X][object.Y][0]), float64(real_coordenates_omni[object.X][object.Y][1])) 
				robots_t[n_allies].Angle = float64(real_coordenates_omni[object.X][object.Y][3]) 
				robots_t[n_allies].Coords.X =float64(x)
				robots_t[n_allies].Coords.Y =float64(y)
				
				
	    		}
	    		case 4: // ROBOT
	    			
	    		
	    		
	    	}
	    
	    
		
		/*var my_robot coms.Robot_st
		my_robot.Coords.X = float64(x_or)
		my_robot.Coords.Y = float64(y_or)
		my_robot.Orientation = omnivision.angle
		//coms.SetRobotPosition(0, my_robot)
		//fmt.Println("Seted Pos")*/
		
		var my_ball coms.Ball_st
		
		my_ball.Coords.X = float64(x_ball_or)
		my_ball.Coords.Y = float64(y_ball_or)
		
		
		fmt.Println("Angle=======",angle_ball)
		my_ball.Z = int(angle_ball)
		coms.SetBallPosition(my_ball)
		coms.SetRobotsPositions(robots_t, robots_o)
		//coms.SetRobotPosition(0, my_robot)
		//fmt.Println(robots_o)

		//coms.SetBallPosition()

		//x_ball_print,y_ball_print:=OurRange_to_Pixels(my_ball.Coords.X,my_ball.Coords.Y)
		//gocv.Circle(&ideal_field, image.Pt(int(x_ball_print), int(y_ball_print)), 1, color.RGBA{200, 200, 200, 0}, -1)
		//gocv.Circle(&ideal_field, image.Pt(int(x_print), int(y_print)), 3, color.RGBA{155, 155, 155, 0}, -1)
		//gocv.Circle(&ideal_field, image.Pt(int(omnivision.x_vision), int(omnivision.y_vision)), 2, color.RGBA{255, 255, 255, 0}, -1)
		//fmt.Println("x =", x_or+x_ball, "y =", y_or+y_ball, "a =", omnivision.angle)
		//fmt.Println("px =", x_ball, "y =", y_ball, "a =", omnivision.angle)
		//fmt.Println("bx =", x_or, "y =", y_or, "a =", omnivision.angle)
		//fmt.Println("vision x =", omnivision.x_vision, "y =", omnivision.y_vision)
		//fmt.Println("enc x =", omnivision.x_enc, "y =", omnivision.y_enc)
		//window.IMShow(ideal_field)
		//window.WaitKey(5)
		//window.IMShow(omnivision.ideal_field_to_edit)
		//window.WaitKey(5)
		//window2.IMShow(omnivision.calc_rotated_field)
		//window2.WaitKey(5)
		//for{}*/
	}
	//img_bytes := C.GoBytes(unsafe.Pointer(omnivision.pointer_camera), C.int(480*480*3))
	//img, _ := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, img_bytes)
	//window := gocv.NewWindow("Localization")
	//window2 := gocv.NewWindow("Localization2")
	//window3 := gocv.NewWindow("Localization3")
	//omnivision.Record()
	//go omnivision.Close_Localize()
	/*for {
	omnivision.Record()
	omnivision.Close_Localize()

	//window.IMShow(omnivision.ideal_field)
	//window.WaitKey(20)
	window2.IMShow(omnivision.ideal_field)
	window2.WaitKey(20)
	//window3.IMShow(omnivision.original_image)
	//window3.WaitKey(20)
	}
	*/
}
}
/*
func main() {
	// Init OmniCamera
	c_pointer := Init_Omnicam()
	// New Mat OpenCV
	var img gocv.Mat
	// treshold
	//lowerMask := gocv.NewMatWithSizeFromScalar(gocv.NewScalar(30, 100.0, 50.0, 0.0), 480, 480, gocv.MatTypeCV8UC3)
	//upperMask := gocv.NewMatWithSizeFromScalar(gocv.NewScalar(70, 255.0, 255.0, 0.0), 480, 480, gocv.MatTypeCV8UC3)

	hsv := gocv.NewMat()
	field := gocv.NewMat()
	real_field := gocv.NewMatWithSize(160,160,gocv.MatTypeCV8UC1)
	//var real_field [160][160] byte
	lowerMask := gocv.NewScalar(MIN_H_lines_omni, MIN_S_lines_omni, MIN_V_lines_omni, 0.0)
	upperMask :=  gocv.NewScalar(MAX_H_lines_omni, MAX_S_lines_omni, MAX_V_lines_omni, 0.0)
	zero :=  gocv.NewScalar(0,0,0,0)
	white :=  gocv.NewScalar(255,255,255,255)
	// New Window
	window := gocv.NewWindow("Original Image")
	window2 := gocv.NewWindow("Filtred Image")
	window3 := gocv.NewWindow("Real Image")
	window4 := gocv.NewWindow("Field Position")
	window5 := gocv.NewWindow("Result")
	// Create deltatime
	dt := time.Now().UnixNano() / int64(time.Millisecond)

	//

	//var ideal_field [341][421]byte
	//real_field_zero := New_Slice(160, 160)

	mask := gocv.NewMatWithSizeFromScalar(white,160,160,gocv.MatTypeCV8UC1)

	// ###### First Verification
	// Get New Frame
	img = GetOmniFrame(c_pointer)
	ideal_field := gocv.IMRead("FIELD.png", gocv.IMReadGrayScale)
	// CODE
	//Convert Color
	gocv.CvtColor(img, &hsv, gocv.ColorBGRToHSV)
	//Treshould para campo !!! Ver Constantes  !!! Duvida de treshold com o professor
	gocv.InRangeWithScalar(hsv, lowerMask, upperMask, &field)
	real_field.SetTo(zero)
	//var real_field [160][160] uint8
	//copy(real_field_zero,real_field)
	//real_field := New_Slice(160, 160)
	GetRealField(&field, &real_field )
	result := gocv.NewMat()
	//m:=gocv.NewMat()
	gocv.MatchTemplate(ideal_field,real_field,&result,gocv.TmCcoeff,mask)//TmSqdiffNormed
	//m.Close()
	//_,maxCoefidence,_, maxLoc
	_, _, _, maxLoc := gocv.MinMaxLoc(result)
	gocv.Circle(&ideal_field,image.Pt(maxLoc.X+80,maxLoc.Y+80),3,color.RGBA{155,155,155,0},-1)

	//fmt.Println(field.GetUCharAt(340, 340))
	//field.SetUCharAt(340, 340, 0)
	// Show Image
	window4.IMShow(ideal_field)
	window4.WaitKey(20)
	window2.IMShow(field)
	window2.WaitKey(20)
	gocv.Circle(&img,image.Pt(240,240),3,color.RGBA{255,0,0,0},-1)
	window.IMShow(img)
	window.WaitKey(20)
	//pic.Show(real_field)
	//real_field_mat, _ := gocv.NewMatFromBytes(160, 160, gocv.MatTypeCV8UC1, bytes.Join(real_field,[]byte("")))
	window3.IMShow(real_field)
	window3.WaitKey(20)
	window5.IMShow(result)
	window5.WaitKey(20)
	fmt.Println("Waitng3")
	// Wait 20ms (Needed to IMShow())

	// Get deltatime
	dt_final := (time.Now().UnixNano() / int64(time.Millisecond)) - dt
	// Get new time
	dt = time.Now().UnixNano() / int64(time.Millisecond)
	// Print deltatime
	fmt.Println(dt_final)
	fmt.Println("End CYcle")

	// ###### Loop
	for {
		// Get New Frame
		img = GetOmniFrame(c_pointer)
		ideal_field := gocv.IMRead("FIELD.png", gocv.IMReadGrayScale)
		// CODE
		//Convert Color
		gocv.CvtColor(img, &hsv, gocv.ColorBGRToHSV)
		//Treshould para campo !!! Ver Constantes  !!! Duvida de treshold com o professor
		gocv.InRangeWithScalar(hsv, lowerMask, upperMask, &field)
		real_field.SetTo(zero)
		//var real_field [160][160] uint8
		//copy(real_field_zero,real_field)
		//real_field := New_Slice(160, 160)
		GetRealField(&field, &real_field )
		result := gocv.NewMat()
		//m:=gocv.NewMat()
		ideal_field_roi:=ideal_field.Region(image.Rect(maxLoc.X-(5), maxLoc.Y-(5), maxLoc.X+(5+160), maxLoc.Y+(5+160)))
		gocv.MatchTemplate(ideal_field_roi,real_field,&result,gocv.TmCcoeff,mask)//TmSqdiffNormed
		//m.Close()
		//_,maxCoefidence,_, maxLoc
		_, _, _, maxLoc_roi := gocv.MinMaxLoc(result)
		maxLoc.X=maxLoc_roi.X + maxLoc.X-(5)
		maxLoc.Y=maxLoc_roi.Y + maxLoc.Y-(5)
		gocv.Circle(&ideal_field,image.Pt(maxLoc.X+80,maxLoc.Y+80),1,color.RGBA{155,155,155,0},-1)
		//fmt.Println(field.GetUCharAt(340, 340))
		//field.SetUCharAt(340, 340, 0)
		// Show Image
		window4.IMShow(ideal_field)
		window4.WaitKey(20)
		window2.IMShow(field)
		window2.WaitKey(20)
		gocv.Circle(&img,image.Pt(240,240),3,color.RGBA{255,0,0,0},-1)
		window.IMShow(img)
		window.WaitKey(20)
		//pic.Show(real_field)
		//real_field_mat, _ := gocv.NewMatFromBytes(160, 160, gocv.MatTypeCV8UC1, bytes.Join(real_field,[]byte("")))
		window3.IMShow(real_field)
		window3.WaitKey(20)
		window5.IMShow(result)
		window5.WaitKey(20)
		fmt.Println("Waitng3")
		// Wait 20ms (Needed to IMShow())

		// Get deltatime
		dt_final := (time.Now().UnixNano() / int64(time.Millisecond)) - dt
		// Get new time
		dt = time.Now().UnixNano() / int64(time.Millisecond)
		// Print deltatime
		fmt.Println(dt_final)
		fmt.Println("End CYcle")

	}
}*/
