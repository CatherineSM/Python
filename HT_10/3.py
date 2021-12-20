from datetime import date, datetime, timedelta
from time import sleep
from json import loads
import requests

API_BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?"


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


def get_rates(rate_date=date.today()):
    response = requests.get(API_BASE_URL, {"json": "", "date": rate_date.strftime("%d.%m.%Y")})
    if response.status_code == 200:
        response_text = response.text
        parsed_response = loads(response_text)
        return parsed_response["exchangeRate"] if "exchangeRate" in parsed_response.keys() else None
    else:
        print("Ошибка при получении ответа от сервера:", response.status_code)
        return


def get_amount():
    while True:
        amount = input("Введите сумму:\n")
        if not validate_amount(amount):
            selected_option = get_option("Вы ввели невалидную сумму. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                return
        return float(amount)


def validate_amount(amount_string):
    try:
        amount = float(amount_string)
        return amount > 0 and amount == round(amount, 2)
    except ValueError as e:
        return False


def get_rate_by_currency_code(rates, currency_code):
    for rate in rates:
        if "currency" in rate.keys() and rate["currency"] == currency_code:
            return rate["saleRateNB"]


def main():
    rates = get_rates()
    if rates is None or len(rates) == 0:
        rates = get_rates(date.today() - timedelta(days=1))
    if rates is not None:
        currencies = list(map(lambda rate: rate["currency"],
                              filter(lambda rate: "currency" in rate.keys() and rate["currency"] != "BTC", rates)))
        currencies_options = tuple(f"{i + 1}. {currencies[i]}" for i in range(len(currencies)))
        selected_option = get_option("Выберите валюту из которой Вы хотите перевести:", currencies_options)
        source_currency = currencies[selected_option - 1]
        selected_option = get_option("Выберите валюту в которую Вы хотите перевести:", currencies_options)
        target_currency = currencies[selected_option - 1]
        amount = get_amount()
        print("Конверсия суммы:")
        if source_currency == "UAH":
            converted_amount = round(amount / get_rate_by_currency_code(rates, target_currency), 2)
            print(f"{amount} {source_currency} -> {converted_amount} {target_currency}")
        elif target_currency == "UAH":
            converted_amount = round(amount * get_rate_by_currency_code(rates, source_currency), 2)
            print(f"{amount} {source_currency} -> {converted_amount} {target_currency}")
        else:
            converted_amount = round(
                amount * get_rate_by_currency_code(rates, source_currency) /
                get_rate_by_currency_code(rates, target_currency), 2)
            print(f"{amount} {source_currency} -> {converted_amount} {target_currency}")
    else:
        print("Завершение работы")


main()
