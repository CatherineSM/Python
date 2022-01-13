from exchange_rate import ApiClient
from cash_machine import CacheMachine
from system import Menu
from system_dao import SystemDao
from transaction import Transaction
from transaction import TransactionType
from user_service import UserService
from utils import Utils


class CashMachineService:

    def __init__(self, system_dao: SystemDao, user_service: UserService) -> None:
        self.__system_dao = system_dao
        self.__user_service = user_service
        self.__cash_machine = system_dao.get_cash_machine()

    @property
    def cash_machine(self) -> CacheMachine:
        return self.__cash_machine

    def show_cash_machine_state(self) -> None:
        self.__cash_machine.show_state()

    def refill_cache_machine(self) -> None:
        options = tuple(f"{i + 1}. {CacheMachine.DENOMINATIONS[i]}" for i in range(len(CacheMachine.DENOMINATIONS)))
        selected_denomination_option = Menu("Выберите номинал купюр, которыми Вы хотите выполнить операцию инкассации:",
                                            options).get_option()
        while True:
            banknotes_count = input("Выберите количество купюр, которые хотите внести:\n")
            if not Utils.validate_positive_int(banknotes_count):
                selected_option = Menu("Вы ввели некорректное количество. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    print("Вы не завершили операцию инкассации. Выход в меню администратора\n")
                    break
            banknotes_count = int(banknotes_count)
            break
        denomination = CacheMachine.DENOMINATIONS[selected_denomination_option - 1]
        Utils.increase_value_with_key(self.__cash_machine.banknotes, denomination, banknotes_count)
        if self.__system_dao.update_cash_machine(self.__cash_machine):
            self.__cash_machine = self.__system_dao.get_cash_machine()
            print(f"Вы успешно внесли {banknotes_count} купюр номиналом {denomination} гривен")
        self.__cash_machine.show_state()

    def change_withdraw_limit(self) -> None:
        while True:
            new_withdraw_limit = input("Выберите лимит снятия за раз:\n")
            if not Utils.validate_positive_int(new_withdraw_limit):
                selected_option = Menu("Вы ввели некорректную сумму. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            new_withdraw_limit = int(new_withdraw_limit)
            break
        self.__cash_machine.withdraw_limit = new_withdraw_limit
        if self.__system_dao.update_cash_machine(self.__cash_machine):
            print(f"Вы успешно изменили лимит снятия за раз до {new_withdraw_limit} грн")
            self.__cash_machine = self.__system_dao.get_cash_machine()
        self.__cash_machine.show_state()

    def show_exchange_rates(self) -> None:
        exchange_rates = ApiClient.get_exchange_rates()
        print("\nКурс валют:\n")
        print("Код валюты".ljust(15) + "Покупка".ljust(15) + "Продажа".ljust(15))
        for exchange_rate in exchange_rates:
            print(exchange_rate)
        print()

    def withdraw_amount(self) -> None:
        user = self.__user_service.current_user
        while True:
            amount_to_withdraw = input("Введите сумму, которую хотите снять:\n")
            if not Utils.validate_positive_int(amount_to_withdraw):
                selected_option = Menu("Вы ввели некорректную сумму. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            amount_to_withdraw = int(amount_to_withdraw)
            if not amount_to_withdraw < user.balance:
                selected_option = Menu("Сумма, которую вы ввели недоступна на Вашем счету. Попробовать снова?")\
                    .get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            if not amount_to_withdraw <= self.__cash_machine.withdraw_limit:
                selected_option = Menu("Сумма, которую Вы ввели превышает лимит выдачи за раз. Попробовать снова?")\
                    .get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            banknotes_to_issue = self.__get_banknotes_to_issue(amount_to_withdraw)
            if banknotes_to_issue is None:
                selected_option = Menu("Сумма, которую вы ввели не может быть выдана. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            user.balance -= amount_to_withdraw
            for k, v in banknotes_to_issue.items():
                Utils.increase_value_with_key(self.__cash_machine.banknotes, k, -v)
            if self.__save_information_after_withdraw(amount_to_withdraw):
                print(f"\nВы успешно сняли: {amount_to_withdraw} грн. Получите Ваши купюры:\n")
                print("Номинал".ljust(10), "Количество".ljust(10))
                for denomination in sorted(banknotes_to_issue.keys(), reverse=True):
                    print(str(denomination).ljust(10), str(banknotes_to_issue[denomination]).ljust(10))
                print(f"\nНа Вашем счету: {user.balance} грн\n")
            break

    def __get_available_banknotes(self, amount_to_withdraw: int) -> dict:
        return {int(k): v for k, v in self.__cash_machine.banknotes.items() if int(k) <= amount_to_withdraw and v > 0}

    def __save_information_after_withdraw(self, amount_to_withdraw: int) -> None:
        user = self.__user_service.current_user
        transaction = Transaction(0, user, amount_to_withdraw, TransactionType.СНЯТИЕ)
        return self.__system_dao.save_data_after_transaction(transaction, self.__cash_machine)

    def __get_banknotes_to_issue(self, amount_to_withdraw: int) -> dict:
        if not self.__is_enough_amount_available(amount_to_withdraw):
            return None

        banknotes_to_issue = self.__get_banknotes_to_issue_by_greedy_algorithm(amount_to_withdraw)
        if banknotes_to_issue is not None:
            return banknotes_to_issue

        if self.__is_advanced_algorithm_needed(amount_to_withdraw):
            return self.__get_banknotes_to_issue_by_advanced_algorithm(amount_to_withdraw)

    def __is_enough_amount_available(self, amount_to_withdraw: int) -> bool:
        total_cash_amount = 0
        available_banknotes = self.__get_available_banknotes(amount_to_withdraw)
        for denomination, count in available_banknotes.items():
            total_cash_amount += denomination * count
            if total_cash_amount >= amount_to_withdraw:
                return True
        return False

    def __is_advanced_algorithm_needed(self, amount_to_withdraw: int) -> bool:
        available_banknotes = self.__get_available_banknotes(amount_to_withdraw)
        available_denominations = sorted(available_banknotes.keys())
        for i in range(1, len(available_denominations)):
            if available_denominations[i] % available_denominations[i - 1] != 0:
                return True
        return False

    def __get_banknotes_to_issue_by_greedy_algorithm(self, amount_to_withdraw: int) -> dict:
        available_banknotes = self.__get_available_banknotes(amount_to_withdraw)
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

    def __get_banknotes_to_issue_by_advanced_algorithm(self, amount_to_withdraw: int) -> dict:
        available_banknotes = self.__get_available_banknotes()
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
            return None
        banknotes_to_issue = {}
        while amount_to_withdraw != 0:
            banknote = possible_amounts.get(amount_to_withdraw)
            Utils.increase_value_with_key(banknotes_to_issue, banknote)
            amount_to_withdraw -= banknote
        return banknotes_to_issue

    def refill_amount(self) -> None:
        user = self.__user_service.current_user
        while True:
            amount_to_refill = input("Введите сумму, на которую Вы хотите пополнить счет:\n")
            if not Utils.validate_positive_int(amount_to_refill):
                selected_option = Menu("Вы ввели некорректную сумму. Попробовать снова?").get_option()
                if selected_option == 1:
                    continue
                elif selected_option == 2:
                    break
            amount_to_refill = int(amount_to_refill)
            user.balance += amount_to_refill
            self.__save_information_after_refill(amount_to_refill)
            print(f"\nВы успешно пополнили: {amount_to_refill} грн")
            print(f"На Вашем счету: {user.balance} грн\n")
            break

    def __save_information_after_refill(self, amount_to_refill: int) -> None:
        user = self.__user_service.current_user
        transaction = Transaction(0, user, amount_to_refill, TransactionType.ПОПОЛНЕНИЕ)
        return self.__system_dao.save_data_after_transaction(transaction, self.__cash_machine)

