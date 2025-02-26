import logging
from concurrent.futures import ThreadPoolExecutor

import grpc
import numpy as np
import PySpin
import EasyPySpin
import freenect
import frame_convert
import cv2 as cv
import matplotlib.pyplot as plt
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
import time
import os
import time
import glob
# Load model
model = YOLO("trained_weights/omni400.pt") 
VERSAO="15v"
# Define the coordinates to find the closest point to
target = np.array([240, 240])

# Pre-compute the distance matrix
x, y = np.meshgrid(np.arange(480), np.arange(480))
distances = np.sqrt((x - target[0])**2 + (y - target[1])**2)


def get_kinect_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth(format=freenect.DEPTH_MM)[0])


def get_kinect_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])





def open_frame_source():
    global omnicap
    while 1:
        try:
            omnicap = EasyPySpin.VideoCapture(0)
            omnicap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
            omnicap.set(cv.CAP_PROP_FPS,30)
            return
        except:
            print("Can't Open Omni Camera... Verify Connection")

    #omnicap.cam.SaturationEnable.SetValue(True)
    

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



def main():
	#list_of_files = glob.glob("./Save_Images")
	#latest_file = max(list_of_files, key=os.path.getctime)
	# verify the path using getcwd()
	#print(latest_file)
	path_save_omni = "Images_Saved_Omni"
	num_of_images = len([name for name in os.listdir(path_save_omni) if os.path.isfile(os.path.join(path_save_omni, name))])
	open_frame_source()
	colormap = plt.get_cmap('hsv')
	print("✅️📷️ Record Tool. \n[space] to save image \n[Esc] to exit")
	#actual_frame_omni = np.zeros((480,480,3), dtype=np.uint8)
	cc = cv.VideoWriter_fourcc(*'XVID')
	cc2 = cv.VideoWriter_fourcc(*'XVID')
	file = cv.VideoWriter("output_kinect"+VERSAO+".avi", cc, 30.0, (640, 480))
	file2 = cv.VideoWriter("output_omni"+VERSAO+".avi", cc2, 30.0, (480, 480))
	while(1):
		_, omni_frame = get_omni_frame()
		kinect_frame_d = get_kinect_depth()
		kinect_frame = get_kinect_video()
		heatmap = (colormap(kinect_frame_d) * 255).astype(np.uint8)[:,:,:3] #Ver isto
		file2.write(omni_frame)
		file.write(kinect_frame)
		cv.imshow("Omni RGB", omni_frame)
		cv.imshow("Kinect RGB", kinect_frame)
		cv.imshow("Kinect Depth", heatmap)#(kinect_frame_d).astype("uint8"))
		key=cv.waitKey(20)
		if key==27:    # Esc key to stop
                    break
		elif key==32:	
		    num_of_images+=1
		    path_save_omni = "Images_Saved_Omni/"+VERSAO+str(num_of_images)+".png"
		    path_save_kinect_rgb = "Images_Saved_Kinect/RGB/"+VERSAO+str(num_of_images)+".png"
		    path_save_kinect_depth = "Images_Saved_Kinect/Depth/"+VERSAO+str(num_of_images)+".png"
		    
		    cv.imwrite(path_save_omni, omni_frame)
		    cv.imwrite(path_save_kinect_rgb, kinect_frame)
		    cv.imwrite(path_save_kinect_depth, kinect_frame_d)#/255).astype("uint8"))
		    print("✅️📷️ Images saved in: "+VERSAO+str(num_of_images)+".png")
		if cv.waitKey(1) == ord('q'):
		    break
	file.release()
	file2.release()
	cv.destroyAllWindows()	

main()	    

	
