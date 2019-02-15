import asyncio

def run_server(host,port):
    dict_metric ={}

    async def handle_echo(reader, writer):
        data = await reader.read(1024)
        message = data.decode()
        # Обрабатываем полученную строку
        message_lst = message.split()
        if message_lst[0] == 'put' and len(message_lst) == 4:

            if message_lst[1] not in dict_metric:
                dict_metric[message_lst[1]] = []
            temp_tuple = (message_lst[2]),(message_lst[3])
            dict_metric[message_lst[1]].append(temp_tuple)

            writer.write(b'ok\n\n')
        elif message_lst[0] == 'get':
            if message_lst[1] == '*':
                string = ''
                for key,value in dict_metric.items():

                    string2 = ''
                    for elem in value:
                        bar = ' '.join(elem)
                        string2 += bar +'\n'
                    string += f'{key} {string2}'
                message = f'ok\n{string}\n'

            else:
                if message_lst[1] in dict_metric:
                    string = ''
                    for value in dict_metric[message_lst[1]]:
                        bar = ' '.join(value)
                        string += bar
                    message =f'ok\n{message_lst[1]} {string}\n'
                else:
                    message = 'ok\n\n'
            writer.write(message.encode('utf8'))
        else:
            message = b'error\nwrong command\n\n'
            writer.write(message)

        writer.close()


    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, host, port, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# host,port = input(),int(input())
host,port = '127.0.0.1',8888
run_server(host,port)