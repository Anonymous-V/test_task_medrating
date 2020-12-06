"""
    Модуль для работы с файлами.
    
    Возможности модуля:
    - создание каталогов;
    - создание файлов;
    - переименовывание файлов;
    - запись данных в файл.
"""


import os
import sys
import datetime


# Создать директорию с именем folder_name
def create_folder(folder_name):    

    if os.path.isdir(folder_name):              # Существует ли папка?
        return

    try:
        os.mkdir(folder_name)
    except OSError:
        print('Не удалось создать папку ' + folder_name)
        sys.exit()
    except:
        print('Неизвестная ошибка при создании папки')
        sys.exit()                              # Завершить работу программы


# Вернуть строку в формате <reverse_date>T<time>
# Формат line_list: ['date', 'time'] 
def get_datetime(line_list):
    reversed_date = '-'.join( line_list[0].split('.')[::-1] )
    time = line_list[-1].replace(':', '.')      # В Windows нельзя в названии файла использовать двоеточие ':'
    return reversed_date + 'T' + time 


# Переименовать файл filename.txt, добавив в название дату и время создания файла
def rename_file(old_path):
    old_path_list = old_path.rsplit('/', 1)     # Отделить путь от названия файла

    new_path = old_path_list[0]
    username = old_path_list[1].split('.')[0]

    with open(old_path, 'r') as f:
        first_line = f.readline().split()[-2:]  # Извлечь только дату и время из файла
        date_time = get_datetime(first_line)

    new_filename = '{}/{}_{}.txt'.format(new_path, username, date_time)

    try:
        os.rename(old_path, new_filename)
    except OSError:
        print('Не удалось переименовать файл ' + old_path)
        sys.exit()
    except:
        print('Неизвестная ошибка при переименовании файла')
        sys.exit()


# Записать данные пользователя и его задач в файл
def write_to_file(user, todos, folder):
    path = '{}/{}.txt'.format(folder, user.get('username'))

    if os.path.exists(path):                    # Проверить существование файла с таким же именем
        rename_file(path)

    # Создаем новый файл и записываем данные
    with open(path, 'w') as f:
        user_info = '{} <{}> {}'.format(
            user.get('name'),
            user.get('email'),
            # Для предотвращения конфликтов имен файлов чаще минуты, дополнительно используются секунды
            datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

        user_company = user.get('company').get('name')

        closed_tasks_title = '\nЗавершенные задачи:'
        opened_tasks_title = 'Оставшиеся задачи:'

        if todos[1]:
            opened_tasks_title = '\n' + opened_tasks_title

        print(user_info,
              user_company,              
              closed_tasks_title,
              '\n'.join(todos[0]),
              opened_tasks_title,
              '\n'.join(todos[1]),
              file=f, sep='\n', end='')
