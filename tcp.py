import socket
import threading

BUFFER_SIZE = 1024
PORT = 60000


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TRANSPARENT, 1)

    sock.bind(('127.0.0.1', PORT))
    sock.listen(32)

    print("Bound to tcp://127.0.0.1:{}".format(PORT))

    while True:
        connection, (ip_address, _) = sock.accept()

        thread = threading.Thread(target=listen, kwargs={
            'connection': connection,
            'ip_address': ip_address})
        thread.run()


def listen(connection, ip_address):
    _, target_port = connection.getsockname()

    print("[{} - {}] Connection".format(ip_address, target_port))

    while True:
        try:
            data = connection.recv(BUFFER_SIZE)
            if data:
                print("[{} - {}] {}".format(ip_address, target_port, data))
            else:
                break
        except ConnectionResetError:
            break
        finally:
            connection.close()


if __name__ == '__main__':
    main()
