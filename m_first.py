# Первый урок молчанова
# Простейший клиент-сервер
import socket
from select import select
import selectors

# Урок 1, простой сервер
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind(('localhost', 10001))
# server_socket.listen()
#
# while True:
#     print('Before accept')
#     client_socket, addr = server_socket.accept()
#     print('Connection from',addr)
#
#     print('before recive')
#     request = client_socket.recv(1024)
#     print(request.decode('utf8'))
#
#     if not request:
#         break
#     else:
#
#         response = 'For Glory Omnissiah and Lindy Booth'.encode('utf8')
#         client_socket.send(response)

# Урок 2 Асинхронность с простыми функциями, Событийный цикл
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind(('localhost', 10001))
# server_socket.listen()
# to_monitor = []
#
#
# def accept_connections(server_socket):
#     client_socket, addr = server_socket.accept()
#     print('Connection from', addr)
#
#     to_monitor.append(client_socket)
#
#
# def send_message(client_socket):
#     request = client_socket.recv(4096)
#     print(request.decode('utf8'))
#     if request:
#         response = 'For Glory Omnissiah\n'.encode('utf8')
#         client_socket.send(response)
#     else:
#         client_socket.close()
#
#
# def event_loop():
#     while True:
#         ready_to_read, _, _ = select(to_monitor, [], [])
#         for sock in ready_to_read:
#             if sock is server_socket:
#                 accept_connections(sock)
#             else:
#                 send_message(sock)
#
# if __name__ == '__main__':
#     to_monitor.append(server_socket)
#     event_loop()

# Урок 3. Асинхронность на колбэках, модуль selectors
selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 10001))
    server_socket.listen()

    selector.register(fileobj=server_socket,events=selectors.EVENT_READ,data=accept_connections)


def accept_connections(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    selector.register(fileobj=client_socket,events=selectors.EVENT_READ,data=send_message)



def send_message(client_socket):
    request = client_socket.recv(4096)
    print(request.decode('utf8'))
    if request:
        response = 'For Glory Omnissiah\n'.encode('utf8')
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()
        print('Соединение закрыто клиентом')

def event_loop():
    while True:
        events = selector.select()
        for key,_ in events:
            callback = key.data
            callback(key.fileobj)

if __name__=='__main__':
    server()
    event_loop()

