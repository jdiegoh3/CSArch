import socket

socket_instance = socket.socket()
socket_instance.connect(("localhost", 8000))

message = "Sv?"
socket_instance.send(message.encode())
result = socket_instance.recv(1024).decode("utf-8")
print("Result: ", result)