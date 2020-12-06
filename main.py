import sys
import json
import requests
import file_manage    # Пользовательский модуль для работы с каталогами и файлами


# Получить данные с сервера
def get_data(link):
    try:
        response = requests.get(link)
        if response.status_code != 200:
            raise requests.RequestException
        return response.text
    except requests.RequestException:
        print('Не удалось подключиться к серверу и получить данные.\nЗавершение программы')
        sys.exit()
    except:
        print('Неизвестная ошибка при получении данных с сервера')
        sys.exit()


# Обрезать строку до max_len символов и добавить в конец троеточие
def trunc_task(task, max_len):
    if len(task) > max_len:
        return task[:max_len] + '...'
    return task


# Вернуть списки задач конкретного пользователя user        
def get_todos(user, json_todos):
    opened_tasks = []                          # Завершенные задачи
    closed_tasks = []                          # Незавершенные задачи
    user_id = user.get('id')
    
    for todo in json_todos:
        if user_id == todo.get('userId'):
            title = todo.get('title')
            if todo.get('completed'):
                opened_tasks.append( trunc_task(title, 50) )
            else:
                closed_tasks.append( trunc_task(title, 50) )
                
    return opened_tasks, closed_tasks


def main():
    link_users = 'https://json.medrating.org/users'
    link_todos = 'https://json.medrating.org/todos'
    folder = 'tasks'                           # Директория с данными пользователей

    json_users = json.loads( get_data(link_users) )
    json_todos = json.loads( get_data(link_todos) )

    file_manage.create_folder(folder)           # Создание директории folder 

    for user in json_users:

        # get() не бросает исключение, поэтому при отсутствии ключа ошибки не будет
        username = user.get('username')
        email = user.get('email')
        company = user.get('company')
        
        if username and email and company:     # Минимальные данные, необходимые для записи в файл
            opened_tasks, closed_tasks = get_todos(user, json_todos)  # Получить задачи конкретного пользователя
            file_manage.write_to_file(user, [opened_tasks, closed_tasks], folder)


main()                                         # Запуск главной программы main
