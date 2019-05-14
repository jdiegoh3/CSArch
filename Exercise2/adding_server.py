import socket
import multiprocessing as mp
import threading as thread
import sys


def message_handler(conn, address):
    import sys
    import lib.protocol_utils as protocol_utils
    import time
    import datetime

    print("New connection from", address)
    actual_time = datetime.datetime.utcnow()
    log_file = open("adding_server_log.csv", "+a")
    time.sleep(60)
    raw_data = conn.recv(1024)

    log_file.write("{},{},{},{},{}".format(actual_time.isoformat(), time.mktime(actual_time.timetuple()), address[0], address[1], raw_data))

    data = protocol_utils.MessageHandler(raw_data).message_loads()
    if data and data[0] == "+":
        try:
            message = protocol_utils.MessageResponseBuilder(False, str(float(data[1]) + float(data[2])))
        except ValueError:
            message = protocol_utils.MessageResponseBuilder(True, "The operands requires to be numbers")
    else:
        message = protocol_utils.MessageResponseBuilder(True, "Invalid operation")
    try:
        log_file.write(",{}\n".format(message.get_message()))
        log_file.close()
        conn.sendall(message.get_message())
        conn.close()
    except Exception:
        print("Connection lost")
    sys.exit()



def identification_handler(conn, address, operation_service_addr, operation_service_port):
    raw_data = conn.recv(1024)
    data = raw_data.decode("utf-8")
    if data == "Sv?":
        message = "serv|{}|{}".format("+", operation_service_port)
        conn.sendall(message.encode())
    else:
        conn.send("400".encode())
    conn.close()
    sys.exit()


def thread_operation(socket_o):
    print("Adding server operation service running ...")
    while True:
        conn, addr = socket_o.accept()
        temp_process = mp.Process(target=message_handler, args=(conn, addr))
        temp_process.start()
        temp_process.join()


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
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    sockname = socket_instance.getsockname()

    t_identification = thread.Thread(target=thread_identification, args=(sockname[0], sockname[1]))
    t_identification.start()

    print("Adding server operation service running ...")
    processes = []
    while True:
        conn, addr = socket_instance.accept()
        temp_process = mp.Process(target=message_handler, args=(conn, addr))
        processes.append(temp_process)
        temp_process.start()

