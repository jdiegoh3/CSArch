import socket
import multiprocessing as mp
# from multiprocessing.reduction import reduce_handle


def message_handler(conn):
    import sys
    # import lib.protocol_utils as protocol_utils
    # from multiprocessing.reduction import rebuild_handle
    print("Working message handler")

    # clientHandle = queue.get()
    # file_descriptor = rebuild_handle(clientHandle)
    # clientsocket = socket.fromfd(file_descriptor, socket.AF_INET, socket.SOCK_STREAM)
    print("message handler", conn)
    conn.send("sikas".encode())


if __name__ == "__main__":
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    print("Adding server running ...")
    while True:
        conn, addr = socket_instance.accept()
        # socket_queue = mp.Queue()
        # client_handle = reduce_handle(conn.fileno())
        # socket_queue.put(client_handle)
        temp_process = mp.Process(target=message_handler, args=(conn,))
        temp_process.start()
        temp_process.join()
