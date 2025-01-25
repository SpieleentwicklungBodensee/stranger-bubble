import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 5000))

while True:
    data, addr = s.recvfrom(100)
    s.sendto(data, addr)
    print(f'{addr} asked')

