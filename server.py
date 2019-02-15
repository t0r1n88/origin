import asyncio


class Server(asyncio.Protocol):
    dict_metric = {}
    def connection_made(self, transport):
        self.transport = transport
    @staticmethod
    def put(data):

        try:
            # Обрабатываем строку
            data = data.split()
            if len(data) == 4 and data[1] != '*':
                # Проверяем наличие ключа если его нет добавляем
                if data[1] not in Server.dict_metric:
                    Server.dict_metric[data[1]] = []
                # Создаем временный кортеж для понятности
                temp_tuple = data[2],data[3]
                Server.dict_metric[data[1]].append(temp_tuple)
                return 'ok\n\n'
        except:
            return 'error\nwrong command\n\n'

    def data_received(self, data):
        data = data.decode('utf8')
        if data.startswith('put'):
            response = self.put(data)
            self.transport.write(response.encode('utf8'))
            print(Server.dict_metric)
        elif data.startswith('get'):
            response= self.get(data)
            self.transport.write(response.encode('utf8'))
        else:
            self.transport.write('error\nwrong command\n\n'.encode('utf8'))

    # @staticmethod
    # def put(data):
    #     pass

    @staticmethod
    def get(data):
        try:
            data = data.split()
            key = data[1].rstrip()
            if key not in Server.dict_metric:
                response = 'ok\n\n'
                return response
            elif key == '*':
                final_string = ''
                for key,value in Server.dict_metric.items():
                    key_lst = sorted(value,key=lambda x:x[1])
                    between_string = ''
                    for temp_tuple in key_lst:
                        bar = ' '.join(temp_tuple)
                        between_string += bar + '\n'
                    final_string += f'{key} {between_string}'
                response = f'ok\n{final_string}'
                return response
            else:
                string = ''
                key_lst =sorted( Server.dict_metric[key],key=lambda x:x[1])
                for temp_tuple in key_lst:
                    bar = ' '.join(temp_tuple)
                    string += bar +'\n'
                response = f'ok\n{key} {string}\n'
                return response



        except:
            return 'error\nwrong command\n\n'



def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
if __name__=='__main__':
    run_server('localhost',8888)