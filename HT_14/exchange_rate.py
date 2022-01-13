from json import loads

import requests


class ApiClient:
    API_BASE_URL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

    @staticmethod
    def get_exchange_rates() -> list:
        response = requests.get(ApiClient.API_BASE_URL)
        exchange_rates_json = response.text
        exchange_rates_parsed = loads(exchange_rates_json)
        rates = []
        for parsed_rate in exchange_rates_parsed:
            if parsed_rate["ccy"] != "BTC":
                rate = ExchangeRate(parsed_rate["ccy"], float(parsed_rate["buy"]), float(parsed_rate["sale"]))
                rates.append(rate)
        return rates


class ExchangeRate:

    def __init__(self, currency_iso: str, buy_rate: float, sale_rate: float) -> None:
        self.__currency_iso = currency_iso
        self.__buy_rate = buy_rate
        self.__sale_rate = sale_rate

    @property
    def currency_iso(self) -> str:
        return self.__currency_iso

    @currency_iso.setter
    def currency_iso(self, currency_iso: str) -> None:
        self.__currency_iso = currency_iso

    @property
    def buy_rate(self) -> float:
        return self.__buy_rate

    @buy_rate.setter
    def buy_rate(self, buy_rate: float) -> None:
        self.__buy_rate = buy_rate

    @property
    def sale_rate(self) -> float:
        return self.__sale_rate

    @sale_rate.setter
    def sale_rate(self, sale_rate: float) -> None:
        self.__sale_rate = sale_rate

    def __str__(self) -> str:
        return self.currency_iso.ljust(15) + str(self.buy_rate).ljust(15) + str(self.sale_rate).ljust(15)
    
