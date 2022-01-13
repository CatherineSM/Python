from enum import Enum


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

    def __str__(self) -> None:
        return self.value


class User:

    def __init__(self, id: int, username: str, password: str, role: UserRole, balance: int):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__role = role
        self.__balance = balance

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        self.__password = password

    @property
    def role(self) -> UserRole:
        return self.__role

    @role.setter
    def role(self, role: UserRole) -> None:
        self.__role = role

    @property
    def balance(self) -> int:
        return self.__balance

    @balance.setter
    def balance(self, balance: int) -> None:
        self.__balance = balance

    def show_balance(self) -> None:
        print(f"\nНа Вашем счету: {self.__balance} грн\n")
