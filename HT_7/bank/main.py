from csv import reader
from csv import writer
from json import dump
from json import load
from datetime import datetime


def start():
    while True:
        selected_option = get_option("Выберите действие:", ("1. Логин", "2. Регистрация", "3. Завершение работы"))
        if selected_option == 1:
            current_user = login()
            if current_user is not None:
                user_menu(current_user[0])
            else:
                continue
        if selected_option == 2:
            current_user = registration()
            if current_user is not None:
                user_menu(current_user[0])
            else:
                continue
        elif selected_option == 3:
            return


def get_option(title, options):
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


def get_user_by_credentials(username, password):
    user = get_user_by_username(username)
    if user is not None:
        if user[1] == password:
            return username, password
    return


def get_user_by_username(username):
    with open("users.data", "r", encoding="utf-8") as users_file:
        users = [*reader(users_file, delimiter=',')]
        for user in users:
            if user[0] == username:
                return tuple(user)
        return


def login():
    while True:
        username = input("Введите логин:\n")
        password = input("Ведите пароль:\n")
        current_user = get_user_by_credentials(username, password)
        if current_user is None:
            selected_option = get_option("Пользователь не найден. Попробовать снова?", ("1. Да", "2. Нет"))
            if selected_option == 1:
                continue
            elif selected_option == 2:
                return
        return current_user


def registration():
    while True:
        username = input("Введите логин:\n")
        if get_user_by_username(username) is not None:
            selected_option = get_option("Вы не можете использовать это имя. Попробовать снова?", ("1. Да", "2. Нет"))
            if selected_option == 1:
                continue
            elif selected_option == 2:
                return
        password = input("Введите пароль:\n")
        perform_after_registration_actions(password, username)

        return username, password


def perform_after_registration_actions(password, username):
    with open("users.data", "a", encoding="utf-8", newline='') as users_file:
        writer(users_file).writerow([username, password])
    with open(f"{username}_balance.data", "w", encoding="utf-8") as user_balance_file:
        user_balance_file.write(str(0.0))
    with open(f"{username}_transactions.data", "w", encoding="utf-8") as user_transactions_file:
        transactions = []
        dump(transactions, user_transactions_file)


def user_menu(username):
    while True:
        selected_option = get_option("Выберите действие:",
                                     ("1. Просмотреть баланс", "2. Снять наличные", "3. Пополнить счет",
                                      "4. Посмотреть историю транзакций", "5. Выход"))
        if selected_option == 1:
            show_balance(username)
        elif selected_option == 2:
            withdraw_amount(username)
        elif selected_option == 3:
            refill_amount(username)
        elif selected_option == 4:
            show_transaction_history(username)
        elif selected_option == 5:
            return


def show_balance(username):
    with open(f"{username}_balance.data", "r", encoding="utf-8") as user_balance_file:
        print("\nНа Вашем счету: {:.2f} \n".format(float(user_balance_file.readline().rstrip())))


def withdraw_amount(username):
    with open(f"{username}_balance.data", "r", encoding="utf-8") as user_balance_file:
        balance = float(user_balance_file.readline().rstrip())
        while True:
            amount_to_withdraw = input("Введите сумму, которую хотите снять:\n")
            if not validate_float(amount_to_withdraw):
                selected_option = get_option("Вы ввели некорректную сумму. Попробовать снова?", ("1. Да", "2. Нет"))
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            amount_to_withdraw = float(amount_to_withdraw)
            if not validate_amount_to_withdraw(amount_to_withdraw, balance):
                selected_option = get_option("Сумма, которую вы ввели недоступна. Попробовать снова?",
                                             ("1. Да", "2. Нет"))
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            new_balance = balance - amount_to_withdraw
            with open(f"{username}_balance.data", "w", encoding="utf-8") as user_balance_file:
                user_balance_file.write(str(new_balance))
            with open(f"{username}_transactions.data", "r", encoding="utf-8") as user_transactions_file:
                transactions = load(user_transactions_file)
                transactions.append({"user": username, "type": "снятие", "amount": amount_to_withdraw,
                                     "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S")})
            with open(f"{username}_transactions.data", "w", encoding="utf-8") as user_transactions_file:
                dump(transactions, user_transactions_file, indent=4, ensure_ascii=False)
            print("\nВы успешно сняли: {:.2f}".format(amount_to_withdraw))
            print("На Вашем счету: {:.2f}\n".format(new_balance))
            break


def refill_amount(username):
    with open(f"{username}_balance.data", "r", encoding="utf-8") as user_balance_file:
        balance = float(user_balance_file.readline().rstrip())
        while True:
            amount_to_refill = input("Введите сумму, на которую Вы хотите пополнить счет:\n")
            if not validate_float(amount_to_refill):
                selected_option = get_option("Вы ввели некорректную сумму. Попробовать снова?", ("1. Да", "2. Нет"))
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            amount_to_refill = float(amount_to_refill)
            new_balance = balance + amount_to_refill
            with open(f"{username}_balance.data", "w", encoding="utf-8") as user_balance_file:
                user_balance_file.write(str(new_balance))
            with open(f"{username}_transactions.data", "r", encoding="utf-8") as user_transactions_file:
                transactions = load(user_transactions_file)
                transactions.append({"user": username, "type": "пополнение", "amount": amount_to_refill,
                                     "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S")})
            with open(f"{username}_transactions.data", "w", encoding="utf-8") as user_transactions_file:
                dump(transactions, user_transactions_file, indent=4, ensure_ascii=False)
            print("\nВы успешно пополнили: {:.2f}".format(amount_to_refill))
            print("На Вашем счету: {:.2f}\n".format(new_balance))
            break


def show_transaction_history(username):
    with open(f"{username}_transactions.data", "r", encoding="utf-8") as user_transactions_file:
        transactions = load(user_transactions_file)
        print("\nИстория транзакций:\n")
        print("Тип".ljust(15), "Сумма".ljust(10), "Дата и время".ljust(20))
        for transaction in transactions:
            print(transaction["type"].ljust(15), "{:.2f}".format(transaction["amount"]).ljust(10),
                  transaction["timestamp"].ljust(20))
        print()

def validate_float(string):
    try:
        return float(string) > 0
    except ValueError as e:
        return False


def validate_amount_to_withdraw(amount_to_withdraw, available_amount):
    return amount_to_withdraw <= available_amount


start()
