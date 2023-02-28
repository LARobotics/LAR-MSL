import os
HOME = os.getcwd()
print(HOME)


from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

from ultralytics import YOLO

from IPython.display import display, Image

from roboflow import Roboflow
rf = Roboflow(api_key="[YOUR-KEY]")
project = rf.workspace("[YOUR-WORKSPACE]").project("[YOUR-PROJECT]")
dataset = project.version(1).download("yolov8")

import torch
torch.cuda.empty_cache()
model = YOLO("yolov8s-seg.pt")
model.train(model="yolov8s-seg.pt",task="segment",data="/home/martins/Desktop/Redes/datasets/MSL-Omnidirecional-LAR-UMinho-1/data.yaml", epochs=5,imgsz=480,plots=True)


# On console: yolo task=segment mode=train model=yolov8s-seg.pt data=/content/datasets/MSL-Omnidirecional-LAR-UMinho-1/data.yaml epochs=200 imgsz=480 plots=True
