import socket
import multiprocessing as mp


def message_handler(conn, address):
    import sys
    import lib.protocol_utils as protocol_utils
    import time
    import datetime

    actual_time = datetime.datetime.utcnow().isoformat()
    log_file = open("adding_server_log.csv", "+a")
    time.sleep(20)
    raw_data = conn.recv(1024)

    log_file.write("{},{},{},{}".format(actual_time, address[0], address[1], raw_data))

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


if __name__ == "__main__":
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    print("Adding server running ...")
    while True:
        conn, addr = socket_instance.accept()
        temp_process = mp.Process(target=message_handler, args=(conn, addr))
        temp_process.start()
        temp_process.join()
