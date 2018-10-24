# -*-coding:utf-8-*-

import SocketServer
from Util import *


class Backend(SocketServer.BaseRequestHandler):

    def handle(self):

        conn = self.request
        conn.sendall(bytes("got"))
        while True:
            ret_bytes = conn.recv(1024) # receive the bytes stream
            ret_str = str(ret_bytes) # transport the type

            #  match the task
            if ret_str == "recognition":
                print "got it, recognition..."
            elif ret_str == "sign_in":
                print "got it, sign in..."
            elif ret_str == "timer":
                print "got it, timing..."
                threading.Thread(target=Utility.camera_timer, args=(float(AUTO_SLEEP_INTERIM),conn )).start()
            elif ret_str == "detect":
                print "got it, detect..."
                img_path = os.path.join(os.getcwd(), "Cache", "detect")
                threading.Thread(target=Utility.detect_face, args=(img_path, conn)).start()
            elif ret_str == "exit":
                break



if __name__ == "__main__":
    server = SocketServer.ThreadingTCPServer(("127.0.0.1", 44967), Backend)
    server.serve_forever()
