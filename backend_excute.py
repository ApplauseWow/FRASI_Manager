# -*-coding:utf-8-*-

import SocketServer
from Util import Utility

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
            elif ret_str == "exit":
                break
            conn.sendall(bytes("task done...")) # reply


if __name__ == "__main__":
    server = SocketServer.ThreadingTCPServer(("127.0.0.1", 8080), Backend)
    server.serve_forever()
