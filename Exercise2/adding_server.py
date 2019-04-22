import socket
import multiprocessing as mp


def message_handler(conn):
    import sys
    import Exercise2.lib.protocol_utils as protocol_utils
    data = protocol_utils.MessageHandler(conn.recv(1024)).message_loads()
    if data and data[0] == "+":
        try:
            message = protocol_utils.MessageResponseBuilder(False, str(float(data[1]) + float(data[2])))
        except ValueError:
            message = protocol_utils.MessageResponseBuilder(True, "The operands requires to be numbers")
    else:
        message = protocol_utils.MessageResponseBuilder(True, "Invalid operation")
    try:
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
        temp_process = mp.Process(target=message_handler, args=(conn,))
        temp_process.start()
        temp_process.join()
