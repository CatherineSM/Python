from user import UserRole

class Menu:

    def __init__(self, title: str, options: tuple = ("1. Да", "2. Нет")):
        self.__title = title
        self.__options = options

    def print(self) -> None:
        print(self.__title)
        print(*self.__options, sep="\n")

    def get_option(self) -> int:
        self.print()
        while True:
            user_input = input()
            if self.__validate_option(user_input):
                return int(user_input)
            else:
                print(f"Неправильная опция. Введите число от 1 до {len(self.__options)}")

    def __validate_option(self, input_string) -> bool:
        try:
            option_number = int(input_string)
            return 1 <= option_number <= len(self.__options)
        except ValueError as e:
            return False

class System:

    def __init__(self, user_service, cash_machine_service):
        self.__user_service = user_service
        self.__cash_machine_service = cash_machine_service

    def start(self) -> None:
        while True:
            selected_option = Menu("Выберите действие:", ("1. Логин", "2. Регистрация", "3. Завершение работы"))\
                .get_option()
            if selected_option == 1:
                current_user = self.__user_service.login()
                if current_user is not None:
                    if current_user.role == UserRole.ADMIN:
                        print("Вы зашли как администратор")
                        self.__admin_menu()
                    elif current_user.role == UserRole.USER:
                        print("Вы зашли как пользователь")
                        self.__user_menu()
                else:
                    continue
            if selected_option == 2:
                current_user = self.__user_service.registration()
                if current_user is not None:
                    print("Вы зарегистрировались как пользователь")
                    self.__user_menu()
                else:
                    continue
            elif selected_option == 3:
                return

    def __admin_menu(self) -> None:
        while True:
            selected_option = Menu("Выберите действие:",
                                         ("1. Просмотреть состояние банкомата", "2. Выполнить инкассацию",
                                          "3. Изменить лимит снятия наличных",
                                          "4. Выход")).get_option()
            if selected_option == 1:
                self.__cash_machine_service.show_cash_machine_state()
            elif selected_option == 2:
                self.__cash_machine_service.refill_cache_machine()
            elif selected_option == 3:
                self.__cash_machine_service.change_withdraw_limit()
            elif selected_option == 4:
                self.__user_service.logout()
                return

    def __user_menu(self) -> None:
        while True:
            selected_option = Menu("Выберите действие:",
                                         ("1. Просмотреть баланс", "2. Снять наличные", "3. Пополнить счет",
                                          "4. Посмотреть историю транзакций", "5. Просмотреть курс валют", "6. Выход"))\
                .get_option()
            if selected_option == 1:
                self.__user_service.current_user.show_balance()
            elif selected_option == 2:
                self.__cash_machine_service.withdraw_amount()
            elif selected_option == 3:
                self.__cash_machine_service.refill_amount()
            elif selected_option == 4:
                self.__user_service.show_transaction_history_for_current_user()
            elif selected_option == 5:
                self.__cash_machine_service.show_exchange_rates()
            elif selected_option == 6:
                self.__user_service.logout()
                return
