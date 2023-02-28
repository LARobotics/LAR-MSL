from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
import time
# Load model
model = YOLO("trained_weights/omni400.pt") 
# OpenCV source
im1 = cv2.imread("datasets/MSL-Omnidirecional-LAR-UMinho-1/test/images/data_omni52_png.rf.9e689873f3167e78d55f1d2d0de36787.jpg")
while(1):
	results = model.predict(source=im1)
	# your code...



