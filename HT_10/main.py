from datetime import datetime
from sqlite3 import Error
from sqlite3 import connect
from json import loads
import requests

DENOMINATIONS = [10, 20, 50, 100, 200, 500, 1000]
DB_FILE = "cash_machine.db"

SELECT_USER_BY_ID_QUERY = """ SELECT * FROM users
                                WHERE username = ?
                            ; """

INSERT_USER_SQL = """INSERT INTO users(username, password, role) 
                        VALUES (?,?,?)
                    ;"""

SELECT_AVAILABLE_BANKNOTES_QUERY = """ SELECT * FROM banknotes 
                                WHERE count > 0
                                ORDER BY denomination DESC
                        ;"""

SELECT_WITHDRAW_LIMIT_QUERY = """ SELECT * FROM withdraw_limit; """

UPDATE_BANKNOTES_SQL = """ UPDATE banknotes 
                            SET count = ?
                            WHERE DENOMINATION = ?
                    ;"""

UPDATE_WITHDRAW_LIMIT_SQL = """ UPDATE withdraw_limit 
                            SET value = ?
                    ;"""


UPDATE_USER_BALANCE_SQL = """ UPDATE users 
                            SET balance = ?
                            WHERE id = ?
                    ;"""


INSERT_TRANSACTION_SQL = """INSERT INTO transactions(user_id, amount, type, timestamp) 
                        VALUES (?,?,?,?)
                    ;"""

SELECT_TRANSACTIONS_BY_USER_ID_QUERY = """SELECT * FROM transactions
                                        WHERE user_id = ?
                                ;"""


def start():
    while True:
        selected_option = get_option("Выберите действие:", ("1. Логин", "2. Регистрация", "3. Завершение работы"))
        if selected_option == 1:
            current_user = login()
            if current_user is not None:
                if current_user[3] == "admin":
                    print("Вы зашли как администратор")
                    admin_menu()
                else:
                    print("Вы зашли как пользователь")
                    user_menu(current_user)
            else:
                continue
        if selected_option == 2:
            current_user = registration()
            if current_user is not None:
                print("Вы зарегистрировались как пользователь")
                user_menu(current_user)
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
        if user[2] == password:
            return user
    return


def get_user_by_username(username):
    with connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(SELECT_USER_BY_ID_QUERY, (username,))
        return c.fetchone()


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
        save_user((username, password, "user"))

        return username, password


def save_user(user):
    with connect(DB_FILE) as conn:
        try:
            c = conn.cursor()
            c.execute(INSERT_USER_SQL, user)
            conn.commit()
        except Error as e:
            conn.rollback()
            print("Ошибка во время сохранения пользователя", e)


def show_cash_machine_state():
    available_banknotes = get_available_banknotes()
    withdraw_limit = get_withdraw_limit()
    print("\nДоступные банкноты:")
    print_banknotes(available_banknotes)
    print(f"\nЛимит снятия наличных: {withdraw_limit}\n")


def get_available_banknotes():
    with connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(SELECT_AVAILABLE_BANKNOTES_QUERY)
        return {banknote[1]: banknote[2] for banknote in c.fetchall()}


def get_withdraw_limit():
    with connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(SELECT_WITHDRAW_LIMIT_QUERY)
        return c.fetchone()[1]


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
    available_banknotes = get_available_banknotes()
    increase_value_with_key(available_banknotes, denomination, banknotes_count)
    if update_banknotes_count(denomination, available_banknotes.get(denomination)):
        print(f"Вы успешно внесли {banknotes_count} купюр номиналом {denomination} гривен")
    show_cash_machine_state()


def update_banknotes_count(denomination, count):
    with connect(DB_FILE) as conn:
        try:
            c = conn.cursor()
            c.execute(UPDATE_BANKNOTES_SQL, (count, denomination))
            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print("Ошибка при сохранении количества банкнот: ", e)
            return False


def update_withdraw_limit(withdraw_limit):
    with connect(DB_FILE) as conn:
        try:
            c = conn.cursor()
            c.execute(UPDATE_WITHDRAW_LIMIT_SQL, (withdraw_limit,))
            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print("Ошибка при сохранении лимита снятия наличных: ", e)
            return False


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
    if update_withdraw_limit(new_withdraw_limit):
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


def show_exchange_rate():
    response = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
    exchange_rates_json = response.text
    exchange_rates_parsed = loads(exchange_rates_json)
    print("\nКурс валют:\n")
    print("Код валюты".ljust(15), "Покупка".ljust(15), "Продажа".ljust(15))
    for rate in exchange_rates_parsed:
        if rate["ccy"] != "BTC":
            print(rate["ccy"].ljust(15), str(rate["buy"]).ljust(15), str(rate["sale"]).ljust(15))
    print()


def user_menu(user):
    while True:
        selected_option = get_option("Выберите действие:",
                                     ("1. Просмотреть баланс", "2. Снять наличные", "3. Пополнить счет",
                                      "4. Посмотреть историю транзакций", "5. Просмотреть курс валют", "6. Выход"))
        if selected_option == 1:
            show_balance(user[1])
        elif selected_option == 2:
            withdraw_amount(user[1])
        elif selected_option == 3:
            refill_amount(user[1])
        elif selected_option == 4:
            show_transaction_history(user[1])
        elif selected_option == 5:
            show_exchange_rate()
        elif selected_option == 6:
            return


def show_balance(username):
    print(f"\nНа Вашем счету: {get_user_by_username(username)[4]} грн\n")


def withdraw_amount(username):
    user = get_user_by_username(username)
    balance = user[4]
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
        available_banknotes = {int(k): v for k, v in get_available_banknotes().items() if
                               int(k) <= amount_to_withdraw and v > 0}
        banknotes_to_issue = get_banknotes_to_issue(available_banknotes, amount_to_withdraw)
        if banknotes_to_issue is None:
            selected_option = get_option("Сумма, которую вы ввели не может быть выдана. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        user = (user[0], user[1], user[2], user[3], balance - amount_to_withdraw)
        for k, v in banknotes_to_issue.items():
            increase_value_with_key(available_banknotes, k, -v)
        save_information_after_withdraw(amount_to_withdraw, user, available_banknotes)
        print(f"\nВы успешно сняли: {amount_to_withdraw} грн. Получите Ваши купюры:\n")
        print_banknotes(banknotes_to_issue)
        print(f"\nНа Вашем счету: {user[4]} грн\n")
        break


def save_information_after_withdraw(amount_to_withdraw, user, available_banknotes):
    with connect(DB_FILE) as conn:
        try:
            c = conn.cursor()
            c.execute(UPDATE_USER_BALANCE_SQL, (user[4], user[0]))
            c.execute(INSERT_TRANSACTION_SQL,
                      (user[0], amount_to_withdraw, "снятие", datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
            for denomination, count in available_banknotes.items():
                c.execute(UPDATE_BANKNOTES_SQL, (count, denomination))
            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print("Ошибка при сохранении данных при снятии суммы: ", e)
            return False


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
    user = get_user_by_username(username)
    while True:
        amount_to_refill = input("Введите сумму, на которую Вы хотите пополнить счет:\n")
        if not validate_positive_int(amount_to_refill):
            selected_option = get_option("Вы ввели некорректную сумму. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                break
        amount_to_refill = int(amount_to_refill)
        user = (user[0], user[1], user[2], user[3], user[4] + amount_to_refill)
        save_information_after_refill(amount_to_refill, user)
        print(f"\nВы успешно пополнили: {amount_to_refill} грн")
        print(f"На Вашем счету: {user[4]} грн\n")
        break


def save_information_after_refill(amount_to_refill, user):
    with connect(DB_FILE) as conn:
        try:
            c = conn.cursor()
            c.execute(UPDATE_USER_BALANCE_SQL, (user[4], user[0]))
            c.execute(INSERT_TRANSACTION_SQL,
                      (user[0], amount_to_refill, "пополнение", datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print("Ошибка при сохранении данных при зачислении суммы: ", e)
            return False


def show_transaction_history(username):
    user = get_user_by_username(username)
    print("\nИстория транзакций:\n")
    print("Тип".ljust(15), "Сумма".ljust(10), "Дата и время".ljust(20))
    for transaction in get_transaction_by_user_id(user[0]):
        print(transaction[3].ljust(15), str(transaction[2]).ljust(10),
              transaction[4].ljust(20))
    print()


def get_transaction_by_user_id(user_id):
    with connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(SELECT_TRANSACTIONS_BY_USER_ID_QUERY, (user_id,))
        return c.fetchall()


def validate_positive_int(string):
    try:
        return int(string) > 0
    except ValueError as e:
        return False


def validate_amount_to_withdraw(amount_to_withdraw, available_amount):
    return amount_to_withdraw <= available_amount


def validate_amount_to_withdraw_for_limit(amount_to_withdraw):
    return amount_to_withdraw < get_withdraw_limit()


start()
