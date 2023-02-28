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



uint16_t get_byte_16(void *buf, int offset)
{
	return *((uint16_t *)buf + offset);
}
void depth_cb(freenect_device* dev, void* data, uint32_t timestamp)
{
	//printf("Received depth frame at %d\n", timestamp);
	pthread_mutex_lock(&m_depth_mutex);

 	m_buffer_depth = (uint8_t*)data;
	pthread_mutex_unlock(&m_depth_mutex);
 	m_new_depth_frame = true;
}

void video_cb(freenect_device* dev, void* data, uint32_t timestamp)
{
	pthread_mutex_lock(&m_rgb_mutex);
	//printf("Received video frame at %d\n", timestamp);

 	m_buffer_rgb = (uint8_t*)data;
	pthread_mutex_unlock(&m_rgb_mutex);
 	m_new_rgb_frame = true;
}

*/
import "C"
import (
	"fmt"
	"runtime"
	"unsafe"

	"gocv.io/x/gocv"
)

// //uint8_t* rgb = (uint8_t*)data;
var img gocv.Mat
var depth_img []byte

type Kinect struct {
	Ctx *C.freenect_context
	Dev *C.freenect_device
}

func (d *Kinect) InitKinectContext() {
	fmt.Printf("freenect_init() \n")
	if C.freenect_init(&d.Ctx, C.NULL) < 0 {
		fmt.Printf("freenect_init() failed\n")

	}

	C.freenect_set_log_level(d.Ctx, C.FREENECT_LOG_DEBUG)
	C.freenect_select_subdevices(d.Ctx, C.FREENECT_DEVICE_MOTOR|C.FREENECT_DEVICE_CAMERA) //C.FREENECT_DEVICE_MOTOR|
	fmt.Printf("InitKinectContext\n")

}

func (d *Kinect) InitKinectDevice() {
	for nr_devices := C.freenect_num_devices(d.Ctx); nr_devices <= 0; {
		fmt.Printf("Number of devices found: %d\n", nr_devices)

	}

	if C.freenect_open_device(d.Ctx, &d.Dev, 0) < 0 {
		fmt.Printf("Could not open device\n")
		C.freenect_shutdown(d.Ctx)

	}
	//d.SetAutoExposureOFF()
	fmt.Printf("Device Opened\n")

	C.freenect_set_led(d.Dev, C.LED_RED)
}

func (d *Kinect) SetAutoExposureOFF() {
	C.freenect_set_flag(d.Dev, C.FREENECT_AUTO_EXPOSURE, C.FREENECT_OFF)
}

func (d *Kinect) SetYellowLedKinect() {
	errCode := C.freenect_set_led(d.Dev, C.LED_YELLOW)

	if errCode == 0 {
		fmt.Printf("Led changed")
	}
}
func (d *Kinect) SetRedLedKinect() {
	errCode := C.freenect_set_led(d.Dev, C.LED_RED)

	if errCode == 0 {
		fmt.Printf("Led changed")
	}
}

func (d *Kinect) Pixel_distance(cx int, cy int) uint16 {
	depth_array := d.GetDepthArray()
	if depth_array != nil {
		sourcePos := C.int(cy*640 + cx)
		return uint16(C.get_byte_16(depth_array, sourcePos))

	}
	return 0
}

func (d *Kinect) StartCallbacks() {
	fmt.Printf("initBuffers...................................................................................")
	C.freenect_set_video_mode(d.Dev, C.freenect_find_video_mode(C.FREENECT_RESOLUTION_MEDIUM, C.FREENECT_VIDEO_RGB))
	C.freenect_set_depth_mode(d.Dev, C.freenect_find_depth_mode(C.FREENECT_RESOLUTION_MEDIUM, C.FREENECT_DEPTH_REGISTERED))

	C.freenect_set_video_callback(d.Dev, (*[0]byte)(C.video_cb))

	C.freenect_set_depth_callback(d.Dev, (*[0]byte)(C.depth_cb))
	//C.freenect_set_video_buffer(d.Dev, unsafe.Pointer(C.rgb_back))

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
	//time.Sleep(1 * time.Second)
	C.freenect_set_led(d.Dev, C.LED_GREEN)

}

func (d *Kinect) ProcessEvents() {
	for {
		fmt.Println("\n\nfreenect\n\n", C.freenect_process_events(d.Ctx))

		//C.freenect_process_events(d.Ctx)
	}
}
func PrintMemUsage() {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	// For info on each, see: https://golang.org/pkg/runtime/#MemStats
	fmt.Printf("Alloc = %v MiB", bToMb(m.Alloc))
	fmt.Printf("\tTotalAlloc = %v MiB", bToMb(m.TotalAlloc))
	fmt.Printf("\tHeapAlloc = %v MiB", bToMb(m.HeapAlloc))
	fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

func bToMb(b uint64) uint64 {
	return b / 1024 / 1024
}

func (d *Kinect) GetRGBMat() gocv.Mat {

	C.freenect_process_events(d.Ctx)

	//defer img.Close()
	if C.m_new_rgb_frame {
		C.m_new_rgb_frame = false

		//C.freenect_update_tilt_state(d.Dev)
		//_ = C.freenect_get_tilt_state(d.Dev)
		//C.freenect_get_mks_accel(state, &dx, &dy, &dz)

		C.pthread_mutex_lock(&C.m_rgb_mutex)
		C.rgb_buffer = C.m_buffer_rgb
		C.pthread_mutex_unlock(&C.m_rgb_mutex)

		//attributes := C.freenect_get_current_video_mode(d.Dev)
		//C.freenect_set_video_buffer(d.Dev, unsafe.Pointer(C.rgb_back))
		//img_bytes := C.GoBytes(unsafe.Pointer(rgb_buffer), 640*480*3) //C.int(attributes.bytes)
		img, _ = gocv.NewMatFromBytes(480, 640, gocv.MatTypeCV8UC3, C.GoBytes(unsafe.Pointer(C.rgb_buffer), C.int(640*480*3)))

		//img = esta
		gocv.CvtColor(img, &img, gocv.ColorBGRAToBGR)

		gocv.CvtColor(img, &img, gocv.ColorBGRToRGB)
		//esta.Close()

		return img
	}
	return img

}

func (d *Kinect) GetDepthArray() unsafe.Pointer {

	//C.freenect_process_events(d.Ctx)
	//C.freenect_process_events(d.Ctx)
	//defer img.Close()
	if C.m_new_depth_frame {
		C.m_new_depth_frame = false

		//C.freenect_update_tilt_state(d.Dev)
		//_ = C.freenect_get_tilt_state(d.Dev)
		//C.freenect_get_mks_accel(state, &dx, &dy, &dz)
		//fmt.Println("dentro..................")
		C.pthread_mutex_lock(&C.m_depth_mutex)
		C.depth_data = C.m_buffer_depth
		C.pthread_mutex_unlock(&C.m_depth_mutex)

		//depth_img = C.GoBytes(unsafe.Pointer(C.depth_data), 640*480*3)
		return unsafe.Pointer(C.depth_data)
	}
	//fmt.Println("fora..................")

	return unsafe.Pointer(C.depth_data)

}
