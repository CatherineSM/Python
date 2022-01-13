from datetime import datetime
from sqlite3 import Error
from sqlite3 import connect

from cash_machine import CacheMachine
from transaction import Transaction
from transaction import TransactionType
from user import User
from user import UserRole


class SystemDao:
    DB_FILE = "cash_machine.db"

    SELECT_USER_BY_USERNAME = """ SELECT * FROM users
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

    def __init__(self) -> None:
        self.__connection = connect(SystemDao.DB_FILE)

    def __del__(self) -> None:
        self.__connection.close()

    def get_user_by_username(self, username: str) -> User:
        cursor = self.__connection.cursor()
        cursor.execute(SystemDao.SELECT_USER_BY_USERNAME, (username,))
        user_raw = cursor.fetchone()
        return User(user_raw[0], user_raw[1], user_raw[2], UserRole[user_raw[3].upper()], user_raw[4]) if user_raw else None

    def insert_new_user(self, user) -> User:
        try:
            cursor = self.__connection.cursor()
            cursor.execute(SystemDao.INSERT_USER_SQL, (user.username, user.password, str(user.role)))
            self.__connection.commit()
            user.id = cursor.lastrowid
        except Error as e:
            print("Ошибка при сохранении нового пользователя:", e)
            self.__connection.rollback()
        return user

    def update_user_balance(self, user) -> bool:
        try:
            cursor = self.__connection.cursor()
            cursor.execute(SystemDao.UPDATE_USER_BALANCE_SQL, (user.balance, user.id))
            self.__connection.commit()
            return True
        except Error as e:
            print("Ошибка при обновлении баланса пользователя:", e)
            self.__connection.rollback()
            return False

    def get_cash_machine(self) -> CacheMachine:
        return CacheMachine(self.__get_available_banknotes(), self.__get_withdraw_limit())

    def __get_available_banknotes(self) -> dict:
        cursor = self.__connection.cursor()
        cursor.execute(SystemDao.SELECT_AVAILABLE_BANKNOTES_QUERY)
        return {banknote[1]: banknote[2] for banknote in cursor.fetchall()}

    def __get_withdraw_limit(self) -> int:
        cursor = self.__connection.cursor()
        cursor.execute(SystemDao.SELECT_WITHDRAW_LIMIT_QUERY)
        return cursor.fetchone()[1]

    def update_cash_machine(self, cache_machine: CacheMachine) -> bool:
        try:
            self.__update_available_banknotes(cache_machine.banknotes)
            self.__update_withdraw_limit(cache_machine.withdraw_limit)
            self.__connection.commit()
            return True
        except Error as e:
            print("Ошибка при сохранении состояния банкомата:", e)
            self.__connection.rollback()
            return False

    def __update_available_banknotes(self, banknotes) -> None:
        cursor = self.__connection.cursor()
        for denomination, count in banknotes.items():
            cursor.execute(SystemDao.UPDATE_BANKNOTES_SQL, (count, denomination))

    def __update_withdraw_limit(self, withdraw_limit) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(SystemDao.UPDATE_WITHDRAW_LIMIT_SQL, (withdraw_limit,))

    def get_transactions_by_user(self, user) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(SystemDao.SELECT_TRANSACTIONS_BY_USER_ID_QUERY, (user.id,))
        raw_transactions = cursor.fetchall()
        transactions = []
        for raw_transaction in raw_transactions:
            transaction = Transaction(raw_transaction[0], user, raw_transaction[2],
                                      TransactionType[raw_transaction[3].upper()],
                                      datetime.fromisoformat(raw_transaction[4]))
            transactions.append(transaction)
        return transactions

    def save_data_after_transaction(self, transaction, cash_machine) -> bool:
        try:
            cursor = self.__connection.cursor()
            cursor.execute(SystemDao.UPDATE_USER_BALANCE_SQL, (transaction.user.balance, transaction.user.id))
            self.__update_available_banknotes(cash_machine.banknotes)
            self.__update_withdraw_limit(cash_machine.withdraw_limit)
            cursor.execute(SystemDao.INSERT_TRANSACTION_SQL, (transaction.user.id, transaction.amount,
                                                              str(transaction.transaction_type), transaction.timestamp))
            self.__connection.commit()
            return True
        except Error as e:
            self.__connection.rollback()
            print("Ошибка во время созранения данных после транзакции:", e)
            return False
