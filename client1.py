import socket
import time
print('For Honour Lindy Booth!!!')

class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def put(self, metric, value, timestamp=None):
        # если не введен необязательный параметр то подставляем туда текущее время
        if not timestamp:
            timestamp = str(int(time.time()))
        message = f'put {metric} {float(value)} {timestamp}\n'
        try:
            self.sock.send(message.encode('utf8'))
            if self.sock.recv(1024).decode('utf8') == 'error\nwrong command\n\n':
                raise ClientError

        except socket.error:
            raise ClientError

    def get(self, key):
        # формируем сообщение
        message = f'get {key}\n'
        self.sock.send(message.encode('utf8'))
        try:
            # пытаемся получить его
            string = self.sock.recv(1024)
            string = string.decode('utf8')

            if string == 'error\nwrong command\n\n':
                raise ClientError

            elif string == 'ok\n\n':
                return {}
            else:
                # отсекаем первый ок и последние 2 символа
                split = string[3:-2].split('\n')
                dict_temp = {}
                for metric in split:
                    temp = metric.split()
                    if temp[0] not in dict_temp:
                        dict_temp[temp[0]] = []
                        dict_temp[temp[0]].append((int(temp[2]), float(temp[1])))
                    else:
                        dict_temp[temp[0]].append((int(temp[2]), float(temp[1])))
                return dict_temp

        except socket.error:
            raise ClientError


class ClientError(Exception):
    pass
