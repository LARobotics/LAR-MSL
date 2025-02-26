import logging
from concurrent.futures import ThreadPoolExecutor

import grpc
import numpy as np
import PySpin
import EasyPySpin
import freenect
import frame_convert
import cv2 as cv
print("🔛 👀 Importing YOLO...")
from ultralytics import YOLO
print("✅ 👀 YOLO Imported!")
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
import time
from message_pb2 import Response_Omni, Response_Kinect,Response_to_BS, Object_Omni, Object_Kinect
from message_pb2_grpc import Yolo_OmniServicer, add_Yolo_OmniServicer_to_server, Yolo_KinectServicer, add_Yolo_KinectServicer_to_server, Base_SatationServicer, add_Base_SatationServicer_to_server
import time
import bisect
import sys
import os
# Load model
model = YOLO("trained_weights/best_omni_pav3.pt" )#best_pavilhao.pt") 
model_kinect = YOLO("trained_weights/best_pav2_kinect.pt") 

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
            return
        except:
            print("⚠️ 🎥 Can't Open Omni Camera... Verify Connection")

    #omnicap.cam.SaturationEnable.SetValue(True)
    #omnicap.set(cv.CAP_PROP_FPS,30)
last_frame = np.zeros((480,480,1), dtype=np.uint8)
actual_frame_omni = np.zeros((480,480,1), dtype=np.uint8)
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
    frame_ori = frame.copy()
    results = model.predict(source=frame,conf=0.30, verbose=False)
    #objects = bytearray( b'')
    objects = []
    #hsv=cv.cvtColor(frame, cv.COLOR_BGR2HSV);
    #h,s,v = cv2.split(hsv)
    for index , box in enumerate(results[0].boxes):
        #print(box.cls)
        #print(results[0].masks.segments[index])
        points = results[0].masks.segments[index] * [480,480]
        #print(points)
        # Find the index of the point with the smallest distance
        #closest_index = np.argmin(distances[int(points[:][1]), int(points[:][0])]) ##for point in points])
        if len(points[:,1])>0:
            #int(box.conf[0]*100)>50 #s[int(box.xywh[0][0])][int(box.xywh[0][1])]>50 and
            #if (int(box.cls[0])==0):
            #	print(h[int(box.xywh[0][0])][int(box.xywh[0][1])])#and  40<h[int(box.xywh[0][0])][int(box.xywh[0][1])]<70)
            if( int(box.cls[0])==0  and int(box.conf[0]*100)>50) or  int(box.cls[0])!=0:

            	closest_index = np.argmin(distances[points[:,1].astype(int), points[:,0].astype(int)]).astype(int)
            #print("Closest: ",points[closest_index])
            #print("Closest: ",int(distances[int(points[closest_index][0])][int(points[closest_index][1])]))
            	object_atual =Object_Omni(id=int(box.cls[0]),x=int(points[closest_index][0]),y=int(points[closest_index][1]),dist=int(distances[int(points[closest_index][0])][int(points[closest_index][1])]),conf=int(box.conf[0]*100))
            #fmt.Println(int(box.conf[0]*100)) 
            	text=classes2[int(box.cls[0])]+" "+str(int(box.conf[0]*100))+"%"
            	frame = cv2.putText(frame, text, (int(points[closest_index][0]), int(points[closest_index][1])), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)
            	cv2.circle(frame,(int(points[closest_index][0]), int(points[closest_index][1])), 5, (0,255,0), -1)
            	
            
            #object_atual.id = int(box.cls[0])
            #object_atual.x =int(points[closest_index][0])
            #object_atual.y =int(points[closeclasses = ["Ball", "Person","Goal","Red_Shirt"]st_index][1])
            
            #objects.append(object_atual)
            	bisect.insort(objects, object_atual, key=sort_omni)
            #print("Classe: ",box.cls[0])
            #objects.append(points[closest_index][0])
    #cv.imshow("Mask",results[0].masks[0])

    #bytes2= bytes(frame)#np.array([1, 2, 3],dtype="byte"))int(box.cls[0])
    # np.where returns a tuple for each dimension, we want the 1st element
   	
    actual_frame_omni=frame
    return frame_ori, objects
classes = ["Ball","Blue_Shirt","Goal", "Person","Red_Shirt","Robot"]
kinect_openned = False
print("🔛 📷Opening Kinect...")
while(not kinect_openned):
    try:
        image_kinect = get_kinect_video()
        depth_kinect = get_kinect_depth()
        print("✅ 📷 Kinect opened!")
        #results = model_kinect.predict(source= image_kinect, conf=0.6, verbose=False)
        kinect_openned = True
        
    except:
        print("⚠️ 📷 Kinect disconnected... Verify Power.")
        time.sleep(1)
        kinect_openned = False
    
image_kinect = get_kinect_video()
depth_kinect = get_kinect_depth()
def Yolo_Ifer_Kinect():
    global image_kinect
    global depth_kinect
    global n_robot
    """Return indices where values more than 2 standard deviations from mean"""
    #print("Enter camera")
    image = get_kinect_video()
    depth = get_kinect_depth()
    print(type(depth),depth[0][0])
    
   
    results = model_kinect.predict(source= image, conf=0.6, verbose=False)
    #print("Frame predicted")
    #objects = bytearray( b'')
    objects = []
    
    for index , box in enumerate(results[0].boxes):
        #print(box.cls)
        
        #print(results[0].masks.segments[index])
        points = results[0].masks.segments[index] * [640,480]
        # Find the index of the point with the smallest distance
        #closest_index = np.argmin(distances[int(points[:][1]), int(points[:][0])]) ##for point in points])
        #print("Chegou")
        if len(points[:,1])>0:
            
            
            #print("Chegou3")
          
            
            #objects.append(object_atual)
          
            #if(object_atual.id==0):
            
            cv2.circle(image,(int(box.xywh[0][0]), int(box.xywh[0][1])), 5, (0,255,0), -1)
           
            
            if n_robot==1:
                center_depth_x = int(((box.xywh[0][0]-320)*1.13)+320)
                center_depth_y = int(box.xywh[0][1])+10
            else:
                center_depth_x = int(((box.xywh[0][0]-320)*1.08)+320)
                center_depth_y = int((((box.xywh[0][1]*0.93)-240)*1.15)+240)

            #print("Chegou7")
            object_atual =Object_Kinect(id= int(box.cls[0]),x=int(box.xywh[0][0]),y=int(box.xywh[0][1]),dist=0,conf=int(box.conf[0]*100))
            if(0<center_depth_x<640) and (0<center_depth_y<480):
            	#print("Chegou8",center_depth_x,center_depth_y)
            	
            	#print("Chegou4.6",int(center_depth_x))
            	#print("object: ", object_atual.id,object_atual.x,object_atual.y, object_atual.dist)
            	#print("Chegou4.5")
            	#print("Chegou4",int(box.xywh[0][0]),int(box.xywh[0][1]))
            	dist=depth[int(center_depth_y)][int(center_depth_x)]
            	#print("Chegou9")
            	if dist == 0 :
            	    if (center_depth_y+5<480):
            	        dist=depth[int(center_depth_y)+5][int(center_depth_x)]
            	    if dist == 0:
            	        if (center_depth_y-5>0):
            	    	    dist=depth[int(center_depth_y)-5][int(center_depth_x)]
            	        if dist == 0:
            	    	    if (center_depth_x+5<640):
            	    		    dist=depth[int(center_depth_y)][int(center_depth_x)+5]
            	    	    if dist == 0:
            	    		    if (center_depth_x-5>0):
            	    			    dist=depth[int(center_depth_y)][int(center_depth_x)-5]
            	#print("Chegou5")
            	
            	#print("dist",dist)
            	object_atual.dist=dist
            	bisect.insort(objects, object_atual, key=sort_key)
            	text=classes[int(box.cls[0])]+" D="+str(int(dist))+" "+str(int(box.conf[0]*100))+"%" 
            	image = cv2.putText(image, text, (int(box.xywh[0][0]), int(box.xywh[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            	cv2.circle(depth,(int(center_depth_x), int(center_depth_y)), 5, (1000000,255,0), -1)
            	cv2.circle(depth,(int(box.xywh[0][0]), int(box.xywh[0][1])), 5, (1712,255,0), -1)
    #print("Image")
    image_kinect=image
    depth_kinect=np.uint8(depth>>4)
    #bytes2= bytes(frame)#np.array([1, 2, 3],dtype="byte"))
    # np.where returns a tuple for each dimension, we want the 1st element
    #print("Image")
    return objects
    #cv.imshow("Mask",results[0].masks[0])
   
    # np.where returns a tuple for each dimension, we want the 1st element
    #return image, depth
omniimg_to_send = np.zeros((480,480,1), dtype=np.uint8)
start_time = time.time()
class Yolo_grpcServer_omni(Yolo_OmniServicer):
    def Send_Omni(self, request, context):
         global omniimg_to_send
         global type_image
         global start_time
         #logging.info('detect request size: %d', request.check)
         # Convert metrics to numpy array of values only
         #data = np.fromiter((m.value for m in request.check), dtype='bool')
         img_omni,objects = Yolo_Ifer_Omni()
         
         #print("####END1")
         #img_kinect, depth_kinect = Yolo_Ifer_Kinect()
         #cv.imshow("Python Kinect",img_kinect)
         #cv.imshow("Python Kinect Depth",depth_kinect)
         if(request.check==True):
            omniimg_to_send =np.frombuffer(request.image,dtype=np.uint8)# cv2.resize(np.frombuffer(request.image,dtype=np.uint8), (480,480), interpolation = cv2.INTER_AREA)
            
         #print("####END")
         resp = Response_Omni(omni = bytes(img_omni),img_to_send=type_image,objects = objects)#kinect = bytes(img_kinect),kinect_depth=bytes(depth_kinect))
         print("FPS: ", 1.0 / (time.time() - start_time))
         start_time = time.time() # start time of the loop
         return resp

class Yolo_grpcServer_kinect(Yolo_KinectServicer):
    def Send_Kinect(self, request, context):
         #start_time = time.time() # start time of the loop
         #logging.info('detect request size: %d', request.check)
         # Convert metrics to numpy array of values only
         #data = np.fromiter((m.value for m in request.check), dtype='bool')
         print("KINECT")
         objects = Yolo_Ifer_Kinect()
         #img_kinect, depth_kinect = Yolo_Ifer_Kinect()
      
         #cv.imshow("Python Kinect",img_kinect)
         #cv.imshow("Python Kinect Depth",depth_kinect)

         resp = Response_Kinect(objects = objects)#kinect = bytes(img_kinect),kinect_depth=bytes(depth_kinect))
         
         return resp

count_omni=0
type_image=0
class BS_grpcServer(Yolo_KinectServicer):
    def Send_to_BS(self, request, context):
         global count_omni
         global type_image
         global omniimg_to_send
         #start_time = time.time() # start time of the loop
         #logging.info('detect request size: %d', request.check)
         # Convert metrics to numpy array of values only
         #data = np.fromiter((m.value for m in request.check), dtype='bool')
         #objects = Yolo_Ifer_Kinect()
         #img_kinect, depth_kinect = Yolo_Ifer_Kinect()
      
         #cv.imshow("Python Kinect",img_kinect)
         #cv.imshow("Python Kinect Depth",depth_kinect)
         
         count_omni+=1
         if(count_omni>100):
            count_omni=0
        
         if(request.check==0):
            resp = Response_to_BS(image = bytes(actual_frame_omni),count=count_omni)
         elif(request.check==1):
            type_image=1
            
    
            resp = Response_to_BS(image = bytes(omniimg_to_send),count=count_omni)
         elif(request.check==2):
            type_image=2
            

            
            resp = Response_to_BS(image = bytes(omniimg_to_send),count=count_omni)
         elif(request.check==3):
            resp = Response_to_BS(image = bytes(image_kinect),count=count_omni)
         elif(request.check==4):
            resp = Response_to_BS(image = bytes(np.uint8(depth_kinect)),count=count_omni)

         #kinect = bytes(img_kinect),kinect_depth=bytes(depth_kinect))
         #print("FPS: ", 1.0 / (time.time() - start_time))
         return resp

if __name__ == '__main__':
    global n_robot
    print("🔛🎥Opening OmniCamera...")
    open_frame_source()
    print("✅🎥OmniCamera opened!")
    print("🔛🔗️ Opening gRPC Server...")
    server = grpc.server(ThreadPoolExecutor())
    add_Yolo_OmniServicer_to_server(Yolo_grpcServer_omni(), server)
    print("➡️ 🎥Omni Added")
    add_Yolo_KinectServicer_to_server(Yolo_grpcServer_kinect(), server)
    print("➡️ 📷Kinect Added")
    add_Base_SatationServicer_to_server(BS_grpcServer(),server)
    print("➡️ 🚉BS Added")
    n_robot = int(sys.argv[1])
    ip_grpc = sys.argv[2]
    port = 40000
    server.add_insecure_port(f'{ip_grpc}:{port}')
    server.start()
    print(f'✅🔗️ gRPC Server ready on IP {ip_grpc}:{port}')
    #while(1):
        #cv.imshow("Omni",actual_frame_omni)
        #cv.imshow("Kinect",image_kinect)
        #cv.imshow("Kinect Depth",depth_kinect)
        #cv.waitKey(20)
    server.wait_for_termination()
    

