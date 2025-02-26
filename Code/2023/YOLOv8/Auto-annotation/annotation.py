#from ultralytics.vit import SAM
#mport os
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:3072"
import torch
import ultralytics
from ultralytics import YOLO
print(ultralytics.__version__)
from ultralytics.yolo.data.annotator import auto_annotate
#model =SAM ('best_2xposOPEN_kinect.pt')
auto_annotate(data="ToDO",det_model="best_pav2_kinect.pt",sam_model="sam_b.pt",output_dir="ToDO")

