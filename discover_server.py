import socket


def waitForClient(server_id='HELLO', forever=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(10)
    s.bind(('0.0.0.0', 5000))

    while True:
        data, addr = s.recvfrom(100)
        s.sendto(bytes(server_id, 'utf8'), addr)
        print(f'{addr} asked for {data}')

        if not forever:
            return addr, data


if __name__ == '__main__':
    waitForClient(forever=True)
