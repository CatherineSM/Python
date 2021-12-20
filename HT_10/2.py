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
        return parsed_response["exchangeRate"]
    else:
        print("Ошибка при получении ответа от сервера:", response.status_code)
        return


def get_date():
    while True:
        date_string = input("Пожалуйста, введите дату не в будущем в формате дд.мм.гггг:\n")
        if not validate_date_string(date_string):
            selected_option = get_option("Вы ввели невалидную дату. Попробовать снова?")
            if selected_option == 1:
                continue
            elif selected_option == 2:
                return
        return datetime.strptime(date_string, "%d.%m.%Y").date()


def validate_date_string(date_string):
    try:
        selected_date = datetime.strptime(date_string, "%d.%m.%Y").date()
        return selected_date <= date.today()
    except ValueError as e:
        return False


def main():
    today = date.today()
    rates = get_rates()
    if rates is not None:
        currencies = list(map(lambda rate: rate["currency"], filter(lambda rate: "currency" in rate.keys(), rates)))
        currencies_options = tuple(f"{i + 1}. {currencies[i]}" for i in range(len(currencies)))
        selected_options = get_option("Выберите валюту:", currencies_options)
        currency = currencies[selected_options - 1]
        selected_date = get_date()
        daily_rates = []
        while selected_date <= today:
            daily_rate = get_rates(selected_date)
            for currency_rate in daily_rate:
                if "currency" in currency_rate.keys() and currency_rate["currency"] == currency:
                    daily_rates.append((selected_date, currency_rate["saleRateNB"]))
            selected_date = selected_date + timedelta(days=1)

        print(f"Валюта: {currency}")
        print("Дата".ljust(15), "Курс".ljust(15), "Изменение".ljust(15))
        for i in range(len(daily_rates)):
            diff = round(daily_rates[i][1] - daily_rates[i - 1][1], 5)
            print(daily_rates[i][0].strftime("%d.%m.%Y").ljust(15), str(daily_rates[i][1]).ljust(15),
                  str(diff).ljust(15) if i > 0 else "-------".ljust(15))
    else:
        print("Завершение работы")


main()





