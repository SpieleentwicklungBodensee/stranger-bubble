import socket

s = None

def init():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(10)
    s.bind(('0.0.0.0', 0))

def findServer(msg=b'hi'):
    s.sendto(msg, ('255.255.255.255', 5000))

    reply = s.recvfrom(100)
    print(reply)

    return reply

def shutdown():
    return # TODO at the moment this is buggy but we have no time to fix

    global s
    if s is not None:
        #s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = None


if __name__ == '__main__':
    init()
    findServer()
