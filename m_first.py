# Первый урок молчанова
# Простейший клиент-сервер
import socket

# Создаем сервер-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 10001))
server_socket.listen()

while True:
    print('Before accept')
    client_socket, addr = server_socket.accept()
    print('Connection from',addr)

    print('before recive')
    request = client_socket.recv(1024)
    print(request.decode())

    if not request:
        break
    else:
        print('else')
        response = 'For Glory Omnissiah and Lindy Booth'.encode()
        client_socket.send(response)

