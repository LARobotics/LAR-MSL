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
import bisect

# Load model
model = YOLO("trained_weights/best_RC.pt") 
model_kinect = YOLO("trained_weights/best_Carolina.pt") 

# Define the coordinates to find the closest point to
target = np.array([240, 240])

# Pre-compute the distance matrix
x, y = np.meshgrid(np.arange(480), np.arange(480))
distances = np.sqrt((x - target[0])**2 + (y - target[1])**2)


def get_kinect_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth(format=freenect.DEPTH_MM)[0]) #


def get_kinect_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

def sort_key(item):
    return -item.y
def sort_omni(item):
    return item.dist
actual_frame = np.zeros((480,480,3), dtype=np.uint8)
def open_frame_source():
    global omnicap
    while 1:
        try:
            omnicap = EasyPySpin.VideoCapture(0)
            omnicap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
            omnicap.set(cv.CAP_PROP_FPS,30)
            print("Omni Camera Opened!")
            return
        except:
            print("Can't Open Omni Camera... Verify Connection")

    #omnicap.cam.SaturationEnable.SetValue(True)
    #omnicap.set(cv.CAP_PROP_FPS,30)

actual_frame_omni = np.zeros((480,480,3), dtype=np.uint8)
def get_omni_frame(frame_bckup=1):
    global omnicap
    global model
    global distances
    global last_frame
    ret,image_test=omnicap.read()
    if(ret):
        frame_omni = cv.cvtColor(image_test, cv.COLOR_BGR2RGB)
        last_frame = frame_omni
    else:
    	frame_omni= last_frame
    return 1, frame_omni
classes2 = ["Ball","Blue_Shirt","Goal", "Person","Red_Shirt","Robot"]
def Yolo_Ifer_Omni():
    global actual_frame_omni
    """Return indices where values more than 2 standard deviations from mean"""
    _, frame = get_omni_frame()
    
    results = model.predict(source=frame,conf=0.30)
    #objects = bytearray( b'')
    objects = []
    frame_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for index , box in enumerate(results[0].boxes):
        #print(box.cls)
        #print(results[0].masks.segments[index])
        points = results[0].masks.segments[index] * [480,480]
        #print(points)
        # Find the index of the point with the smallest distance
        #closest_index = np.argmin(distances[int(points[:][1]), int(points[:][0])]) ##for point in points])
        
        if len(points[:,1])>0:
            closest_index = np.argmin(distances[points[:,1].astype(int), points[:,0].astype(int)]).astype(int)
            if (frame_hsv[int(box.xywh[0][1])][int(box.xywh[0][0])][1]>83 and int(box.cls[0])==0) or int(box.cls[0])!=0:
               cv2.polylines(frame,np.int32([points]),True,(0,0,255),2)
               
               print("Closest: ",points[closest_index])
               print("Closest: ",int(distances[int(points[closest_index][0])][int(points[closest_index][1])]))
               object_atual =Object_Omni(id=int(box.cls[0]),x=int(points[closest_index][0]),y=int(points[closest_index][1]),dist=int(distances[int(points[closest_index][0])][int(points[closest_index][1])]))
               text=classes2[int(box.cls[0])]+" "+str(int(box.conf[0]*100))+"%"
               frame = cv2.putText(frame, text, (int(points[closest_index][0]), int(points[closest_index][1])), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)
               cv2.circle(frame,(int(box.xywh[0][0]), int(box.xywh[0][1])), 5, (0,0,255), -1)
               cv2.circle(frame,(int(points[closest_index][0]), int(points[closest_index][1])), 5, (0,255,0), -1)
            
               #object_atual.id = int(box.cls[0])
               #object_atual.x =int(points[closest_index][0])
               #object_atual.y =int(points[closeclasses = ["Ball", "Person","Goal","Red_Shirt"]st_index][1])
               
               #objects.append(object_atual)
               bisect.insort(objects, object_atual, key=sort_omni)
               print("Classe: ",box.cls[0])
               #objects.append(points[closest_index][0])
    #cv.imshow("Mask",results[0].masks[0])

    #bytes2= bytes(frame)#np.array([1, 2, 3],dtype="byte"))int(box.cls[0])
    # np.where returns a tuple for each dimension, we want the 1st element
   
    actual_frame_omni=frame
    return frame, objects
classes = ["Ball","Blue_Shirt","Goal", "Person","Red_Shirt","Robot"]
image_kinect = get_kinect_video()
depth_kinect = get_kinect_depth()
def Yolo_Ifer_Kinect():
    global image_kinect
    global depth_kinect
    """Return indices where values more than 2 standard deviations from mean"""
    #print("Enter camera")
    image = get_kinect_video()
    depth = get_kinect_depth()
    print("Frame geted",len(depth))
   
    results = model_kinect.predict(source= image, conf=0.6)
    #print("Frame predicted")
    #objects = bytearray( b'')
    objects = []
    MAX_VALUE=9000
    
    for index , box in enumerate(results[0].boxes):
        #print(box.cls)
        #print(results[0].masks.segments[index])
        points = results[0].masks.segments[index] * [640,480]
        #print(points)
        # Find the index of the point with the smallest distance
        #closest_index = np.argmin(distances[int(points[:][1]), int(points[:][0])]) ##for point in points])
        if len(points[:,1])>0:
            #closest_index = np.argmin(distances[points[:,1].astype(int), points[:,0].astype(int)])
            # compute the center of the contour
           
            #print("################################################################Classe:",box.cls[0],"X:",box.xywh[0][0],"Y:",box.xywh[0][1],"W:",box.xywh[0][2],"H:",box.xywh[0][3])
            #print("Closest: ",points[closest_index])
            object_atual =Object_Kinect(id= int(box.cls[0]),x=int(box.xywh[0][0]),y=int(box.xywh[0][1]),dist=depth[int(box.xywh[0][1])][int(box.xywh[0][0])])
            #object_atual.id =
            #object_atual.x =inc_x=int(box.xywh[0][0])
            #object_atual.y =inc_y=int(box.xywh[0][1])
            #object_atual.dist =depth[int(box.xywh[0][1])][int(box.xywh[0][0])]
            
          
            
            #objects.append(object_atual)
            bisect.insort(objects, object_atual, key=sort_key)
            #if(object_atual.id==0):
            text=classes[int(box.cls[0])]+" "+str(int(box.conf[0]*100))+"% D=" +str(depth[int(box.xywh[0][1])][int(box.xywh[0][0])])
            image = cv2.putText(image, text, (int(box.xywh[0][0]), int(box.xywh[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.circle(image,(int(box.xywh[0][0]), int(box.xywh[0][1])), 5, (0,255,0), -1)
            center_depth_x = int(((box.xywh[0][0]-320)*1.08)+320)
            center_depth_y = int((((box.xywh[0][1]*0.93)-240)*1.15)+240)
            object_atual.dist=depth[center_depth_y][center_depth_x]
            cv2.circle(depth,(int(center_depth_x), int(center_depth_y)), 5, (1000000,255,0), -1)
            cv2.circle(depth,(int(box.xywh[0][0]), int(box.xywh[0][1])), 5, (1712,255,0), -1)   
            print("object: ", object_atual.id,object_atual.x,object_atual.y, object_atual.dist) 
            #cv2.circle(image,(int(cX), int(cY)), 5, (0,255,0), -1)
           
            #AVOID NOISE
            '''while depth[inc_x][inc_y] > MAX_VALUE:
                inc_x+=1
                object_actual[inc_x][inc_y] 
                objects.append(object_atual)
            '''
            #print("Classe: ",box.cls[0])
            #objects.append(points[closest_index][0])
    #cv.imshow("Mask",image)
    #cv.imshow("Mask2",np.uint8(depth>>4))
    image_kinect=image
    depth_kinect=np.uint8(depth>>4)
    #bytes2= bytes(frame)#np.array([1, 2, 3],dtype="byte"))
    # np.where returns a tuple for each dimension, we want the 1st element
    
    return objects
    #cv.imshow("Mask",results[0].masks[0])
   
    # np.where returns a tuple for each dimension, we want the 1st element
    #return image, depth

class Yolo_grpcServer_omni(Yolo_OmniServicer):
    def Send_Omni(self, request, context):
         start_time = time.time() # start time of the loop
         #logging.info('detect request size: %d', request.check)
         # Convert metrics to numpy array of values only
         #data = np.fromiter((m.value for m in request.check), dtype='bool')
         img_omni,objects = Yolo_Ifer_Omni()
         
         #print("####END1")
         #img_kinect, depth_kinect = Yolo_Ifer_Kinect()
         #cv.imshow("Python Kinect",img_kinect)
         #cv.imshow("Python Kinect Depth",depth_kinect)
         
         #print("####END")
         resp = Response_Omni(omni = bytes(img_omni),objects = objects)#kinect = bytes(img_kinect),kinect_depth=bytes(depth_kinect))
         #print("FPS: ", 1.0 / (time.time() - start_time))
         return resp

class Yolo_grpcServer_kinect(Yolo_KinectServicer):
    def Send_Kinect(self, request, context):
         #start_time = time.time() # start time of the loop
         #logging.info('detect request size: %d', request.check)
         # Convert metrics to numpy array of values only
         #data = np.fromiter((m.value for m in request.check), dtype='bool')
         objects = Yolo_Ifer_Kinect()
         #img_kinect, depth_kinect = Yolo_Ifer_Kinect()
      
         #cv.imshow("Python Kinect",img_kinect)
         #cv.imshow("Python Kinect Depth",depth_kinect)

         resp = Response_Kinect(objects = objects)#kinect = bytes(img_kinect),kinect_depth=bytes(depth_kinect))
         #print("FPS: ", 1.0 / (time.time() - start_time))
         return resp


if __name__ == '__main__':
    logging.basicConfig(
         level=logging.INFO,
         format='%(asctime)s - %(levelname)s - %(message)s',
	)
    open_frame_source()
    while(1):
         objects = Yolo_Ifer_Omni()
         #objects = Yolo_Ifer_Kinect()
         cv.imshow("Omni",actual_frame_omni)
         #cv.imshow("Kinect",image_kinect)
         #cv.imshow("Kinect Depth",depth_kinect)
         cv.waitKey(20)
   
    

Mask2
