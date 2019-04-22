import socket
import threading as thread

if __name__ == "__main__":
    # while True:
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket_instance.connect(("192.168.8.78", 9000))
    socket_instance.connect(("localhost", 9999))
    socket_instance.send("+|100|100".encode())
    msg = socket_instance.recv(1024)
    print(msg)
