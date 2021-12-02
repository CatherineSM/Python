#1. Створіть функцію, всередині якої будуть записано список із п'яти 
#користувачів (ім'я та пароль).
#   Функція повинна приймати три аргументи: два - обов'язкових (<username> та <
#password>) і третій - необов'язковий параметр <silent> (значення за 
#замовчуванням - <False>).
#   Логіка наступна:
#       якщо введено коректну пару ім'я/пароль - вертається <True>;
#       якщо введено неправильну пару ім'я/пароль і <silent> == <True> - 
#функція вертає <False>, інакше (<silent> == <False>) - породжується 
#виключення LoginException

class LoginException(Exception):
    pass

user_name = input()
user_password = input()

def validation(user_name, user_password, silent = False):
    user_input = []
    user_input.append(user_name)
    user_input.append(user_password)
    users_list = [['Vasya', 123456], ['Sasha', 654321], ['Tanya', 111111], ['Katya', 654371], ['Sara', 129456]]
    if user_input in users_list:
        return True
    else:
        if silent == True:
            return False
        try:
            if silent == False:
                raise LoginException
        except LoginException:
            print("Неверный логин/пароль")

            
result = validation(user_name, user_password)

print(result)