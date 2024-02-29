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
import os
import time
import glob
import matplotlib.pyplot as plt
# Load model


def get_kinect_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_kinect_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])





def open_frame_source():
    global omnicap
    while 1:
        try:
            omnicap = EasyPySpin.VideoCapture(0)
            omnicap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
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
VERSAO = "1."
def main():
	colormap = plt.get_cmap('hsv')
	n_files = 0
	path_save_kinect_depth = "Images_Saved_Kinect/Depth/"
	num_of_images = len([name for name in os.listdir(path_save_kinect_depth) if os.path.isfile(os.path.join(path_save_kinect_depth, name))])
	try:
		img =cv.imread("Images_Saved_Kinect/Depth/"+VERSAO+"1.png",cv.IMREAD_UNCHANGED)
		heatmap = (colormap(img) * 255).astype(np.uint8)[:,:,:3] #Ver isto
	except:
		print("❌️ File don't exist.")
		return
	while(num_of_images>n_files):
		n_files += 1
		path_save_kinect_depth = "Images_Saved_Kinect/Depth/"+VERSAO+str(n_files)+".png"
		path_converted_kinect_depth = "Images_Saved_Kinect/Depth/Converted/"+VERSAO+str(n_files)+".png"
		img =cv.imread(path_save_kinect_depth,cv.IMREAD_UNCHANGED)
		heatmap = (colormap(img) * 255).astype(np.uint8)[:,:,:3] #Ver isto
		cv.imwrite(path_converted_kinect_depth, heatmap)
	print("✅️ Success!")
		
main()	    
	
	
