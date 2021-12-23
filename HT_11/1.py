from json import loads
from random import choice
import requests

API_BASE_URL = "https://jsonplaceholder.typicode.com"


def get_option(title, options=("1. Да", "2. Нет")):
    print(title)
    print(*options, sep="\n")
    while True:
        selected_option = input()
        if validate_option(selected_option, len(options)):
            return int(selected_option)
        else:
            print(f"Неправильная опция. Введите число от 1 до {len(options)}")


def validate_option(input_string, number_of_options):
    try:
        option_number = int(input_string)
        return 1 <= option_number <= number_of_options
    except ValueError as e:
        return False


def get_response_payload(url, params={}):
    response = requests.get(url, params)
    if response.status_code == 200:
        return loads(response.text)
    else:
        return


def user_menu(user_id):
    while True:
        selected_option = get_option("Выберите действие:",
                                     ("1. Просмотреть профиль", "2. Просмотреть посты", "3. Список задач",
                                      "4. Ссылка на случайную картинку", "5. Назад"))
        if selected_option == 1:
            show_user_info(user_id)
        elif selected_option == 2:
            user_posts_menu(user_id)
        elif selected_option == 3:
            user_todos_menu(user_id)
        elif selected_option == 4:
            show_random_user_image(user_id)
        elif selected_option == 5:
            return


def user_posts_menu(user_id):
    while True:
        selected_option = get_option("Выберите действие:",
                                     ("1. Просмотреть список постов пользователя", "2. Просмотреть конкретный пост пользователя",
                                     "3. Назад"))
        if selected_option == 1:
            show_user_posts(user_id)
        elif selected_option == 2:
            show_user_post(user_id)
        elif selected_option == 3:
            return


def user_todos_menu(user_id):
    while True:
        selected_option = get_option("Выберите действие:",
                                     ("1. Просмотреть невыолненные задачи", "2. Просмотреть выолненные задачи",
                                     "3. Назад"))
        if selected_option == 1:
            show_todos(user_id, False, "Невыполненные задачи")
        elif selected_option == 2:
            show_todos(user_id, True, "Выполненные задачи")
        elif selected_option == 3:
            return


def show_todos(user_id, status, title):
    print()
    print(title)
    status = "true" if status else "false"
    todos = get_response_payload(API_BASE_URL + f"/users/{user_id}/todos", {"completed": status})
    for todo in todos:
        print(f"ID: {todo['id']}".ljust(10) + f"Название: {todo['title']}")
    print()


def show_user_info(user_id):
    user_info = get_response_payload(API_BASE_URL + f"/users/{user_id}")
    print()
    print("Информация о пользователе: ")
    print("ID: ".ljust(20), user_info["id"])
    print("Имя: ".ljust(20), user_info["name"])
    print("Имя пользователя: ".ljust(20), user_info["username"])
    print("E-mail: ".ljust(20), user_info["email"])
    print("Телефон: ".ljust(20), user_info["phone"])
    print("Сайт: ".ljust(20), user_info["website"], end='\n\n')
    user_address = user_info["address"]
    print("Адрес пользователя: ")
    print("Улица: ".ljust(20), user_address["street"])
    print("Дом: ".ljust(20), user_address["suite"])
    print("Город: ".ljust(20), user_address["city"])
    print("Почтовый индекс: ".ljust(20), user_address["zipcode"])
    print("Координаты: ".ljust(20), user_address["geo"]["lat"] + "; " + user_address["geo"]["lng"], end='\n\n')
    user_company = user_info["company"]
    print("Информация о компании пользователя: ")
    print("Название: ".ljust(20), user_company["name"])
    print("Девиз: ".ljust(20), user_company["catchPhrase"])
    print("Описание: ".ljust(20), user_company["bs"], end='\n\n')


def show_user_posts(user_id):
    posts = get_response_payload(API_BASE_URL + f"/users/{user_id}/posts")
    posts_info = [get_post_short_info(posts, i) for i in range(len(posts))]
    for post_info in posts_info:
        print(post_info)


def show_user_post(user_id):
    while True:
        post_id = input("Введите ID поста, который хотите просмотреть:\n")
        if not validate_positive_int(post_id):
            selected_option = get_option("Вы вввели недопустимый ID поста. Попробовать еще раз?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                print("Выход")
                break
        if not validate_post_belongs_to_user(post_id, user_id):
            selected_option = get_option("Данный пост не принадлежит выбранному пользователю. Попробовать еще раз?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                print("Выход")
                break
        break
    post = get_response_payload(API_BASE_URL + f"/posts/{post_id}")
    if post is not None:
        print()
        print(f"ID: {post['id']}")
        print(f"Заголовок: {post['title']}")
        comments = get_response_payload(API_BASE_URL + f"/posts/{post_id}/comments")
        print(f"Количество комментариев: {len(comments)}")
        print("ID комментариев: ", *list(map(lambda comment: comment['id'], comments)))
        print("Текст:")
        print(post["body"])
        print()


def show_random_user_image(user_id):
    albums = get_response_payload(API_BASE_URL + f"/users/{user_id}/albums")
    photos = get_response_payload(API_BASE_URL + f"/albums/{choice(albums)['id']}/photos")
    print(f"Ссылка на случайную картинку пользователя: {choice(photos)['url']}")


def get_user_short_info(users, index):
    return f"{index + 1}.".ljust(4) + f"ID: {users[index]['id']}".ljust(10) + \
           f"Имя: {users[index]['name']}".ljust(30) + f"Имя пользователя: {users[index]['username']}"


def get_post_short_info(post, index):
    return f"{index + 1}.".ljust(4) + f"ID: {post[index]['id']}".ljust(10) + \
           f"Заголовок: {post[index]['title']}"


def validate_positive_int(string):
    try:
        return int(string) > 0
    except ValueError as e:
        return False


def validate_post_belongs_to_user(post_id, user_id):
    post = get_response_payload(API_BASE_URL + f"/posts/{post_id}")
    return post is not None and post["userId"] == user_id


def main():
    while True:
        users = get_response_payload(API_BASE_URL + "/users")
        options_list = [get_user_short_info(users, i) for i in range(len(users))]
        options_list.append(f"{len(users) + 1}. Выход")
        options = tuple(options_list)
        selected_option = get_option("Выберите пользователя или выйдите из программы: ", options)
        if selected_option <= len(users):
            user_id = users[selected_option - 1]["id"]
            user_menu(user_id)
        else:
            return

main()
