from sklearn.externals import joblib
from sklearn import svm
from face_recognition import face_locations, face_encodings
from PyQt5.QtGui import QPixmap, QImage
import socket
import xml.etree.ElementTree as EL
import numpy as np
from cv2.cv2 import *
import threading
import time
import dlib
import os


path = "./sys.xml"
tree = EL.parse(path)
root = tree.getroot()
param_dict = dict()

for param in root.iter("param"):
    name = param.attrib['name']
    count = param.attrib['count']
    param_dict[name] = count

# parameters of system
RECOGNITION_FRAME = param_dict["recognition_frame"] # the number of captured frames for recognition
REGISTER_FRAME = param_dict["register_frame"] # the number of captured frames for register
AUTO_SLEEP_INTERIM = param_dict["auto_sleep_interim"] # the seconds of interim
DETECT_FRAME = param_dict["detect_frame"] # the number of captured frames for detect

SWITCH = True # the status of camera - T => open F => close
DET_CACHE_SIGNAL = False # permission for saving detect cache
REC_CACHE_SIGNAL = False # permission for saving recognition cache
REG_CACHE_SIGNAL = False # permission for saving register cache

# following functions in utilities class are scalable and pluggable
# process runs in backend

class Utility(object):
    """
    utilities
    """


    @staticmethod
    def open_camera(gui_frame):
        """
        - front end
        open the camera and capture each frame to show on the GUI label
        :param gui_frame: the object of GUI label
        :return: none
        """

        # search the available device
        for i in range(4):
            device = VideoCapture(i)
            if device.isOpened():
                # device is available
                print("device connect successfully!")
                global SWITCH
                SWITCH = True
                # start timer
                # threading.Thread(target=Utility.camera_timer, args=(device, float(AUTO_SLEEP_INTERIM))).start()
                threading.Thread(target=Utility.socket_transmission, args=("timer", )).start()

                NUM_RECOGNITION_CACHE = 0  # the number of saved frames for recognition
                NUM_DETECT_CACHE = 0  # the number of saved frames for detect
                NUM_SIGN_IN_CACHE = 0  # the number of saved frames for signing in

                while True:
                    if not SWITCH:
                        # close the camera
                        device.release()
                    # capture frame
                    success, frame = device.read()
                    if not success:  # not captured  successfully
                        msg = "no frame was captured!"
                        print("no frame was captured!\nstop working...")
                        return
                    elif success:  # captured successfully
                        # data of frame
                        row = frame.shape[0]
                        col = frame.shape[1]
                        bytesPerLine = frame.shape[2] * col

                        # image processing
                        frame_flipped = flip(frame, 1)  # 0-vertical 1-horizontal -1-ver&hor
                        # thread of recognition
                        cvtColor(frame_flipped, COLOR_BGR2RGB, frame_flipped)

                        # store cache of frames
                        global DET_CACHE_SIGNAL
                        global REC_CACHE_SIGNAL
                        global REG_CACHE_SIGNAL
                        if DET_CACHE_SIGNAL:
                            print "save the cache of the frame for detect..."
                            img_path = os.path.join("./Cache/detect", "det_cache_" + str(NUM_DETECT_CACHE) + ".jpg")
                            # img_path = ("./Cache/detect/det_cache_".join(NUM_DETECT_CACHE)).join(".jpg")
                            imwrite(img_path, frame)
                            NUM_DETECT_CACHE += 1
                            if NUM_DETECT_CACHE == int(DETECT_FRAME):
                                # have finished saving cache and init the var
                                DET_CACHE_SIGNAL = False
                                NUM_DETECT_CACHE = 0
                                # send msg -- have saved cache and start detect
                                threading.Thread(target=Utility.socket_transmission, args=("detect", )).start()
                        if REC_CACHE_SIGNAL :
                            print "save the cache of the frame for recognition..."
                            img_path = os.path.join("./Cache/recognition", "rec_cache_" + str(NUM_RECOGNITION_CACHE) + ".jpg")
                            # img_path = ("./Cache/recognition/rec_cache_".join(NUM_RECOGNITION_CACHE)).join(".jpg")
                            imwrite(img_path, frame)
                            NUM_RECOGNITION_CACHE += 1
                            if NUM_RECOGNITION_CACHE == int(RECOGNITION_FRAME):
                                REC_CACHE_SIGNAL = False
                                NUM_RECOGNITION_CACHE = 0
                        if REG_CACHE_SIGNAL :
                            print "save the cache of the frame for signing in..."
                            img_path = os.path.join("./Cache/sign_in", "sign_cache_" + str(NUM_SIGN_IN_CACHE) + ".jpg")
                            # img_path = ("./Cache/sign_in/sign_cache_".join(NUM_SIGN_IN_CACHE)).join(".jpg")
                            imwrite(img_path, frame)
                            NUM_SIGN_IN_CACHE += 1
                            if NUM_SIGN_IN_CACHE == int(REGISTER_FRAME):
                                REG_CACHE_SIGNAL = False
                                NUM_SIGN_IN_CACHE = 0

                        # show on the GUI
                        gui_frame.setPixmap(QPixmap.fromImage(QImage(frame_flipped.data,
                                                                     col, row, bytesPerLine,
                                                                     QImage.Format_RGB888)).scaled(gui_frame.width(),
                                                                                                   gui_frame.height()))
            elif not device.isOpened():
                # device is not available
                msg = "device is not available!"
                print("device is not available!")
                device.release()
        else:
            # none of the devices is available
            msg = "none of the devices is available"
            print("none of the devices is available")

    @staticmethod
    def camera_timer(seconds, conn):
        """
        - backend
        close the camera after some interim
        :param seconds: interim
        :param conn: backend socket for sending message
        :return: none
        """

        print "start counting seconds..."
        time.sleep(seconds)
        # if there is a detected face pass
        # or not so, release the object of camera
        # send msg -- start storing the cache
        conn.sendall(bytes("save_det_cache"))

    @staticmethod
    def save_cache_of_frame(kind):
        """
        - front end
        save the all kinds of frames in Cache directory for specific use
        :param kind: according to the task name, save the frames
        :return: none
        """

        if kind == "detect":
            # save the cache for detect
            global DET_CACHE_SIGNAL
            DET_CACHE_SIGNAL = True
        elif kind == "recognition":
            # save the cache for recognition
            global REC_CACHE_SIGNAL
            REC_CACHE_SIGNAL = True
        elif kind == "sign_in":
            # save the cache for register
            global REG_CACHE_SIGNAL
            REG_CACHE_SIGNAL = True

    @staticmethod
    def detect_face(img_path, conn):
        """
        - backend
        detect the cache of frames if there is face
        :param img_path: detect the image in the directory of the path
        :param conn: the object of socket
        :return: boolean => true : exist false : none
        """

        detector = dlib.get_frontal_face_detector()
        for file in os.listdir(img_path):
            if file == "":
                # dir is empty
                conn.sendall(bytes("no_file"))
            else:
                file_path = os.path.join(img_path, file)
                img = imread(file_path)
                dets = detector(img, 1)
                if len(dets) > 0:
                    # there is detected face
                    print "exist face!"
                    conn.sendall(bytes("exist"))
                    break
                elif len(dets) == 0:
                    print "no face here!"
        else:
            # no face in each frame
            conn.sendall(bytes("no_face"))

    @staticmethod
    def socket_transmission(task):
        """
        - front end
        connected with backend via socket and transmit the information of task
        this function can be normalized for specific task like JAVA servlet
        :param task: a string containing the name of task
        :return: none
        """

        obj = socket.socket()
        obj.connect(("127.0.0.1", 44967))

        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes)
        if ret_str == "got":
            print "backend is working, keep accepting task..."
            obj.sendall(bytes(task))
            ret_bytes = obj.recv(1024)
            ret_str = str(ret_bytes)
            # feedback
            if ret_str == "save_det_cache":
                # start saving the cache for detect
                Utility.save_cache_of_frame("detect")
            elif ret_str == "no_file":
                # no cache exist
                print "no cache file"
            elif ret_str == "exist":
                # cant't close the camera and start timing again
                threading.Thread(target=Utility.socket_transmission, args=("timer", )).start()
            elif ret_str == "no_face":
                # close the camera
                global SWITCH
                SWITCH = False
        else:
            print "there is something wrong with backend...\nfail to connect"
        obj.close()


    @staticmethod
    def read_param_from_xml():
        """
        parse the XML file for getting the parameters of system
        :return: params_dict that a dictionary containing the parameters of system
        """

        path = "./sys.xml"
        tree = EL.parse(path)
        root = tree.getroot()
        params_dict = dict()

        for param in root.iter("param"):
            name = param.attrib['name']
            count = param.attrib['count']
            params_dict[name] = count

        return params_dict

