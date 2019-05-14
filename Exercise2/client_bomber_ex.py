import socket
import threading as thread


def request():
    socket_instance = socket.socket()
    socket_instance.connect(("localhost", 9999))
    message = "+|200|100"
    socket_instance.send(message.encode())
    result = socket_instance.recv(1024).decode("utf-8")
    print("Result: ", result)


if __name__ == "__main__":
   for i in range(0, 1000):
        bomb = thread.Thread(target=request)
        bomb.start()
