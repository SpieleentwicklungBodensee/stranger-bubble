import socket
import threading

NETWORK_ROLE = None         # 'server', 'client'

serverSocket = None
clientSocket = None

serverCallback = None
clientCallback = None

running = False


def initServer(port, callback):
    global NETWORK_ROLE
    NETWORK_ROLE = 'server'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))

    global serverSocket
    serverSocket = s

    global running, serverCallback
    running = True
    serverCallback = callback

    t = threading.Thread(target=serverThread)
    t.start()

def shutdownServer():
    global running
    running = False
    if serverSocket:
        serverSocket.close()
        #serverSocket.shutdown(socket.SHUT_RDWR)

def serverThread():
    while running:
        data = serverSocket.recv(1024)
        serverCallback(data)


def initClient(host, port, callback):
    global NETWORK_ROLE
    NETWORK_ROLE = 'client'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))

    global clientSocket
    clientSocket = s

    global running, clientCallback
    running = True
    clientCallback = callback

    t = threading.Thread(target=clientThread)
    t.start()

    clientSocket.send(b'LETS GO!')

def shutdownClient():
    global running
    running = False
    if clientSocket:
        clientSocket.shutdown(socket.SHUT_RDWR)

def clientThread():
    while running:
        data = clientSocket.recv(1024)
        clientCallback(data)
