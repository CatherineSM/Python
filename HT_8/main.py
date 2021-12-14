from csv import reader
from csv import writer
from json import dump
from json import load
from datetime import datetime

DENOMINATIONS = [10, 20, 50, 100, 200, 500, 1000]


def start():
    while True:
        selected_option = get_option("Выберите действие:", ("1. Логин", "2. Регистрация", "3. Завершение работы"))
        if selected_option == 1:
            current_user = login()
            if current_user is not None:
                if current_user[2] == "admin":
                    print("Вы зашли как администратор")
                    admin_menu()
                else:
                    print("Вы зашли как пользователь")
                    user_menu(current_user[0])
            else:
                continue
        if selected_option == 2:
            current_user = registration()
            if current_user is not None:
                print("Вы зарегистрировались как пользователь")
                user_menu(current_user[0])
            else:
                continue
        elif selected_option == 3:
            return


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


def get_user_by_credentials(username, password):
    user = get_user_by_username(username)
    if user is not None:
        if user[1] == password:
            return user
    return


def get_user_by_username(username):
    with open("users.csv", "r", encoding="utf-8") as users_file:
        users = [*reader(users_file, delimiter=',')]
        for user in users:
            if user[0] == username:
                return tuple(user)
        return


def login():
    remain_attempts = 3
    while True:
        username = input("Введите логин:\n")
        password = input("Ведите пароль:\n")
        current_user = get_user_by_credentials(username, password)
        if current_user is None:
            remain_attempts -= 1
            if remain_attempts == 0:
                print("Вы исчерпали максимальное количество поппыток входа. Выход в Главное меню.\n")
                return
            selected_option = get_option("Пользователь не найден. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                return
        return current_user


def registration():
    while True:
        username = input("Введите логин:\n")
        if get_user_by_username(username) is not None:
            selected_option = get_option("Вы не можете использовать это имя. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                return
        password = input("Введите пароль:\n")
        perform_after_registration_actions(password, username)

        return username, password


def perform_after_registration_actions(password, username):
    with open("users.csv", "a", encoding="utf-8", newline='') as users_file:
        writer(users_file).writerow([username, password, "user"])
    with open(f"{username}_balance.data", "w", encoding="utf-8") as user_balance_file:
        user_balance_file.write(str(0))
    with open(f"{username}_transactions.json", "w", encoding="utf-8") as user_transactions_file:
        transactions = []
        dump(transactions, user_transactions_file)


def show_cash_machine_state():
    with open("cash_machine.json") as cash_machine_file:
        cash_machine_state = load(cash_machine_file)
        available_banknotes = cash_machine_state["banknotes"]
        withdraw_limit = cash_machine_state["withdraw_limit"]
        print("\nДоступные банкноты:")
        print_banknotes(available_banknotes)
        print(f"\nЛимит снятия наличных: {withdraw_limit}\n")


def print_banknotes(banknotes_dictionary):
    print("Номинал".ljust(10), "Количество".ljust(10))
    for k in sorted(banknotes_dictionary.keys(), reverse=True):
        print(str(k).ljust(10), str(banknotes_dictionary[k]).ljust(10))


def refill_cache_machine():
    options = tuple(f"{i + 1}. {DENOMINATIONS[i]}" for i in range(len(DENOMINATIONS)))
    selected_denomination_option = get_option(
        "Выберите номинал купюр, которыми Вы хотите выполнить операцию инкассации:",
        options)
    while True:
        banknotes_count = input("Выберите количество купюр, которые хотите внести:\n")
        if not validate_positive_int(banknotes_count):
            selected_option = get_option("Вы ввели некорректное количество. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                print("Вы не завершили операцию инкассации. Выход в меню администратора\n")
                break
        banknotes_count = int(banknotes_count)
        break
    denomination = DENOMINATIONS[selected_denomination_option - 1]
    with open("cash_machine.json") as cash_machine_file:
        cash_machine_state = load(cash_machine_file)
        available_banknotes = {int(k): v for k, v in cash_machine_state["banknotes"].items()}
        increase_value_with_key(available_banknotes, denomination, banknotes_count)
        cash_machine_state["banknotes"] = available_banknotes
    with open("cash_machine.json", "w") as cash_machine_file:
        dump(cash_machine_state, cash_machine_file, indent=4, ensure_ascii=False)
    print(f"Вы успешно внесли {banknotes_count} купюр номиналом {denomination} гривен")
    show_cash_machine_state()


def increase_value_with_key(dictionary, key, value_to_add=1):
    if key in dictionary.keys():
        dictionary[key] = dictionary[key] + value_to_add
    else:
        dictionary[key] = value_to_add


def change_withdraw_limit():
    while True:
        new_withdraw_limit = input("Выберите лимит снятия за раз:\n")
        if not validate_positive_int(new_withdraw_limit):
            selected_option = get_option("Вы ввели некорректную сумму. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        new_withdraw_limit = int(new_withdraw_limit)
        break
    with open("cash_machine.json") as cash_machine_file:
        cash_machine_state = load(cash_machine_file)
        cash_machine_state["withdraw_limit"] = new_withdraw_limit
    with open("cash_machine.json", "w") as cash_machine_file:
        dump(cash_machine_state, cash_machine_file, indent=4, ensure_ascii=False)
    print(f"Вы успешно изменили лимит снятия за раз до {new_withdraw_limit} грн")
    show_cash_machine_state()


def admin_menu():
    while True:
        selected_option = get_option("Выберите действие:",
                                     ("1. Просмотреть состояние банкомата", "2. Выполнить инкассацию",
                                      "3. Изменить лимит снятия наличных",
                                      "4. Выход"))
        if selected_option == 1:
            show_cash_machine_state()
        elif selected_option == 2:
            refill_cache_machine()
        elif selected_option == 3:
            change_withdraw_limit()
        elif selected_option == 4:
            return


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
        print(f"\nНа Вашем счету: {user_balance_file.readline().rstrip()} грн\n")


def withdraw_amount(username):
    with open(f"{username}_balance.data", "r", encoding="utf-8") as user_balance_file:
        balance = int(user_balance_file.readline().rstrip())
    while True:
        amount_to_withdraw = input("Введите сумму, которую хотите снять:\n")
        if not validate_positive_int(amount_to_withdraw):
            selected_option = get_option("Вы ввели некорректную сумму. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        amount_to_withdraw = int(amount_to_withdraw)
        if not validate_amount_to_withdraw(amount_to_withdraw, balance):
            selected_option = get_option("Сумма, которую вы ввели недоступна на Вашем счету. Попробовать снова?",
                                         ("1. Да", "2. Нет"))
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        if not validate_amount_to_withdraw_for_limit(amount_to_withdraw):
            selected_option = get_option("Сумма, которую Вы ввели превышает лимит выдачи за раз. Попробовать снова?",
                                         ("1. Да", "2. Нет"))
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        with open("cash_machine.json") as cash_machine_file:
            cash_machine_state = load(cash_machine_file)
        available_banknotes = {int(k): v for k, v in cash_machine_state["banknotes"].items() if
                               int(k) <= amount_to_withdraw and v > 0}
        banknotes_to_issue = get_banknotes_to_issue(available_banknotes, amount_to_withdraw)
        if banknotes_to_issue is None:
            selected_option = get_option("Сумма, которую вы ввели не может быть выдана. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        new_balance = balance - amount_to_withdraw
        print(f"\nВы успешно сняли: {amount_to_withdraw} грн. Получите Ваши купюры:\n")
        print_banknotes(banknotes_to_issue)
        print(f"\nНа Вашем счету: {new_balance} грн\n")
        save_information_after_withdraw(amount_to_withdraw, new_balance, username, banknotes_to_issue)
        break


def save_information_after_withdraw(amount_to_withdraw, new_balance, username, banknotes_to_issue):
    with open(f"{username}_balance.data", "w", encoding="utf-8") as user_balance_file:
        user_balance_file.write(str(new_balance))
    with open(f"{username}_transactions.json", "r", encoding="utf-8") as user_transactions_file:
        transactions = load(user_transactions_file)
        transactions.append({"user": username, "type": "снятие", "amount": amount_to_withdraw,
                             "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S")})
    with open(f"{username}_transactions.json", "w", encoding="utf-8") as user_transactions_file:
        dump(transactions, user_transactions_file, indent=4, ensure_ascii=False)
    with open("cash_machine.json") as cash_machine_file:
        cash_machine_state = load(cash_machine_file)
        available_banknotes = {int(k): v for k, v in cash_machine_state["banknotes"].items()}
        for k, v in banknotes_to_issue.items():
            increase_value_with_key(available_banknotes, k, -v)
        cash_machine_state["banknotes"] = available_banknotes
    with open("cash_machine.json", "w") as cash_machine_file_w:
        dump(cash_machine_state, cash_machine_file_w, indent=4, ensure_ascii=False)


def get_banknotes_to_issue(available_banknotes, amount_to_withdraw):

    if not is_enough_amount_available(available_banknotes, amount_to_withdraw):
        return

    banknotes_to_issue = get_banknotes_to_issue_by_greedy_algorithm(available_banknotes, amount_to_withdraw)
    if banknotes_to_issue is not None:
        return banknotes_to_issue

    if is_advanced_algorithm_needed(available_banknotes):
        return get_banknotes_to_issue_by_advanced_algorithm(available_banknotes, amount_to_withdraw)


def is_enough_amount_available(available_banknotes, amount_to_withdraw):
    total_cash_amount = 0
    available_denominations = sorted(available_banknotes.keys(), reverse=True)
    for denomination in available_denominations:
        total_cash_amount += available_banknotes[denomination] * denomination
    if total_cash_amount < amount_to_withdraw:
        return False
    else:
        return True

    
def is_advanced_algorithm_needed(available_banknotes):
    available_denominations = sorted(available_banknotes.keys())
    for i in range(1, len(available_denominations)):
        if available_denominations[i] % available_denominations[i - 1] != 0:
            return True
    return False


def get_banknotes_to_issue_by_greedy_algorithm(available_banknotes, amount_to_withdraw):
    available_denominations = sorted(available_banknotes.keys(), reverse=True)
    banknotes_to_issue = {}
    for denomination in available_denominations:
        banknotes_count = min(amount_to_withdraw // denomination, available_banknotes[denomination])
        amount_to_withdraw -= banknotes_count * denomination
        if banknotes_count > 0:
            banknotes_to_issue[denomination] = min(banknotes_count, available_banknotes[denomination])
        if amount_to_withdraw == 0:
            break
    if amount_to_withdraw != 0:
        return None
    else:
        return banknotes_to_issue


def get_banknotes_to_issue_by_advanced_algorithm(available_banknotes, amount_to_withdraw):
    all_banknotes = []
    for denomination in sorted(available_banknotes.keys(), reverse=True):
        all_banknotes += [denomination] * available_banknotes[denomination]
    possible_amounts = {0: 0}
    for banknote in all_banknotes:
        new_possible_amounts = {k + banknote: banknote for k, v in possible_amounts.items() if
                                k + banknote <= amount_to_withdraw}
        new_possible_amounts.update(possible_amounts)
        possible_amounts = new_possible_amounts
        if amount_to_withdraw in possible_amounts.keys():
            break
    if amount_to_withdraw not in possible_amounts.keys():
        return
    banknotes_to_issue = {}
    while amount_to_withdraw != 0:
        banknote = possible_amounts.get(amount_to_withdraw)
        increase_value_with_key(banknotes_to_issue, banknote)
        amount_to_withdraw -= banknote
    return banknotes_to_issue


def refill_amount(username):
    with open(f"{username}_balance.data", "r", encoding="utf-8") as user_balance_file:
        balance = int(user_balance_file.readline().rstrip())
    while True:
        amount_to_refill = input("Введите сумму, на которую Вы хотите пополнить счет:\n")
        if not validate_positive_int(amount_to_refill):
            selected_option = get_option("Вы ввели некорректную сумму. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        amount_to_refill = int(amount_to_refill)
        new_balance = balance + amount_to_refill
        with open(f"{username}_balance.data", "w", encoding="utf-8") as user_balance_file:
            user_balance_file.write(str(new_balance))
        with open(f"{username}_transactions.json", "r", encoding="utf-8") as user_transactions_file:
            transactions = load(user_transactions_file)
            transactions.append({"user": username, "type": "пополнение", "amount": amount_to_refill,
                                 "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S")})
        with open(f"{username}_transactions.json", "w", encoding="utf-8") as user_transactions_file:
            dump(transactions, user_transactions_file, indent=4, ensure_ascii=False)
        print("\nВы успешно пополнили: {:.2f}".format(amount_to_refill))
        print("На Вашем счету: {:.2f}\n".format(new_balance))
        break


def show_transaction_history(username):
    with open(f"{username}_transactions.json", "r", encoding="utf-8") as user_transactions_file:
        transactions = load(user_transactions_file)
        print("\nИстория транзакций:\n")
        print("Тип".ljust(15), "Сумма".ljust(10), "Дата и время".ljust(20))
        for transaction in transactions:
            print(transaction["type"].ljust(15), "{:.2f}".format(transaction["amount"]).ljust(10),
                  transaction["timestamp"].ljust(20))
        print()


def validate_positive_int(string):
    try:
        return int(string) > 0
    except ValueError as e:
        return False


def validate_amount_to_withdraw(amount_to_withdraw, available_amount):
    return amount_to_withdraw <= available_amount


def validate_amount_to_withdraw_for_limit(amount_to_withdraw):
    with open("cash_machine.json") as cash_machine_file:
        cash_machine_state = load(cash_machine_file)
    return  amount_to_withdraw < cash_machine_state["withdraw_limit"]


start()
