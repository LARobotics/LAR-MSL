import cv2
import consts
import message_pb2
import message_pb2_grpc
import grpc
import time
import os
import numpy as np
import pygame
import json

cap = cv2.VideoCapture(0)

def handleCameras(Robots):
    #
    for i in range(5):
        try:
            Robots[i].grpcChoice = consts.DefaultWidgets[4][i].getSelected()
            if Robots[i].grpcChoice > -1:
                request = message_pb2.Request_BS(check=consts.DefaultWidgets[4][i].getSelected())
                Robots[i].grpcReply = Robots[i].grpcConnection.Send_to_BS(request, timeout=0.1)
            else:
                Robots[i].grpcReply = 0
        except Exception as e:
            if "StatusCode.DEADLINE_EXCEEDED" not in str(e):
                print(e)
            else:
                print(Robots[i].robotID, "-", "StatusCode.DEADLINE_EXCEEDED")
            
    
    for i in range(5):
        if Robots[i].grpcChoice > -1 and Robots[i].grpcReply != 0:
            frame = np.frombuffer(Robots[i].grpcReply.image, dtype=np.uint8)
            if round(np.sqrt(len(Robots[i].grpcReply.image))) == 480:
                shape = (480, 480, 1)
            elif round(np.sqrt(len(Robots[i].grpcReply.image)/3)) == 480:
                shape = (480, 480, 3)
            elif round(np.sqrt(len(Robots[i].grpcReply.image))) == 160:
                shape = (160, 160, 1)
            elif round(len(Robots[i].grpcReply.image)) < 307202:
                shape = (480, 640, 1)
            else:
                shape = (480, 640, 3)
                
            frame.shape = shape
            # print(np.sqrt(len(Robots[i].grpcReply.image)), np.sqrt(len(Robots[i].grpcReply.image)/3))
            # match Robots[i].grpcChoice:
            #     case  0: frame.shape = (480, 480, 3)
            #     case  1: frame.shape = (480, 480, 1)
            #     case  2: frame.shape = (480, 480, 1)
            #     case  3: frame.shape = (480, 640, 3)
            #     case  4: frame.shape = (480, 640, 3)
            
            if frame.shape[1] == frame.shape[0]:
                finalIMG = cv2.resize(frame, (int(1/5*consts.RESOLUTION[0]), int(1/5*consts.RESOLUTION[0])), interpolation = cv2.INTER_AREA)
            else:
                finalIMG = cv2.resize(frame, (int(1/5*consts.RESOLUTION[0]), int(0.75*1/5*consts.RESOLUTION[0])), interpolation = cv2.INTER_AREA)
            consts.SCREEN.blit(convert_opencv_img_to_pygame(finalIMG), (i/5*consts.RESOLUTION[0], 0.04*consts.RESOLUTION[1] + consts.YOFFSET,))

def get_opencv_img_res(opencv_image):
    height, width = opencv_image.shape[:2]
    return width, height

pygame_surface_cache = {}

    
def convert_opencv_img_to_pygame(opencv_image):
    
    if len(opencv_image.shape) == 2:
        cvt_code = cv2.COLOR_GRAY2RGB
    else:
        cvt_code = cv2.COLOR_BGR2RGB
    rgb_image = cv2.cvtColor(opencv_image, cvt_code).swapaxes(0, 1)

    cache_key = rgb_image.shape
    cached_surface = pygame_surface_cache.get(cache_key)

    if cached_surface is None:
        cached_surface = pygame.surfarray.make_surface(rgb_image)
        pygame_surface_cache[cache_key] = cached_surface
    else:
        pygame.surfarray.blit_array(cached_surface, rgb_image)

    return cached_surface
    
'''

localIP = "172.16.49.12"
porta = "40011"

ipServer = localIP + ":" + porta

with grpc.insecure_channel(ipServer) as channel:
    stub = message_pb2_grpc.Base_SatationStub(channel)
    a = -1
    number = 0
    while a != 27:
        initialTime = time.time()
        if a >= 48 and a <= 58:
            number = a-48
        request = message_pb2.Request_BS(check=number)
        reply = stub.Send_to_BS(request)
        
        if len(reply.image) > 10:
            IMG = np.frombuffer(reply.image, dtype=np.uint8)
            if number <= 2:
                IMG.shape = (480, 480, 3)
            else:
                IMG.shape = (480, 640, 3)
            cv2.imshow("IMG", IMG)
            
        a = cv2.waitKey(1)
        print(reply.count, "/100 | ", number, " - ", round((time.time()-initialTime)*1000, 2), " FPS: ", round(1/(time.time()-initialTime), 2))
'''
# if __name__ == "__main__":
#     porta = "40000"
#     IP = ["172.16.49.11", "172.16.49.12", "172.16.49.13", "172.16.49.14", "172.16.49.15"]
#     IPS = [IP[0] + ":" + porta, IP[1] + ":" + porta, IP[2] + ":" + porta, IP[3] + ":" + porta, IP[4] + ":" + porta]
#     for i in IPS
#     channel = grpc.insecure_channel(ipServer)
#     stub = message_pb2_grpc.Base_SatationStub(channel)
#     a = -1
#     number = 0
    
#     while a != 27:
#         initialTime = time.time()
#         if a >= 48 and a <= 58:
#             number = a-48
#         request = message_pb2.Request_BS(check=number)
#         reply = stub.Send_to_BS(request)
        
#         if len(reply.image) > 10:
#             IMG = np.frombuffer(reply.image, dtype=np.uint8)
#             match number:
#                 case -1: IMG.shape = (480, 480, 3)
#                 case  0: IMG.shape = (480, 480, 3)
#                 case  1: IMG.shape = (480, 480, 1)
#                 case  2: IMG.shape = (480, 480, 1)
#                 case  3: IMG.shape = (480, 640, 3)
#                 case  4: IMG.shape = (480, 640, 3)
#             # if number == 0:
#             #     IMG.shape = (480, 480, 3)
#             # elif number == 1:
#             #     IMG.shape = (480, 480, 1)
#             # elif number == 2:
#             #     IMG.shape = (480, 480, 1)
#             # else:
#             #     IMG.shape = (480, 640, 3)
                
#             cv2.imshow("IMG", IMG)
            
            
#         a = cv2.waitKey(1)
#         print(reply.count,"/100 | ", number, " - ", round((time.time()-initialTime)*1000, 2), " FPS: ", round(1/(time.time()-initialTime), 2))
