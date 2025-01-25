import socket
import threading
import pickle

NETWORK_ROLE = None         # 'server', 'client'

serverSocket = None
clientSocket = None

serverCallback = None
clientCallback = None

clientAddr = None

running = False


def reset():
    if NETWORK_ROLE == 'server':
        shutdownServer()
    else:
        shutdownClient()


# -- server

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
    global running, serverSocket, clientAddr
    running = False
    if serverSocket:
        serverSocket.close()
        #serverSocket.shutdown(socket.SHUT_RDWR)
        serverSocket = None
        clientAddr = None

def serverThread():
    while running:
        data, addr = serverSocket.recvfrom(1024)
        serverCallback(data, addr)
    print('server stopped')


# -- client

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
    global running, clientSocket
    running = False
    if clientSocket:
        clientSocket.shutdown(socket.SHUT_RDWR)
        clientSocket = None

def clientThread():
    while running:
        data = clientSocket.recv(1024)
        clientCallback(data)
    print('client stopped')


# -- game-specific messages

def sendPosition(playerpos):
    if NETWORK_ROLE == 'server':
        if not clientAddr:
            return

        msg = 'PLAYER1_POS=%s/%s' % playerpos
        serverSocket.sendto(bytes(msg, 'utf8'), clientAddr)
    else:
        msg = 'PLAYER2_POS=%s/%s' % playerpos
        clientSocket.send(bytes(msg, 'utf8'))

def sendKeyItemState(keyitem):
    if NETWORK_ROLE == 'server':
        if not clientAddr:
            return

        msg = b'KEYITEM1=' + pickle.dumps(keyitem, protocol=5)
        serverSocket.sendto(msg, clientAddr)
    else:
        msg = b'KEYITEM2=' + pickle.dumps(keyitem, protocol=5)
        clientSocket.send(msg)

def sendGameOver():
    if NETWORK_ROLE == 'server':
        if not clientAddr:
            return

        serverSocket.sendto(b'GAMEOVER', clientAddr)
    else:
        clientSocket.send(b'GAMEOVER')

def sendRestart():
    if NETWORK_ROLE == 'server':
        if not clientAddr:
            return

        serverSocket.sendto(b'RESTART', clientAddr)
    else:
        clientSocket.send(b'RESTART')

