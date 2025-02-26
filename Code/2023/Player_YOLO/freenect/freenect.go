package freenect

/*
#cgo CPPFLAGS: -std=c++11 -O3 -Wall -w -I/usr/include/opencv4
#cgo LDFLAGS: -lfreenect -lfreenect_sync -lopencv_core -lopencv_imgproc -lopencv_highgui -lpthread
#cgo CFLAGS: -I/home/rui/Desktop/Tese/test -I/usr/local/include/libfreenect
#include <libfreenect.h>
#include <libfreenect_sync.h>
//#include </home/rui/Desktop/Tese/test/freenect.h>
#include <stdbool.h>
#include <pthread.h>
#include <assert.h>
bool m_new_rgb_frame;
bool m_new_depth_frame;
uint8_t *m_buffer_depth;
uint8_t *depth_data;
uint8_t *m_buffer_rgb;
uint8_t *rgb_back;// = (uint8_t*)malloc(640*480*3);
uint8_t * rgb_buffer;
pthread_mutex_t m_rgb_mutex;
pthread_mutex_t m_depth_mutex;
//depth frame callback
void depth_cb(freenect_device* dev, void* data, uint32_t timestamp)
{
	//printf("Received depth frame at %d\n", timestamp);
	pthread_mutex_lock(&m_depth_mutex);
 	m_buffer_depth = (uint8_t*)data;
	pthread_mutex_unlock(&m_depth_mutex);
 	m_new_depth_frame = true;
}
//rgb frame callback
void video_cb(freenect_device* dev, void* data, uint32_t timestamp)
{
	pthread_mutex_lock(&m_rgb_mutex);
 	m_buffer_rgb = (uint8_t*)data;
	pthread_mutex_unlock(&m_rgb_mutex);
 	m_new_rgb_frame = true;
}
*/
import "C"
import (
	"fmt"

	"gocv.io/x/gocv"

	"unsafe"
)

var img gocv.Mat
var depth_img []byte

type Kinect struct {
	Ctx *C.freenect_context
	Dev *C.freenect_device
}

// InitKinectContext initializes the kinect contex.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) InitKinectContext() {
	if C.freenect_init(&d.Ctx, C.NULL) < 0 {
		fmt.Printf("freenect_init failed\n")

	}

	C.freenect_set_log_level(d.Ctx, C.FREENECT_LOG_DEBUG)
	C.freenect_select_subdevices(d.Ctx, C.FREENECT_DEVICE_CAMERA) //C.FREENECT_DEVICE_MOTOR|
	fmt.Printf("InitKinectContext\n")
}

// InitKinectDevice initializes the kinect usb device.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) InitKinectDevice() {
	//check if there is a device available
	/*for nr_devices := C.freenect_num_devices(d.Ctx); nr_devices == 0; {
		fmt.Printf("Number of devices found: %d\n", nr_devices)
		time.Sleep(10 * time.Millisecond)
		//return
	}*/
	/*nr_devices := C.freenect_num_devices(d.Ctx)
	fmt.Printf("Number of devices found: %d\n", nr_devices)
	//open the device kinect if there is one
	for C.freenect_open_device(d.Ctx, &d.Dev, 0) < 0 {
		fmt.Printf("Could not open device\n")
		time.Sleep(100 * time.Millisecond)
		//C.freenect_shutdown(d.Ctx)

	}

	//changes the color LED from the kinect to red indicating a sucessful initialization
	d.SetRedLedKinect()*/

	fmt.Printf("InitKinectDevice\n")
	nr_devices := C.freenect_num_devices(d.Ctx)
	for nr_devices = C.freenect_num_devices(d.Ctx); nr_devices == 0; {
		fmt.Printf("Number of devices found: %d\n", nr_devices)

	}
	fmt.Printf("Number of devices found: %d\n", nr_devices)
	if C.freenect_open_device(d.Ctx, &d.Dev, 0) < 0 {
		fmt.Printf("Could not open device\n")
		C.freenect_shutdown(d.Ctx)

	}
	fmt.Printf("Device Opened\n")
	C.freenect_set_led(d.Dev, C.LED_RED)

}

// SetAutoExposureOFF disable the autoexposure flag.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) SetAutoExposureOFF() {

	C.freenect_set_flag(d.Dev, C.FREENECT_AUTO_EXPOSURE, C.FREENECT_OFF)
}

// SetYellowLedKinect sets the led yellow color.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) SetYellowLedKinect() {
	errCode := C.freenect_set_led(d.Dev, C.LED_YELLOW)

	if errCode == 0 {
		fmt.Printf("Led changed")
	}
}

// SetRedLedKinect sets the led red color.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) SetRedLedKinect() {
	errCode := C.freenect_set_led(d.Dev, C.LED_RED)

	if errCode == 0 {
		fmt.Printf("Led changed")
	}
}

// SetGreenLedKinect sets the led green color.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) SetGreenLedKinect() {
	errCode := C.freenect_set_led(d.Dev, C.LED_GREEN)

	if errCode == 0 {
		fmt.Printf("Led changed")
	}
}

// StartCallbacks sets the video and depth formats to read.
// Initializes the threads for receiving the rgb and dept frames
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
func (d *Kinect) StartCallbacks() {
	C.freenect_set_video_mode(d.Dev, C.freenect_find_video_mode(C.FREENECT_RESOLUTION_MEDIUM, C.FREENECT_VIDEO_RGB))
	C.freenect_set_depth_mode(d.Dev, C.freenect_find_depth_mode(C.FREENECT_RESOLUTION_MEDIUM, C.FREENECT_DEPTH_REGISTERED))

	C.freenect_set_video_callback(d.Dev, (*[0]byte)(C.video_cb))

	C.freenect_set_depth_callback(d.Dev, (*[0]byte)(C.depth_cb))

	//start video first for don't get [stream...] errors
	ret := C.freenect_start_video(d.Dev)
	if ret < 0 {
		C.freenect_shutdown(d.Ctx)
		return
	}
	ret = C.freenect_start_depth(d.Dev)
	if ret < 0 {
		C.freenect_shutdown(d.Ctx)
		return
	}
	fmt.Printf("\n\nLed changed\n\n\n")
	d.SetGreenLedKinect()

}

// GetRGBMat returns a matrix on the rgb format from the received array.
// It copies the thread array to another and converts from array to matrix.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
//
// Returns:
//
//	-gocv.Mat -> matrix with pixels information on RGB format
func (d *Kinect) GetRGBMat() gocv.Mat {

	C.freenect_process_events(d.Ctx)

	if C.m_new_rgb_frame {
		C.m_new_rgb_frame = false

		C.pthread_mutex_lock(&C.m_rgb_mutex)
		C.rgb_buffer = C.m_buffer_rgb
		C.pthread_mutex_unlock(&C.m_rgb_mutex)

		img, _ = gocv.NewMatFromBytes(480, 640, gocv.MatTypeCV8UC3, C.GoBytes(unsafe.Pointer(C.rgb_buffer), C.int(640*480*3)))

		gocv.CvtColor(img, &img, gocv.ColorBGRAToBGR)

		gocv.CvtColor(img, &img, gocv.ColorBGRToRGB)

		return img
	}
	return img

}

// GetDepthArray returns an array with the distances measured by the kinect.
// It copies the thread array to another.
//
// Parameters:
//
//   - d * : Kinect -> pointer to struct previously defined
//
// Returns:
//
//	-unsafe.Pointer -> matrix with depth frame distances per 4 rgb pixels
func (d *Kinect) GetDepthArray() unsafe.Pointer {

	if C.m_new_depth_frame {
		C.m_new_depth_frame = false

		C.pthread_mutex_lock(&C.m_depth_mutex)
		C.depth_data = C.m_buffer_depth
		C.pthread_mutex_unlock(&C.m_depth_mutex)

		return unsafe.Pointer(C.depth_data)
	}

	return unsafe.Pointer(C.depth_data)

}
