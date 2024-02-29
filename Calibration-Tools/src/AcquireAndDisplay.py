# coding=utf-8
# =============================================================================
# Copyright (c) 2001-2021 FLIR Systems, Inc. All Rights Reserved.
#
# This software is the confidential and proprietary information of FLIR
# Integrated Imaging Solutions, Inc. ("Confidential Information"). You
# shall not disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with FLIR Integrated Imaging Solutions, Inc. (FLIR).
#
# FLIR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
# SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT. FLIR SHALL NOT BE LIABLE FOR ANY DAMAGES
# SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
# THIS SOFTWARE OR ITS DERIVATIVES.
# =============================================================================
#
# This AcquireAndDisplay.py shows how to get the image data, and then display images in a GUI.
# This example relies on information provided in the ImageChannelStatistics.py example.
#
# This example demonstrates how to display images represented as numpy arrays.
# Currently, this program is limited to single camera use.
# NOTE: keyboard and matplotlib must be installed on Python interpreter prior to running this example.

import os
import EasyPySpin
import PySpin
import matplotlib.pyplot as plt
import sys
import keyboard
import time
import cv2 as cv
cap = EasyPySpin.VideoCapture(0)
cap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
cap.set(cv.CAP_PROP_FPS,20)
print(type(cap.cam.Camera_SaturationEnable_get()))
cap.cam.SaturationEnable.SetValue(PySpin.On)


cap.cam.Saturation.SetValue(200.0)
while(1):
    ret, frame = cap.read()
    dst = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    cap.cam.Gain.SetValue(float(5))
    cap.cam.Saturation.SetValue(200.0)
    cap.cam.ExposureTime.SetValue(7810.0)
    print("Sat:",cap.cam.Saturation.GetValue())
    print("Gain:",cap.cam.Gain.GetValue())
    print("Expo:",cap.cam.ExposureTime.GetValue())
    
    print(frame.shape[0])
    print(frame[479][479])
    cv.imshow("frame.png", dst)
    cv.waitKey(20)

cap.release()