import socket


def findServer(msg=b'hi'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(10)
    s.bind(('0.0.0.0', 0))
    s.sendto(msg, ('255.255.255.255', 5000))

    reply = s.recvfrom(100)
    print(reply)

    return reply


if __name__ == '__main__':
    findServer()
