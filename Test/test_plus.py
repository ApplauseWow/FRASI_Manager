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

import threading
import time

def test():
    threading.Thread(target=thread_test).start()
    for i in range(20):
        time.sleep(0.5)
        print i


def thread_test():
    print("sleep...")
    time.sleep(5)
    print("wake up")


test()