import message_pb2
import message_pb2_grpc
import time
import grpc
import os
import cv2
import numpy as np

localIP = "172.16.49.12"
porta = "40000"

ipServer = localIP + ":" + porta
channel = grpc.insecure_channel(ipServer)
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
        match number:
            case -1: IMG.shape = (480, 480, 3)
            case  0: IMG.shape = (480, 480, 3)
            case  1: IMG.shape = (480, 480, 1)
            case  2: IMG.shape = (480, 480, 1)
            case  3: IMG.shape = (480, 640, 3)
            case  4: IMG.shape = (480, 640, 3)
        # if number == 0:
        #     IMG.shape = (480, 480, 3)
        # elif number == 1:
        #     IMG.shape = (480, 480, 1)
        # elif number == 2:
        #     IMG.shape = (480, 480, 1)
        # else:
        #     IMG.shape = (480, 640, 3)
            
        cv2.imshow("IMG", IMG)
        
        
    a = cv2.waitKey(1)
    print(reply.count,"/100 | ", number, " - ", round((time.time()-initialTime)*1000, 2), " FPS: ", round(1/(time.time()-initialTime), 2))
