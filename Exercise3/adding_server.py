from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket
import socketserver
import multiprocessing as mp
import threading
import sys

rpc_ip = "192.168.9.83"
rpc_port = 9999

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RegisteredFunctions:
    @staticmethod
    def add(num1, num2):
        result = float(num1) + float(num2)
        return result

class SimpleThreadedXMLRPCServer(socketserver.ThreadingMixIn, SimpleXMLRPCServer):
    pass

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleThreadedXMLRPCServer((rpc_ip, rpc_port))
        self.localServer.register_instance(RegisteredFunctions())

    def run(self):
        print("RPC Server running..")
        self.localServer.serve_forever()

def identification_handler(conn, address, operation_service_addr, operation_service_port):
    raw_data = conn.recv(1024)
    data = raw_data.decode("utf-8")
    if data == "Sv?":
        message = "serv|{}|{}|add".format("+", operation_service_port)
        conn.sendall(message.encode())
    else:
        conn.send("400".encode())
    conn.close()
    sys.exit()

def thread_identification(operation_service_addr, operation_service_port):
    socket_i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_i.bind(('', 8000))
    socket_i.listen(10)

    print("Adding server identification service running ...")
    while True:
        conn, addr = socket_i.accept()
        temp_process = mp.Process(target=identification_handler, args=(conn, addr, operation_service_addr, operation_service_port))
        temp_process.start()
        temp_process.join()


if __name__ == "__main__":
    server = ServerThread()
    server.start()

    t_identification = threading.Thread(target=thread_identification, args=(rpc_ip, rpc_port))
    t_identification.start()
