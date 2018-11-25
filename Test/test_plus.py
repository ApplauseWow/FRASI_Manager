# -*-coding:utf-8-*-

# camera test
# from cv2 import *
#
# device = VideoCapture(0)
# while True:
#     if device.isOpened():
#         print("OK", device.isOpened())
#     else:
#         print("No", device.isOpened())

# socket test
# import socket
#
#
# obj = socket.socket()
#
# obj.connect(("127.0.0.1",8080))
#
# ret_bytes = obj.recv(1024)
# ret_str = str(ret_bytes)
# print ret_str
#
# while True:
#     inp = input("what are u talking about\n >>>")
#     if inp == "q":
#         obj.sendall(bytes(inp))
#         break
#     elif inp == "1":
#         obj.sendall(bytes("recognition"))
#     elif inp == "2":
#         obj.sendall(bytes("sign_in"))
#     else:
#         obj.sendall(bytes(inp))
#         ret_bytes = obj.recv(1024)
#         ret_str = str(ret_bytes)
#         print ret_str

# import threading
# import time
#
# class Test(object):
#
#     @staticmethod
#     def test():
#         threading.Thread(target=Test.thread_test).start()
#         for i in range(20):
#             time.sleep(0.5)
#             print i
#
#     @staticmethod
#     def thread_test():
#         print("sleep...")
#         time.sleep(5)
#         print("wake up")
#
#
# if __name__ == '__main__':
#     print("main thread ...")
#     threading.Thread(target=Test.test).start()

# import os
#
# p = os.path.abspath(".")
# print p
# p=os.getcwd()
# print p
# for root, dirs, files in os.walk(p):
#     print root
#     print dirs
#     print files

# test: flip the frame cv.flip or run on the GPU
import torch
import cv2
import time
# import tensorflow as tf

# if torch.cuda.is_available():
# # with tf.device("/gpu:0"):
#     img = cv2.imread("1.jpg")
#     print type(img)
#     # _img = torch.from_numpy(img)
#     # _img.cuda()
#     start = time.time()
#     width = img.shape[1]
#     for i in range(width):
#         img[:, [i, width - 1 - i]] = img[:, [width - 1 - i, i]]
#         if (width - 1 - i - i) <= 2:
#             break
#
#     # f_img = cv2.flip(img, 1)
#     end = time.time()
#     print end - start
#     cv2.imwrite("2.jpg", img)

# 1 - torch 调用gpu 翻转 15% gpu 0.18-0.22s  稳定0.182-0.199
# 2 - 直接翻转 0.0051-0.0059s 未使用gpu？？？ **最快**
# 3 - cv2.flip() 0.065-0.068s  未使用gpu

# 使用框架调用Gpu会抢夺dlib的GPU资源使其无法使用cuda加速直接终端程序

from PyQt5 import QtWidgets
import sys
from  PyQt5 import QtGui
app=QtWidgets.QApplication(sys.argv) #pyqt窗口必须在QApplication方法中使用
label=QtWidgets.QLabel()
label.resize(1920,1080)
#label.show()
label.showFullScreen() #全屏显示
img = QtGui.QPixmap('./1.jpg').scaled(label.width(), label.height())
label.setPixmap(img)

