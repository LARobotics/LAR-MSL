package TM

import (
	"fmt"
	"image"
	"image/color"

	"log"

	"gocv.io/x/gocv"
)

var Methods [6]gocv.TemplateMatchMode = [6]gocv.TemplateMatchMode{gocv.TmSqdiff, gocv.TmSqdiffNormed, gocv.TmCcorr, gocv.TmCcorrNormed, gocv.TmCcoeff, gocv.TmCcoeffNormed}

/*
	0 - SSD	(Sum of Squared Differences)
	1 - NSSD(Normalized Sum of Squared Differences)
	2 - CC	(Cross Correlation)
	3 - NCC	(Normalized Cross Correlation) 			[-1 ,(1)]
	4 -
	5 - ZNCC (Zero-normalized Cross Correlation)
*/
/*
	type Goalkeeper struct {
		frame    gocv.Mat
		template gocv.Mat
		window   *gocv.Window
	}
*/
var Threshold float32 = 1 // Calibrate Threshold fot Template Match // Parameter
var prevMatch image.Point
var LidarLost bool = false

// Try all TM Methods. NOTE: Should be called iteratively
/*
func TryMethods(frame gocv.Mat, template gocv.Mat, show bool) { // NOT WORKING : FOR SOME REASON THE FRAMES ARE ALL THE SAME
	fmt.Println("Trying Methods")
	var frames [6]gocv.Mat = [6]gocv.Mat{}

	frame.Rows() := frame.Rows()
	frame.Cols() := frame.Cols()
	template.Rows() := template.Rows()
	template.Cols() := template.Cols()

	var best_loc image.Point
	var best_meth_min gocv.TemplateMatchMode
	var best_meth_max gocv.TemplateMatchMode
	var best_val float32
	mask := gocv.NewMat()

	for i, meth := range Methods {
		result := gocv.NewMatWithSize(frame.Rows(), frame.Cols(), 0)
		gocv.MatchTemplate(frame, template, &result, meth, mask)
		min_val, max_val, min_loc, max_loc := gocv.MinMaxLoc(result)

		// If method is TmSqdiff or TmSqdiffNormed the best matching location is returned as the minimum location
		// The point refers to the top left corner where the template was most accurate
		if meth == gocv.TmSqdiff || meth == gocv.TmSqdiffNormed {
			best_loc = min_loc
			if min_val < best_val {
				best_val = min_val
				best_meth_min = meth
			}
		} else {
			best_loc = max_loc
			if max_val > best_val {
				best_val = max_val
				best_meth_max = meth
			}
		}

		// SHOW RESULTS
		bot_right := image.Point{best_loc.X + template.Cols(), best_loc.Y + template.Rows()}
		gocv.Rectangle(&frame, image.Rectangle{best_loc, bot_right}, color.RGBA{255, 255, 255, 255}, 2)
		gocv.PutText(&frame, fmt.Sprint(template.Rows()), image.Point{best_loc.X - template.Cols()/4, best_loc.Y + template.Rows()/4}, gocv.FontHersheySimplex, 1, color.RGBA{120, 120, 120, 255}, 2)
		gocv.PutText(&frame, fmt.Sprint(template.Cols()), image.Point{best_loc.X + template.Cols()/4, best_loc.Y - template.Rows()/4}, gocv.FontHersheySimplex, 1, color.RGBA{120, 120, 120, 255}, 2)
		frames[i] = frame
		if show {
			// Template Match Method Results
			fmt.Printf("TM_Method: %v %v\n\tmin_val: %v\tmax_val: %v\t best_loc: ( %d , %d )\n", i, meth, min_val, max_val, best_loc.X, best_loc.Y)
		}
	}
	fmt.Println("Best Max Min Meths", best_meth_max, best_meth_min)

	if show {
		var winTrial [6]gocv.Window
		for i := 0; i <= 5; i++ {
			trials := frames
			// Create a window for each method representation
			winTrial[i] = *gocv.NewWindow("Method" + fmt.Sprint(Methods[i]))
			// Place windows separated in the screen
			if i <= 2 {
				winTrial[i].MoveWindow(10+i*frame.Cols()/3, 10)
			} else {
				winTrial[i].MoveWindow(10+(i-3)*frame.Cols()/3, 10+frame.Rows()/2)
			}
			if Methods[i] == best_meth_min || Methods[i] == best_meth_max {
				gocv.PutText(&trials[i], "Best Method", image.Point{10, 20}, gocv.FontHersheySimplex, 1, color.RGBA{120, 120, 120, 255}, 2)
			}
			if i == 1 {
				gocv.Line(&trials[i], image.Point{trials[i].Cols(), trials[i].Rows()}, image.Point{0, 0}, color.RGBA{255, 255, 255, 255}, 5)
			}
			winTrial[i].IMShow(trials[i])
		}
		// close all method representation windows
		if winTrial[0].WaitKey(1)-113 == 0 {
			for i := 0; i <= 5; i++ {
				winTrial[i].Close()
			}
		}
	}
}*/
var Angle_hist int
var mask gocv.Mat = gocv.NewMat()
var result gocv.Mat = gocv.NewMat()
var min_val, max_val float32
var min_loc, max_loc image.Point
var best_loc, bot_right image.Point
var best_val float32

func Absolute_Locate_TM(frame *gocv.Mat, template gocv.Mat, meth gocv.TemplateMatchMode, tm_threshold float32, show bool) image.Point {
	// Validate Template Match Mode
	if !(0 <= meth && meth <= 5) {
		//if meth != Methods[0] && meth != Methods[1] && meth != Methods[2] && meth != Methods[3] && meth != Methods[4] && meth != Methods[5] {
		log.Fatal("🧧 Invalid Template Match Mode. Choose from Methods[0-6].")
	}
	// Open Template File
	/*
		var template gocv.Mat = gocv.IMRead(template_Name, gocv.IMReadGrayScale)
		if template.Empty() {
			log.Fatal("Failed to read template")
		}

	*/

	// ROTATE
	//....
	//
	// - Template Match Init -

	mask.SetTo(gocv.Scalar{0, 0, 0, 0})
	result.SetTo(gocv.Scalar{0, 0, 0, 0})
	//result.Reshape(frame.Cols(), frame.Rows())

	//result = gocv.NewMatWithSize(frame.Rows(), frame.Cols(), 0)
	// - Template Matching -
	gocv.MatchTemplate(*frame, template, &result, meth, mask)
	min_val, max_val, min_loc, max_loc = gocv.MinMaxLoc(result)
	// If method is TmSqdiff or TmSqdiffNormed the best matching location is returned as the minimum location
	// Mormed Methods with Threshold Applied. Threshold = 0 it's the equivalent of no Threshold applied.
	// - Interpret TM Results -
	// Normed Methods
	fmt.Println("Meth: ", meth%2)
	if meth%2 == 1 {
		fmt.Println("Entrou if")
		if meth == gocv.TmSqdiffNormed && min_val < (1-tm_threshold) {
			fmt.Println("Min Val: ", min_val)
			best_loc = min_loc
			best_val = min_val
		} else if max_val > tm_threshold {
			fmt.Println("Max Val: ", min_val)
			best_loc = max_loc
			best_val = max_val
		}
	} else {
		// Non-Normed Methods
		if meth == gocv.TmSqdiff {
			best_loc = min_loc
			best_val = min_val
		} else {
			best_loc = max_loc
			best_val = max_val
		}
	}
	// - Filter No Match -
	// When the TM is unable to find a Match wich is under the requirement threshold the coordinates of best match location are return as (0,0)
	// In this case, to prevent the indication of a wrong match at the origin, if there isn't a match, then the last matched coordinates prevail.
	// In order to prevent problems in the navigation control of the robot, the last known Goal Location can´t be used.
	if best_loc == image.Pt(0, 0) {
		best_loc = prevMatch
		LidarLost = true
		fmt.Println("Entrou 1")
		//return image.Point{frame.Cols() / 2, frame.Rows()} // Show that lidar is at this location
	} else {
		LidarLost = false
	}
	//prevMatch = best_loc // FIX DEBUG
	// if best_loc == image.Pt(0, 0) {
	// 	return image.Point{-1, -1}
	// }
	// --------------------
	// Tamplate Matching Result Center
	//var tm_center image.Point = image.Pt(best_loc.X+template.Cols()/2, best_loc.Y+template.Rows()/2) //Not relevant for the aplication
	// Center of the Goal Line
	var goalLineCenter = image.Pt(best_loc.X+template.Cols()/2, best_loc.Y+template.Rows())
	// - SHOW RESULTS -
	bot_right = image.Point{best_loc.X + template.Cols(), best_loc.Y + template.Rows()}
	gocv.Rectangle(frame, image.Rectangle{best_loc, bot_right}, color.RGBA{255, 255, 255, 255}, 1)
	/*
		if show {
			// Show Template Match Matrix Result
			/*
				winRes := gocv.NewWindow("Result")
				winRes.MoveWindow(10, 15)
				winRes.IMShow(result)


			// Show Original Image Highlighing where the Template Matched
			winMatch := gocv.NewWindow("TM - Method " + fmt.Sprint(int(meth)) + " " + fmt.Sprint(meth))
			//winMatch.MoveWindow(300, 15)
			// Place windows separated in the screen
			if int(meth) <= 2 {
				winMatch.MoveWindow(10+int(meth)*frame.Cols()/3, 10)
			} else {
				winMatch.MoveWindow(10+(int(meth)-3)*frame.Cols()/3, 10+frame.Rows()/3)
			}

			gocv.PutText(frame, fmt.Sprint(template.Rows()), image.Point{best_loc.X - template.Cols()/2, best_loc.Y + template.Rows()/2}, gocv.FontHersheySimplex, 0.8, color.RGBA{120, 120, 120, 255}, 1)
			gocv.PutText(frame, fmt.Sprint(template.Cols()), image.Point{best_loc.X + template.Cols()/2, best_loc.Y - template.Rows()/2}, gocv.FontHersheySimplex, 0.8, color.RGBA{120, 120, 120, 255}, 1)
			winMatch.IMShow(*frame)

			// Template Match Method Results
			fmt.Printf("TM_Method: %v\tbest_val: %v\t TM Center: ( %d , %d )", meth, best_val, tm_center.X, tm_center.Y)
			fmt.Printf("\t\tmin_val: %v\tmax_val: %v\n", min_val, max_val)
		}*/

	return goalLineCenter
}

// It is not easy to make a numerical comparison between the different Methods.
// Even With Normalized Methods it would be required to visually observe the accuracy of the methods results
// So, Bes_Method shows the results of every method so it can be chosen based on actual performance
func Show_All_Methods(frame *gocv.Mat, template gocv.Mat, threshold float32) {
	var m int
	thisFrame := gocv.NewMat()
	for m = range Methods {
		frame.CopyTo(&thisFrame)
		//fmt.Println("Trying Method:" + fmt.Sprint(meth))
		Absolute_Locate_TM(&thisFrame, template, gocv.TemplateMatchMode(m), threshold, true)
	}
}
