import socket

obj = socket.socket()

obj.connect(("127.0.0.1",8080))

ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes)
print ret_str

while True:
    inp = input("what are u talking about\n >>>")
    if inp == "q":
        obj.sendall(bytes(inp))
        break
    elif inp == 1:
        obj.sendall(bytes("recognition"))
	ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes)
        print ret_str
    elif inp == 2:
        obj.sendall(bytes("sign_in"))
	ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes)
        print ret_str
    else:
        obj.sendall(bytes(inp))
        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes)
        print ret_str

