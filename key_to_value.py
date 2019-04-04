import os,tempfile,argparse,json


# Создаем парсер аргументов
parser = argparse.ArgumentParser(description='For Glory Omnissiah')
#Добавляем аргументы
parser.add_argument('--key',help='Имя ключа')
parser.add_argument('--val',help='Значение',action='append')
print('gddg')
# Записываем созданные аргументы в переменную args
args = parser.parse_args()
print(args.key,args.val)
# Создаем словарь который будет хранить наши значения
storage_dict = {}


# #Создаем файл хранилища
# storage_path = os.path.join(tempfile.gettempdir(),'storage.data')
# with open(storage_path,'w') as f:
# # В зависимости от наличия аргументов создаем ветвление определяющее что будет делать скрипт
# # Если передан только аргумент --key,в этом случае у аргумента --val значение будет None и  условие будет False
# # Если переданы оба аргумента то условие выполнится
#     if args.key and args.val:
#         storage_dict[args.key] = args.val
#         f.write(storage_dict)
#         print('For Lindy Booth')
#
#
#
