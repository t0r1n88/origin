import socket

with socket.create_connection(('localhost',10001)) as sock:
    sock.send(b'Lindy Booth')
    print(sock.recv(1024).decode())
