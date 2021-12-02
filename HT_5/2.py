#2. Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
#   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
#   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну 
#цифру;
#   - щось своє :)
#   Якщо якийсь із параментів не відповідає вимогам - породити виключення із 
#відповідним текстом.

login = input()
password = input()

def is_valid(login, password):
    try:
        if len(login) < 3 or len(login) > 50:
            raise InvalidName
    except InvalidName:
        print("Пароль должен быть от 3 до 50 символов")
    try:
        for i in password:
            if i in "0123456789":
                break
            if i not in "0123456789":
                raise InvalidPassword:
    except InvalidPassword:
        print("В пароле доолжна быть цифра")
    try:
        if len(password) < 8:
            raise InvalidPassword
    except InvalidPassword:
        print("В пароле меньше 8 символов")
    try:
        for j in login:
            if j in "0123456789":
                raise NumberName
    except NumberName:
        print("В имени не должно быть цифр")
    return "ОК"

print(is_valid(login, password))
