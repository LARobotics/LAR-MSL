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

import (
	"context"
	"fmt"
	"image"
	"image/color"
	"log"
	"math"

	//"os"
	GK "player/GK_Position"
	coms "player/communication"
	pb "player/pb"
	"runtime"
	"time"

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
	return int(100 * -(y - 310)), int(100 * -(x - 270))
}
func Cm_to_Pixels(x, y float64) (int, int) {
	return int(-(y / 10) + 270), int(-(x / 10) + 310)
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
	const MIN_LINE_WIDTH = 1 //Min Abs 2
	const MAX_LINE_WIDTH = 60

	last_pixel_field := 0

	for a := 0; a < 480; a += 3 {
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
func Clean_OutField(readed_field *gocv.Mat, x int, y int) {
	black := color.RGBA{0, 0, 0, 0}
	Limit_L_x := 80 - ((B / 20) - y/10) - 5
	Limit_R_x := 80 + ((B / 20) + y/10) + 5
	Limit_T_y := 80 - ((A / 20) - x/10) - 5
	Limit_B_y := 80 + ((A / 20) + x/10) + 5
	//fmt.Println("Limit:",Limit_L_x,y)
	gocv.Rectangle(readed_field, image.Rect(0, 0, Limit_L_x, 160), black, -1)
	gocv.Rectangle(readed_field, image.Rect(Limit_R_x, 0, 160, 160), black, -1)
	gocv.Rectangle(readed_field, image.Rect(0, 0, 160, Limit_T_y), black, -1)
	gocv.Rectangle(readed_field, image.Rect(0, Limit_B_y, 160, 160), black, -1)
	//window := gocv.NewWindow("Cleaned_MAP")
	//window.IMShow(*readed_field)
	//window.WaitKey(0)
	//gocv.Rectangle(readed_field, r, blue, 3)
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
func (vision *OmniVision) Reset_Kalman(x, y float64) {

	vision.Kalman.X.SetVec(0, x)
	vision.Kalman.X.SetVec(1, y)

	vision.Kalman.Enc_ac.SetVec(0, x)
	vision.Kalman.Enc_ac.SetVec(1, y)
	//vision.Kalman.X.SetVec(0,x)
	//vision.Kalman.X.SetVec(1,y)
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
	window              *gocv.Window
	window2             *gocv.Window
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
	//vision.window = gocv.NewWindow("Window")
	//vision.window2 = gocv.NewWindow("Window2")

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

	vision.ideal_field.CopyTo(&vision.ideal_field_to_edit)

	//real_field.SetTo(zero)
	lowerMask := gocv.NewScalar(MIN_H_lines_omni, MIN_S_lines_omni, MIN_V_lines_omni, 0.0)
	upperMask := gocv.NewScalar(MAX_H_lines_omni, MAX_S_lines_omni, MAX_V_lines_omni, 0.0)
	vision.calc_field.SetTo(gocv.NewScalar(0, 0, 0, 0))

	gocv.InRangeWithScalar(vision.hsv_image, lowerMask, upperMask, &vision.viewed_field)
	//vision.window.IMShow(vision.hsv_image)
	//vision.window2.IMShow(vision.viewed_field)
	//vision.window.WaitKey(0)
	GetRealField(&vision.viewed_field, &vision.calc_field)
	result := gocv.NewMat()
	defer result.Close()

	Rotate(vision.calc_field, &vision.calc_rotated_field, vision.angle)
	gocv.MatchTemplate(vision.ideal_field, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed
	_, _, _, maxLoc := gocv.MinMaxLoc(result)
	vision.x_vision = maxLoc.X + 80
	vision.y_vision = maxLoc.Y + 80

	//gocv.Circle(&ideal_field, image.Pt(vision.x, vision.y), 1, color.RGBA{155, 155, 155, 0}, -1)
	//fmt.Println("posição:", vision.x_vision, vision.y_vision)
	vision.x_vision, vision.y_vision = Pixels_to_MM(float64(vision.x_vision), float64(vision.y_vision))
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
	//vision.window2.IMShow(vision.viewed_field)
	Clean_OutField(&vision.calc_rotated_field, vision.x, vision.y)
	gocv.MatchTemplate(ideal_field_roi, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed
	_, _, _, maxLoc_roi := gocv.MinMaxLoc(result)

	vision.x_vision, vision.y_vision = Pixels_to_MM(float64(maxLoc_roi.X+x_vision-25), float64(maxLoc_roi.Y+y_vision-25))
	//fmt.Println("LOC",A,vision.x_vision,vision.y_vision)
	//vision.x_vision, vision.y_vision = Pixels_to_MM(float64(maxLoc_roi.X+80), float64(maxLoc_roi.Y+80))
	//vision.y_vision = -vision.y_vision
	//fmt.Println("X: ", vision.x_vision)
	//fmt.Println("Y: ", vision.y_vision)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(x_vision, y_vision), 1, color.RGBA{255, 255, 255, 0}, -1)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+x_vision-25, maxLoc_roi.Y+y_vision-25), 3, color.RGBA{155, 155, 155, 0}, -1)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+80, maxLoc_roi.Y+80), 3, color.RGBA{155, 155, 155, 0}, -1)
	//vision.window.IMShow(vision.calc_rotated_field) //ideal_field_to_edit)

	//vision.window.WaitKey(10)

	return vision.x_vision, vision.y_vision
}

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

var last_direction_reori int
var n_interations int

func (vision *OmniVision) ReOrientation() (x, y int) {

	vision.ideal_field.CopyTo(&vision.ideal_field_to_edit)
	x_vision, y_vision := Cm_to_Pixels(float64(vision.x), float64(vision.y))
	result := gocv.NewMat()
	defer result.Close()
	ideal_field_roi := vision.ideal_field_to_edit.Region(image.Rect(x_vision-105, y_vision-105, x_vision+105, y_vision+105))
	Clean_OutField(&vision.calc_rotated_field, vision.x, vision.y)
	gocv.MatchTemplate(ideal_field_roi, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed
	_, max_val_0, _, _ := gocv.MinMaxLoc(result)

	Rotate(vision.calc_field, &vision.calc_rotated_field, 90)
	Clean_OutField(&vision.calc_rotated_field, vision.x, vision.y)
	gocv.MatchTemplate(ideal_field_roi, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed
	_, max_val_90, _, _ := gocv.MinMaxLoc(result)
	Rotate(vision.calc_field, &vision.calc_rotated_field, -90)
	Clean_OutField(&vision.calc_rotated_field, vision.x, vision.y)
	gocv.MatchTemplate(ideal_field_roi, vision.calc_rotated_field, &result, gocv.TmCcoeff, vision.mask) //TmSqdiffNormed
	_, max_val_270, _, _ := gocv.MinMaxLoc(result)
	if max_val_0 > max_val_90 && max_val_0 > max_val_270 {
		if last_direction_reori == 0 {
			n_interations += 1
		} else {
			last_direction_reori = 0
			n_interations = 0
		}

	} else if max_val_0 < max_val_90 && max_val_90 > max_val_270 {
		if last_direction_reori == 90 {
			n_interations += 1
		} else {
			last_direction_reori = 90
			n_interations = 0
		}

	} else if max_val_0 < max_val_270 && max_val_90 < max_val_270 {
		if last_direction_reori == 270 {
			n_interations += 1
		} else {
			last_direction_reori = 270
			n_interations = 0
		}

	}
	if n_interations > 30 && last_direction_reori != 0 {
		if last_direction_reori == 90 {
			vision.angle += 90
		} else {
			vision.angle -= 90
		}
	}
	//vision.x_vision, vision.y_vision = Pixels_to_MM(float64(maxLoc_roi.X+x_vision-25), float64(maxLoc_roi.Y+y_vision-25))
	//fmt.Println("LOC",A,vision.x_vision,vision.y_vision)
	//vision.x_vision, vision.y_vision = Pixels_to_MM(float64(maxLoc_roi.X+80), float64(maxLoc_roi.Y+80))
	//vision.y_vision = -vision.y_vision
	//fmt.Println("X: ", vision.x_vision)
	//fmt.Println("Y: ", vision.y_vision)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(x_vision, y_vision), 1, color.RGBA{255, 255, 255, 0}, -1)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+x_vision-25, maxLoc_roi.Y+y_vision-25), 3, color.RGBA{155, 155, 155, 0}, -1)
	//gocv.Circle(&vision.ideal_field_to_edit, image.Pt(maxLoc_roi.X+80, maxLoc_roi.Y+80), 3, color.RGBA{155, 155, 155, 0}, -1)
	//vision.window.IMShow(vision.viewed_field) //ideal_field_to_edit)
	//vision.window2.IMShow(vision.calc_rotated_field)
	//vision.window.WaitKey(10)

	return vision.x_vision, vision.y_vision
}
func adjustAngle(image_r gocv.Mat) int {
	circles := gocv.NewMat()
	defer circles.Close()
	/*gocv.HoughCirclesWithParams(
		image_r,
		&circles,
		gocv.HoughGradient,
		1,           // dp
		float64(40), // minDist
		140,         // param1
		40,          // param2
		10,          // minRadius
		30,          // maxRadius
	)*/

	//black := color.RGBA{0, 0, 0, 0}
	black := color.RGBA{155, 155, 155, 155}

	for i := 0; i < circles.Cols(); i++ {
		v := circles.GetVecfAt(0, i)
		// if circles are found
		if len(v) > 2 {
			x := int(v[0])
			y := int(v[1])
			r := int(v[2])

			gocv.Circle(&image_r, image.Pt(x, y), r, black, 5)

		}
	}

	MIN_HISTOGRAM := -10
	MAX_HISTOGRAM := 10
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
		max_values = append(max_values, histH_n[index_h]+histV_n[index_v])
		max_values = append(max_values, histV_n[index_v]+histH_n[index_h])
		//fmt.Println("I",i)
		//
		//fmt.Println("H", histH_n, index_h)
		//fmt.Println("V", histV_n, index_v)

	}

	index := ArgMax(max_values) / 2

	Rotate(image_r, &rotated, MIN_HISTOGRAM+index)
	//window2.IMShow(image_r)
	//window.IMShow(rotated)
	//window.WaitKey(10)
	//fmt.Println("Max Values:", max_values, index)
	//fmt.Println("########Ajuste", MIN_HISTOGRAM+index)
	return MIN_HISTOGRAM + index
}

// Object_in to know if the object is inside of the field or not

// Parameters:
//
//   - `dist` : float64 ->
//   - `angle` : float64 ->
//
// Returns:
//
//   - `In` : bool -> In/Out
func (vision *OmniVision) Object_in(dist int, angle int) bool {
	//vision.angle // angulo robot
	//dist // distancia obj
	//angle //angulo obj

	Obj_angle := -vision.angle + angle //angle robot
	X_obj_rel := float64(dist) * math.Sin(float64(Obj_angle)*(math.Pi/180))
	Y_obj_rel := float64(dist) * math.Cos(float64(Obj_angle)*(math.Pi/180))
	X_obj := vision.x + int(X_obj_rel)
	Y_obj := -vision.y + int(Y_obj_rel)

	if X_obj > (A/2+25) || X_obj < -(A/2-25) || Y_obj > (B/2+25) || Y_obj < -(B/2-25) {
		//fmt.Println(" Out Ball Absolut :",X_obj,Y_obj)
		return false
	} else {
		//fmt.Println(" In Ball Absolut :",X_obj,Y_obj)
		return true
	}

}

func Image_to_PrintBS(vision *OmniVision, image_to_send int) []byte {
	switch image_to_send {
	case 1:
		return vision.viewed_field.ToBytes()
		break
	case 2:
		return vision.calc_rotated_field.ToBytes()
		break

	}
	byteArray := []byte{100, 100}
	return byteArray

}
func Run(shirt bool, ip_grpc string, ID int) {
	team_shirt := shirt
	fmt.Println("🔛️👁️  OmniVision!")
	//fmt.Println("The number of CPU Cores:", runtime.GOMAXPROCS(0))
	var omnivision OmniVision
	omnivision.Init()

	addr := ip_grpc + ":40000"

	conn, err := grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("🔛️📤 GRPC Omni service openning...", addr)
	defer conn.Close()

	client := pb.NewYolo_OmniClient(conn)
	req := pb.Request_Omni_Calib{
		Check: false,
		Image: Image_to_PrintBS(&omnivision, 0),
	}
	fmt.Println("✅📤 GRPC Omni service opened!", addr)
	//omnivision.GetFrame_hsv()
	fmt.Println("🔛️🌍️ Global localization!") //0.0, 0.0 //
	N_GLOBAL_ITERATIONS := 20
	x_global := 0
	y_global := 0
	adjust := 0

	//window := gocv.NewWindow("Localization")
	//window2 := gocv.NewWindow("Detected Field")
	num_it := 0

	for i := 0; i < N_GLOBAL_ITERATIONS; i++ {
		// # Request data
		resp, err := client.Send_Omni(context.Background(), &req)
		if err != nil {
			log.Fatal(err)
		}

		image, _ := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, resp.Omni)

		gocv.CvtColor(image, &omnivision.hsv_image, gocv.ColorBGRToHSV)

		omnivision.Global_Localize()

		adjust = adjustAngle(omnivision.calc_rotated_field)

		//fmt.Println("Adjust",adjust,omnivision.x_vision,omnivision.y_vision)
		omnivision.angle = adjust
		//-180<omnivision.angle<180
		if -180 > omnivision.angle {
			adjust += 360
			omnivision.angle += 360
		}
		if omnivision.angle > 180 {
			adjust -= 360
			omnivision.angle -= 360
		}
		if omnivision.x_vision < 0 {
			x_global += omnivision.x_vision
			y_global += omnivision.y_vision
			num_it++
		}
	}
	if num_it != 0 {
		omnivision.x_vision = x_global / num_it
		omnivision.y_vision = y_global / num_it
	}
	fmt.Println("✅️🌍️ Localization Ready! X=", omnivision.x_vision, " Y=", omnivision.y_vision)
	omnivision.Init_Kalman(float64(omnivision.x_vision), float64(omnivision.y_vision))

	now := time.Now()      // current local time
	last := now.UnixNano() // number of nanoseconds since January 1, 1970 UTC

	last_ms := 0.0

	angle_ball := 0

	var last_ball coms.Ball_st
	image_to_print := 0
	fmt.Println("✅️👁️  OmniVision Ready!")
	cmps_ant := coms.Get_bussola()
	buttons := 0
	side := false

	for {
		coms.GetButtons(&buttons, &team_shirt, &side)
		//  RELOCATION
		if buttons == 2 {
			//N_GLOBAL_ITERATIONS := 20
			//x_global := 0
			//y_global := 0
			adjust := 0

			//window := gocv.NewWindow("Localization")
			//window2 := gocv.NewWindow("Detected Field")
			//num_it := 0
			adjust = adjustAngle(omnivision.calc_rotated_field)

			//fmt.Println("Adjust",adjust,omnivision.x_vision,omnivision.y_vision)
			omnivision.angle = adjust
			//-180<omnivision.angle<180

			omnivision.x_vision = -5000 //x_global / num_it
			if side {
				omnivision.y_vision = -7000 //y_global / num_it
				omnivision.x_vision = 5000
			} else {
				omnivision.y_vision = 7000
				omnivision.x_vision = -5000
			}
			omnivision.Reset_Kalman(float64(omnivision.x_vision), float64(omnivision.y_vision))

		}
		var robots_t []coms.Robot_st
		var robots_o []coms.Robot_st
		//PrintMemUsage()
		now = time.Now() // current local time
		current := now.UnixNano()
		ms := (current - last) / 1000000
		last_ms = last_ms*0.95 + float64(ms)*0.05
		//fmt.Println("ℹ️ ⏱️ FPS:", 1000.0/last_ms)
		last = current

		// # Request data
		req := pb.Request_Omni_Calib{
			Check: (image_to_print == 1 || image_to_print == 2),
			Image: Image_to_PrintBS(&omnivision, image_to_print),
		}

		resp, err := client.Send_Omni(context.Background(), &req)

		if err != nil {
			log.Fatal(err)
		}
		image_to_print = int(resp.ImgToSend)
		cmps := coms.Get_bussola()
		delta_cmps := cmps - cmps_ant
		if delta_cmps > 300 {
			delta_cmps -= 360
		}

		//omnivision.angle = coms.Get_bussola() +adjust

		omnivision.angle += int(float64(adjust)*0.30) + int(float64(delta_cmps)) //int(float64(cmps-cmps_ant)*0.50)
		cmps_ant = cmps
		//-180<omnivision.angle<180
		if -180 > omnivision.angle {
			adjust += 360
			omnivision.angle += 360
		}
		if omnivision.angle > 180 {
			adjust -= 360
			omnivision.angle -= 360
		}
		//fmt.Println("Adjust Angle", adjust, omnivision.angle)
		x_enc_rel, y_enc_rel := coms.GetDisplacement()
		to_RAD := 0.017453293
		rad_y_angle := float64(omnivision.angle) * to_RAD
		rad_x_angle := float64(omnivision.angle-90) * to_RAD

		x_enc := (float64(y_enc_rel)*math.Cos(rad_y_angle) + float64(x_enc_rel)*math.Cos(rad_x_angle))
		y_enc := (float64(y_enc_rel)*math.Sin(rad_y_angle) + float64(x_enc_rel)*math.Sin(rad_x_angle))
		//fmt.Println("Geted Displacement")
		omnivision.x_enc = int(float64(x_enc))
		omnivision.y_enc = int(float64(-y_enc))
		image, err := gocv.NewMatFromBytes(480, 480, gocv.MatTypeCV8UC3, resp.Omni)
		gocv.CvtColor(image, &omnivision.hsv_image, gocv.ColorBGRToHSV)
		omnivision.Close_Localize()
		adjust = adjustAngle(omnivision.calc_rotated_field)

		x := 0.0
		y := 0.0
		if ID == 0 {
			x_lidar, y_lidar, angle := GK.Get_GKPosition(A / 2)
			if x != 999999 || y != 999999 {
				omnivision.x_vision = x_lidar
				omnivision.y_vision = y_lidar
				x, y = omnivision.Update_Kalman(float64(omnivision.x_enc), float64(omnivision.y_enc))
				if angle > 70 || angle < -70 {
					omnivision.angle = int(angle)
				}
			} else {
				x, y = omnivision.Update_Kalman(float64(omnivision.x_enc), float64(omnivision.y_enc))
			}
		} else {
			x, y = omnivision.Update_Kalman(float64(omnivision.x_enc), float64(omnivision.y_enc))
		}
		//fmt.Println("ℹ️ 🌍️ OmniVision Position: ",x_v_or,y_v_or)
		//fmt.Println("ℹ️ 📉️ Kalman Position: ",x_or,y_or)fkick()
		//fmt.Println("ℹ️ 🏹️ Angle:", omnivision.angle)

		var my_localization coms.Robot_st
		my_localization.Coords.X = x
		my_localization.Coords.Y = -y
		my_localization.Orientation = omnivision.angle
		my_localization.Distance = 0
		robots_t = append(robots_t, my_localization)
		first_ball := true
		last_ball.Conf = 0
		for _, object := range resp.Objects {
			switch object.Id {
			case 0: // BALL

				if first_ball {
					if omnivision.Object_in(real_coordenates_omni[object.X][object.Y][2], real_coordenates_omni[object.X][object.Y][3]) {
						var my_ball coms.Ball_st
						my_ball.Coords.X = float64(real_coordenates_omni[object.X][object.Y][0])
						my_ball.Coords.Y = float64(real_coordenates_omni[object.X][object.Y][1])
						angle_ball = real_coordenates_omni[object.X][object.Y][3]
						angle_ball -= 90
						if angle_ball <= -180 {
							angle_ball += 360
						}
						angle_ball = -angle_ball
						my_ball.Angle = angle_ball
						my_ball.Dist = real_coordenates_omni[object.X][object.Y][2]
						my_ball.Conf = int(object.Conf)
						last_ball = my_ball
						first_ball = false
						//fmt.Println("ℹ️ ⚽️ Ball Position: ", my_ball.Coords.X , my_ball.Coords.Y , "Angle: ",angle_ball)
					}
				}
				break
			case 1: // BLUE_SHIRT
				if omnivision.Object_in(real_coordenates_omni[object.X][object.Y][2], real_coordenates_omni[object.X][object.Y][3]) {
					var blue_shirt coms.Robot_st
					blue_shirt.Coords.X = float64(real_coordenates_omni[object.X][object.Y][0])
					blue_shirt.Coords.Y = float64(real_coordenates_omni[object.X][object.Y][1])
					blue_shirt.Distance = real_coordenates_omni[object.X][object.Y][2]
					blue_shirt.Conf = int(object.Conf)
					angle_temp := real_coordenates_omni[object.X][object.Y][3]
					angle_temp -= 90
					if angle_temp <= -180 {
						angle_temp += 360
					}
					angle_temp = -angle_temp
					blue_shirt.Angle = angle_temp
					if team_shirt { // if blue
						robots_t = append(robots_t, blue_shirt)
					} else {
						robots_o = append(robots_o, blue_shirt)
					}
				}
				break

			case 2: // GOAL
				break

			case 3: // PERSON
				if omnivision.Object_in(real_coordenates_omni[object.X][object.Y][2], real_coordenates_omni[object.X][object.Y][3]) {
					var red_shirt coms.Robot_st
					red_shirt.Coords.X = float64(real_coordenates_omni[object.X][object.Y][0])
					red_shirt.Coords.Y = float64(real_coordenates_omni[object.X][object.Y][1])
					red_shirt.Distance = real_coordenates_omni[object.X][object.Y][2]
					red_shirt.Conf = int(object.Conf)
					angle_temp := real_coordenates_omni[object.X][object.Y][3]
					angle_temp -= 90
					if angle_temp <= -180 {
						angle_temp += 360
					}
					red_shirt.Angle = angle_temp
					robots_o = append(robots_o, red_shirt)
				}
				break

			case 4: // RED_SHIRT
				if omnivision.Object_in(real_coordenates_omni[object.X][object.Y][2], real_coordenates_omni[object.X][object.Y][3]) {
					var red_shirt coms.Robot_st
					red_shirt.Coords.X = float64(real_coordenates_omni[object.X][object.Y][0])
					red_shirt.Coords.Y = float64(real_coordenates_omni[object.X][object.Y][1])
					red_shirt.Distance = real_coordenates_omni[object.X][object.Y][2]
					red_shirt.Conf = int(object.Conf)
					angle_temp := real_coordenates_omni[object.X][object.Y][3]
					angle_temp -= 90
					if angle_temp <= -180 {
						angle_temp += 360
					}
					angle_temp = -angle_temp
					red_shirt.Angle = angle_temp
					if team_shirt { // if blue
						robots_o = append(robots_o, red_shirt)
					} else {
						robots_t = append(robots_t, red_shirt)
					}
				}
				break

			case 5: // ROBOT
				if omnivision.Object_in(real_coordenates_omni[object.X][object.Y][2], real_coordenates_omni[object.X][object.Y][3]) {
					var robot coms.Robot_st
					robot.Coords.X = float64(real_coordenates_omni[object.X][object.Y][0])
					robot.Coords.Y = float64(real_coordenates_omni[object.X][object.Y][1])
					robot.Distance = real_coordenates_omni[object.X][object.Y][2]
					angle_temp := real_coordenates_omni[object.X][object.Y][3]
					angle_temp -= 90
					if angle_temp <= -180 {
						angle_temp += 360
					}
					angle_temp = -angle_temp
					robot.Angle = angle_temp
					robots_o = append(robots_o, robot)
				}
				break

			}
		}
		coms.SetBallPosition(last_ball)
		coms.SetRobotsPositions(robots_t, robots_o)

	}
}
