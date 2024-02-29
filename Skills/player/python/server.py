import logging
from concurrent.futures import ThreadPoolExecutor

import grpc
import numpy as np
import PySpin
import EasyPySpin
import freenect
import frame_convert
import cv2 as cv
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
import time
from message_pb2 import Response_Omni, Response_Kinect, Object_Omni, Object_Kinect
from message_pb2_grpc import Yolo_OmniServicer, add_Yolo_OmniServicer_to_server, Yolo_KinectServicer, add_Yolo_KinectServicer_to_server
import time

# Load model
model = YOLO("trained_weights/best.pt") 

# Define the coordinates to find the closest point to
target = np.array([240, 240])

# Pre-compute the distance matrix
x, y = np.meshgrid(np.arange(480), np.arange(480))
distances = np.sqrt((x - target[0])**2 + (y - target[1])**2)


def get_kinect_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_kinect_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])


actual_frame = np.zeros((480,480,3), dtype=np.uint8)
def open_frame_source():
    global omnicap
    while 1:
        try:
            omnicap = EasyPySpin.VideoCapture(0)
            omnicap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
            omnicap.set(cv.CAP_PROP_FPS,20)
            print("Omni Camera Opened!")
            return
        except:
            print("Can't Open Omni Camera... Verify Connection")

    #omnicap.cam.SaturationEnable.SetValue(True)
    #omnicap.set(cv.CAP_PROP_FPS,30)

actual_frame_omni = np.zeros((480,480,3), dtype=np.uint8)
def get_omni_frame(frame_bckup=1):
    global actual_frame_omni
    global omnicap
    global model
    global distances
    ret,image_test=omnicap.read()
    if(ret):
        actual_frame_omni = cv.cvtColor(image_test, cv.COLOR_BGR2RGB)
    return 1, actual_frame_omni
def Yolo_Ifer_Omni():
    """Return indices where values more than 2 standard deviations from mean"""
    _, frame = get_omni_frame()
    results = model.predict(source=frame)
    #objects = bytearray( b'')
    objects = []
    
    for index , box in enumerate(results[0].boxes):
        #print(box.cls)
        #print(results[0].masks.segments[index])
        points = results[0].masks.segments[index] * [480,480]
        #print(points)
        # Find the index of the point with the smallest distance
        #closest_index = np.argmin(distances[int(points[:][1]), int(points[:][0])]) ##for point in points])
        if len(points[:,1])>0:
            closest_index = np.argmin(distances[points[:,1].astype(int), points[:,0].astype(int)])
            print("Closest: ",points[closest_index])
            object_atual =Object_Omni()
            object_atual.id = int(box.cls[0])
            object_atual.x =int(points[closest_index][0])
            object_atual.y =int(points[closest_index][1])
            objects.append(object_atual)
            print("Classe: ",box.cls[0])
            #objects.append(points[closest_index][0])
    #cv.imshow("Mask",results[0].masks[0])
    #bytes2= bytes(frame)#np.array([1, 2, 3],dtype="byte"))
    # np.where returns a tuple for each dimension, we want the 1st element
   	
    return frame, objects

def Yolo_Ifer_Kinect():
    """Return indices where values more than 2 standard deviations from mean"""
    image = get_kinect_video()
    depth = get_kinect_depth()
    results = model.predict(source= image)
    
    #cv.imshow("Mask",results[0].masks[0])
   
    # np.where returns a tuple for each dimension, we want the 1st element
    return image, depth

class Yolo_grpcServer_omni(Yolo_OmniServicer):
    def Send_Omni(self, request, context):
         start_time = time.time() # start time of the loop
         #logging.info('detect request size: %d', request.check)
         # Convert metrics to numpy array of values only
         #data = np.fromiter((m.value for m in request.check), dtype='bool')
         img_omni,objects = Yolo_Ifer_Omni()
         #img_kinect, depth_kinect = Yolo_Ifer_Kinect()
         cv.imshow("Python Omni",img_omni)
         #cv.imshow("Python Kinect",img_kinect)
         #cv.imshow("Python Kinect Depth",depth_kinect)
         cv.waitKey(10)
         resp = Response_Omni(omni = bytes(img_omni),objects = objects)#kinect = bytes(img_kinect),kinect_depth=bytes(depth_kinect))
         #print("FPS: ", 1.0 / (time.time() - start_time))
         return resp


if __name__ == '__main__':
    logging.basicConfig(
         level=logging.INFO,
         format='%(asctime)s - %(levelname)s - %(message)s',
	)
    open_frame_source()
    server = grpc.server(ThreadPoolExecutor())
    add_Yolo_OmniServicer_to_server(Yolo_grpcServer_omni(), server)
    port = 9999
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info('server ready on port %r', port)
    server.wait_for_termination()
    

