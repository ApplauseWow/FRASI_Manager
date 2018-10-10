# -*-coding:utf-8-*-

from cv2 import *

device = VideoCapture(0)
while True:
    if device.isOpened():
        print("OK", device.isOpened())
    else:
        print("No", device.isOpened())