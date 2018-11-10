import SocketServer


class Backend(SocketServer.BaseRequestHandler):

    def handle(self):

        conn = self.request  # return [0]data [1] address
        conn.sendall("I am robot")
        while True:
            ret_bytes = conn.recv(1024)
            ret_str = str(ret_bytes)
            if ret_str == "recognition":
                print "recognition..."
            if ret_str == "sign_in":
                print "sign in..."
            if ret_str == "test_obj":
                conn.sendall(bytes("got"))
                obj = conn.recv(1024)
                import pickle
                dic = pickle.loads(obj)
                print dic["person"].name
                dic["person"].name = "kwok"
                conn.sendall(bytes("change"))
            if ret_str == "q":
                break
            conn.sendall(bytes("task done..."))


if __name__ == "__main__":
    server = SocketServer.ThreadingTCPServer(("127.0.0.1", 8080), Backend)
    server.serve_forever()
