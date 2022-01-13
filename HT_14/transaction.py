from datetime import datetime
from enum import Enum

from user import User


class TransactionType(Enum):
    ПОПОЛНЕНИЕ = "пополнение"
    СНЯТИЕ = "снятие"

    def __str__(self) -> None:
        return self.value


class Transaction:

    def __init__(self, id: int, user: User, amount: int, transaction_type: TransactionType,
                 timestamp: datetime = datetime.now()):
        self.__id = id
        self.__user = user
        self.__amount = amount
        self.__transaction_type = transaction_type
        self.__timestamp = timestamp

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def user(self) -> User:
        return self.__user

    @user.setter
    def user(self, user: User) -> None:
        self.__user = user

    @property
    def amount(self) -> int:
        return self.__amount

    @amount.setter
    def amount(self, amount: int) -> None:
        self.__amount = amount

    @property
    def transaction_type(self) -> TransactionType:
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, transaction_type: TransactionType) -> None:
        self.__transaction_type = transaction_type

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int) -> None:
        self.__timestamp = timestamp

    def show_details(self) -> None:
        print(str(self.transaction_type).ljust(15), str(self.amount).ljust(10),
              self.timestamp.strftime("%d.%m.%Y %H:%M:%S").ljust(20))
