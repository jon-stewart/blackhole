import socket
import struct

PORT = 60001
IP_ORIGDSTADDR = 20


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_IP, socket.IP_TRANSPARENT, 1)
    sock.setsockopt(socket.SOL_IP, IP_ORIGDSTADDR, 1)

    sock.bind(('127.0.0.1', PORT))

    while True:
        message, address, port = listen(sock)

        print('[{} - {}] {}'.format(address, port, message))


def listen(sock):
    message, ancillary_data, _, (address, _) = sock.recvmsg(4096, socket.CMSG_SPACE(24))

    port = None

    for cmsg_level, cmsg_type, cmsg_data in ancillary_data:
        if cmsg_level == socket.SOL_IP and cmsg_type == IP_ORIGDSTADDR:
            _, port = struct.unpack('=HH', cmsg_data[0:4])
            port = socket.htons(port)
            break

    return message, address, port


if __name__ == '__main__':
    main()
