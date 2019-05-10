import socket
import threading as thread


def request():
	socket_instance = socket.socket()
	socket_instance.connect(("localhost", 9999))
	message = "+|200|100"
	socket_instance.send(message.encode())
	result = socket_instance.recv(1024).decode("utf-8")
	print("Result: ", result)

if name == "__main__":
	while True:
		bomb = thread.Thread(target=request)
