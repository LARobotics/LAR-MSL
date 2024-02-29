#!/usr/bin/env python
import freenect
import cv2 as cv
import frame_convert


print('Press ESC in window to stop')


def get_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])


while 1:
    cv.imshow('Depth', get_depth())
    cv.imshow('Video', get_video())
    if cv.waitKey(10) == 27:
        break
