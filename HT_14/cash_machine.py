class CacheMachine:
    DENOMINATIONS = [10, 20, 50, 100, 200, 500, 1000]

    def __init__(self, banknotes: dict, withdraw_limit: int) -> None:
        self.__banknotes = banknotes
        self.__withdraw_limit = withdraw_limit

    @property
    def banknotes(self) -> dict:
        return self.__banknotes

    @banknotes.setter
    def banknotes(self, banknotes: dict) -> None:
        self.__banknotes = banknotes

    @property
    def withdraw_limit(self) -> int:
        return self.__withdraw_limit

    @withdraw_limit.setter
    def withdraw_limit(self, withdraw_limit: int) -> None:
        self.__withdraw_limit = withdraw_limit

    def show_banknotes(self) -> None:
        banknotes = self.banknotes
        print("Номинал".ljust(10), "Количество".ljust(10))
        for denomination in sorted(banknotes.keys(), reverse=True):
            print(str(denomination).ljust(10), str(banknotes[denomination]).ljust(10))

    def show_withdraw_limit(self) -> None:
        print(f"\nЛимит снятия наличных: {self.withdraw_limit}\n")

    def show_state(self) -> None:
        self.show_banknotes()
        self.show_withdraw_limit()

