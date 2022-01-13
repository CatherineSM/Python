from system import Menu
from system_dao import SystemDao
from user import User
from user import UserRole

from enum import Enum


class UserService:

    ATTEMPTS_TO_LOGIN = 3

    def __init__(self, system_dao: SystemDao):
        self.__system_dao = system_dao
        self.__current_user = None

    @property
    def current_user(self) -> User:
        return self.__current_user

    def login(self) -> User:
        remain_attempts = UserService.ATTEMPTS_TO_LOGIN
        while True:
            username = input("Введите логин:\n")
            password = input("Ведите пароль:\n")
            user = self.__system_dao.get_user_by_username(username)
            if user is None or user.password != password:
                remain_attempts -= 1
                if remain_attempts == 0:
                    print("Вы исчерпали максимальное количество поппыток входа. Выход в Главное меню.\n")
                    return None
                selected_option = Menu("Пользователь не найден. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    return None
            self.__current_user = user
            return user

    def registration(self) -> User:
        while True:
            username = input("Введите логин:\n")
            if self.__system_dao.get_user_by_username(username) is not None:
                selected_option = Menu("Вы не можете использовать это имя. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    return None
            password = input("Введите пароль:\n")
            user = User(0, username, password, UserRole.USER, 0)
            user = self.__system_dao.insert_new_user(user)
            self.__current_user = user

            return user

    def logout(self) -> None:
        self.__current_user = None

    def show_transaction_history_for_current_user(self) -> None:
        transactions = self.__system_dao.get_transactions_by_user(self.__current_user)
        print("\nИстория транзакций:\n")
        print("Тип".ljust(15), "Сумма".ljust(10), "Дата и время".ljust(20))
        for transaction in transactions:
            transaction.show_details()
        print()


