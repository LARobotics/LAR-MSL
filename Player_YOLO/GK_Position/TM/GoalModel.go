package TM

import (
	"fmt"
	"image"
	"image/color"

	URG "player/GK_Position/URG_04LX_SCIP2_0"

	"gocv.io/x/gocv"
)

// Rulebook v24: [Sizes in milimeters]
/*

const GoalDepth = 500 // MINIMUM
//  If tournment field is only 18m x 12m goal width must be 2m
const GoalWidth = 2400  // Internal
const GoalHeight = 1000 // Internal
*/
// Lab Model
/*
const PostWidth = 125
const GoalWidth = 2010 // Internal Width
const GoalDepth = 400
*/
/*
// FNR Model
const PostWidth = 125
const GoalWidth = 2000 // Internal Width
const GoalDepth = 640  // Internal Depth
*/
// RoboCup Model

const PostWidth = 125
const GoalWidth = 2400 // Internal Width
const GoalDepth = 500  // Internal Depth

// MESA PAVILHÃO
/*
const PostWidth = 125  // random
const GoalWidth = 1200 // Internal Width
const GoalDepth = 400  // random
*/
const Thickness = 60

// Model Parameters
const lineWidth = 3

func CreateGoalModel(scale int) (goalModel gocv.Mat) { //(goalModel gocv.Mat)
	//plan_scale := 4 // FIX : This should be information known from the Lidar Representation
	plan_width := 256 * scale
	plan_height := 256 * scale
	t_GoalDepth := int(GoalDepth * plan_height / (URG.DistRes * 2))
	t_GoalWidth := int(GoalWidth * plan_width / (URG.DistRes * 2))
	t_PostWidth := int(PostWidth * plan_width / (URG.DistRes * 2))

	goalModel = gocv.NewMatWithSize(t_GoalDepth, t_PostWidth*2+t_GoalWidth, 0)
	defer goalModel.Close()

	var EOB image.Point = image.Point{0, 0}
	var EO image.Point = image.Point{0, t_GoalDepth}
	var EI image.Point = image.Point{t_PostWidth, t_GoalDepth}
	var EIB image.Point = image.Point{t_PostWidth, 0}

	var DOB image.Point = image.Point{t_PostWidth*2 + t_GoalWidth, 0}
	var DO image.Point = image.Point{t_PostWidth*2 + t_GoalWidth, t_GoalDepth}
	var DI image.Point = image.Point{t_PostWidth + t_GoalWidth, t_GoalDepth}
	var DIB image.Point = image.Point{t_PostWidth + t_GoalWidth, 0}

	gocv.Line(&goalModel, EOB, EO, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EO, EI, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EI, EIB, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EIB, DIB, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DIB, DI, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DI, DO, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DO, DOB, color.RGBA{255, 255, 255, 255}, lineWidth)

	gocv.IMWrite("GoalModelTemplate_Scaled2LIDAR.png", goalModel)
	fmt.Printf("😎 Created Goal Model. Resolution: %vx%v\n", goalModel.Cols(), goalModel.Rows())
	return goalModel
}
func CreateGoalModel_Pretty(scale int) (goalModel gocv.Mat) { //(goalModel gocv.Mat)
	//plan_scale := 4 // FIX : This should be information known from the Lidar Representation
	/*plan_width := 256 * scale
	plan_height := 256 * scale
	t_GoalDepth := int(GoalDepth * plan_height / (URG.DistRes * 2))
	t_GoalWidth := int(GoalWidth * plan_width / (URG.DistRes * 2))
	t_PostWidth := int(PostWidth * plan_width / (URG.DistRes * 2))
	*/
	t_GoalDepth := GoalDepth
	t_GoalWidth := GoalWidth
	t_PostWidth := PostWidth
	goalModel = gocv.NewMatWithSize(t_GoalDepth, t_PostWidth*2+t_GoalWidth, 0)
	defer goalModel.Close()

	var EOB image.Point = image.Point{0, 0}
	var EO image.Point = image.Point{0, t_GoalDepth}
	var EI image.Point = image.Point{t_PostWidth, t_GoalDepth}
	var EIB image.Point = image.Point{t_PostWidth, 0}

	var DOB image.Point = image.Point{t_PostWidth*2 + t_GoalWidth, 0}
	var DO image.Point = image.Point{t_PostWidth*2 + t_GoalWidth, t_GoalDepth}
	var DI image.Point = image.Point{t_PostWidth + t_GoalWidth, t_GoalDepth}
	var DIB image.Point = image.Point{t_PostWidth + t_GoalWidth, 0}

	var RGB_Black color.RGBA = color.RGBA{0, 0, 0, 0}
	var RGB_White color.RGBA = color.RGBA{255, 255, 255, 255}
	// Make Model Background White
	gocv.Rectangle(&goalModel, image.Rectangle{EOB, DO}, RGB_White, -1)
	// Draw Model
	gocv.Line(&goalModel, EOB, EO, RGB_Black, lineWidth)
	gocv.Line(&goalModel, EO, EI, RGB_Black, lineWidth)
	gocv.Line(&goalModel, EI, EIB, RGB_Black, lineWidth)
	gocv.Line(&goalModel, EIB, DIB, RGB_Black, lineWidth)
	gocv.Line(&goalModel, DIB, DI, RGB_Black, lineWidth)
	gocv.Line(&goalModel, DI, DO, RGB_Black, lineWidth)
	gocv.Line(&goalModel, DO, DOB, RGB_Black, lineWidth)

	gocv.IMWrite("GoalModelTemplate_Scaled2LIDAR_Pretty.png", goalModel)
	fmt.Printf("😎 Created Goal Model. Resolution: %vx%v\n", goalModel.Cols(), goalModel.Rows())
	return goalModel
}

func CreateGoalModel_FNR23(scale int) (goalModel gocv.Mat) { // Creates the model of the goal used in FNR23
	plan_scale := 256 * scale //plan_width := 256 * scale	//plan_height := 256 * scale
	t_GoalDepth := int(GoalDepth * plan_scale / (URG.DistRes * 2))
	t_GoalWidth := int(GoalWidth * plan_scale / (URG.DistRes * 2))
	t_PostWidth := int(PostWidth * plan_scale / (URG.DistRes * 2))
	t_Thickness := int(Thickness * plan_scale / (URG.DistRes * 2))

	goalModel = gocv.NewMatWithSize(t_GoalDepth+1, t_PostWidth*2+t_GoalWidth+1, 0)
	defer goalModel.Close()

	var EOB image.Point = image.Point{0, 0}
	var EOF image.Point = image.Point{0, t_GoalDepth}
	var EIF image.Point = image.Point{t_PostWidth, t_GoalDepth}
	var EIM image.Point = image.Point{t_PostWidth, t_GoalDepth - t_Thickness}
	var EOM image.Point = image.Point{t_Thickness, t_GoalDepth - t_Thickness}
	var EIB image.Point = image.Point{t_Thickness, 0}

	var DIB image.Point = image.Point{2*t_PostWidth + t_GoalWidth - t_Thickness, 0}
	var DOM image.Point = image.Point{2*t_PostWidth + t_GoalWidth - t_Thickness, t_GoalDepth - t_Thickness}
	var DIM image.Point = image.Point{t_PostWidth + t_GoalWidth, t_GoalDepth - t_Thickness}
	var DIF image.Point = image.Point{t_PostWidth + t_GoalWidth, t_GoalDepth}
	var DOF image.Point = image.Point{t_PostWidth*2 + t_GoalWidth, t_GoalDepth}
	var DOB image.Point = image.Point{t_PostWidth*2 + t_GoalWidth, 0}

	gocv.Line(&goalModel, EOB, EOF, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EOF, EIF, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EIF, EIM, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EIM, EOM, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, EOM, EIB, color.RGBA{255, 255, 255, 255}, lineWidth)

	gocv.Line(&goalModel, EIB, DIB, color.RGBA{255, 255, 255, 255}, lineWidth)

	gocv.Line(&goalModel, DIB, DOM, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DOM, DIM, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DIM, DIF, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DIF, DOF, color.RGBA{255, 255, 255, 255}, lineWidth)
	gocv.Line(&goalModel, DOF, DOB, color.RGBA{255, 255, 255, 255}, lineWidth)

	gocv.IMWrite("GoalModelTemplate_FNR.png", goalModel)
	fmt.Printf("😎 Created Goal Model. Resolution: %vx%v\n", goalModel.Cols(), goalModel.Rows())
	return goalModel
}
