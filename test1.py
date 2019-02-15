import socket
with socket.create_connection(('localhost',10001)) as sock:
    # test_dcit = {'palm.cpu': [('1501864247', '15.6\n'), ('1501864247', '10.6\n'), ('54', '65\n')],
    #              'Lindy': [('Cassandra', 'Cilian\n')]}
    # # message = f"ok\nLindy {test_dcit['Lindy']}\n\n".encode('utf8')
    # # ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n
    # for key, value in test_dcit.items():
    #     bar = ''
    #
    #     for elem in value:
    #         string = ' '.join(elem)
    #         bar += string
    #         # print(bar)
    #     mes = f'ok\n{key} {bar}\n'.encode('utf8')
    #     sock.send(mes)

    message = 'put palm.cpu 10.6 1501864247\n'.encode('utf8')
    sock.send(message)
    data = sock.recv(1024)
    print(data.decode('utf8'))