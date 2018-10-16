import  SocketServer

class Myserver(SocketServer.BaseRequestHandler):

	def handle(self):

		conn = self.request
		conn.sendall(bytes("I am robot"))
		while True:
			ret_bytes = conn.recv(1024)
			ret_str = str(ret_bytes)
			if ret_str == "recognition":
				print "recognition..."
			if ret_str == "sign_in":
				print "sign in..."
			if ret_str == "q":
				break
			conn.sendall(bytes("task done..."))


if __name__ == "__main__":
	server = SocketServer.ThreadingTCPServer(("127.0.0.1",8080),Myserver)
	server.serve_forever() 
