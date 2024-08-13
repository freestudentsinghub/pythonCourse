# -*- coding: utf-8 -*-

import json
from datetime import datetime
from typing import List, Optional, Tuple

import requests

from src.utils import read_excel


def get_greeting(datetime_str) -> str:
    """Функция для определения времени суток на основе переданной даты и времени."""

    dt = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S")
    current_hour = dt.hour

    if 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


transactions = read_excel("../../pythonProject7/mywork/data/operations.xls")


def for_each_card(transactions: List[dict]) -> Tuple[List[str], List[float], List[int]]:
    """По каждой карте: последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""
    cards = [transaction.get("Номер карты") for transaction in transactions]
    total_spend = [transaction.get("Сумма платежа") for transaction in transactions]
    cashback = [transaction.get("Сумма платежа") // 100 for transaction in transactions]
    return cards, total_spend, cashback


# print(for_each_card(transactions))


def top_transactions_by_payment_amount(transactions: List[dict]) -> List[dict]:
    """Топ-5 транзакций по сумме платежа."""
    total_spend = [
        transaction.get("Сумма платежа")
        for transaction in transactions
        if transaction.get("Сумма платежа") >= 0
    ]
    top_five = sorted(total_spend, reverse=True)[:5]

    last_top = [
        transaction
        for transaction in transactions
        if transaction.get("Сумма платежа") in top_five
    ]

    if last_top:
        result = []
        for transaction in last_top[:5]:
            result.append(
                {
                    "date": transaction["Дата операции"],
                    "amount": transaction["Сумма платежа"],
                    "category": transaction["Категория"],
                    "description": transaction["Описание"],
                }
            )
        return result
    else:
        return []


# print(top_transactions_by_payment_amount(transactions))


def currency_rates_usd() -> Optional[float]:
    """Курс валют USD"""
    currency_exchange_rate = requests.get(
        "https://v6.exchangerate-api.com/v6/04fed55e4543c3c22311996f/latest/USD"
    )
    data = currency_exchange_rate.json()
    conversion_rates = data.get("conversion_rates")

    if "RUB" in conversion_rates:
        return conversion_rates["RUB"]
    else:
        return None


# print(currency_rates_usd())


def currency_rates_eur() -> Optional[float]:
    """Курс валют EUR"""
    currency_exchange_rate = requests.get(
        "https://v6.exchangerate-api.com/v6/04fed55e4543c3c22311996f/latest/EUR"
    )
    data = currency_exchange_rate.json()
    conversion_rates = data.get("conversion_rates")

    if "RUB" in conversion_rates:
        return conversion_rates["RUB"]
    else:
        return None


# print(currency_rates_eur())


def get_stock_prices(symbols: List[str]) -> List[dict]:
    """Получение стоимости акций по списку символов компаний."""
    api_key = "RO2A922012F628NY"
    stock_prices = []

    for symbol in symbols:
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}"
            f"&interval=1min&apikey={api_key}"
        )
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            time_series = data.get("Time Series (1min)")
            if time_series:

                latest_time = sorted(time_series.keys())[0]
                latest_price = time_series[latest_time]["1. open"]
                stock_prices.append({"stock": symbol, "price": float(latest_price)})
            else:
                stock_prices.append({"stock": symbol, "price": None})
        else:
            stock_prices.append({"stock": symbol, "price": None})

    return stock_prices


symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
result = get_stock_prices(symbols)
# print(result)


def main_fun(datetime_str: str) -> str:
    """Главная функция, принимающая строку с датой и временем и возвращающая JSON-ответ."""
    greeting = get_greeting(datetime_str)
    cards, total_spend, cashback = for_each_card(transactions)
    top_five_transactions = top_transactions_by_payment_amount(transactions)
    currency_rates_one = currency_rates_usd()
    currency_rates_two = currency_rates_eur()
    stock_prices = get_stock_prices(symbols)
    response = {
        "greeting": greeting,
        "cards": [
            {
                "last_digits": cards[0],
                "total_spent": total_spend[0],
                "cashback": cashback[0],
            },
            {
                "last_digits": cards[1],
                "total_spent": total_spend[1],
                "cashback": cashback[1],
            },
        ],
        "top_transactions": top_five_transactions,
        "currency_rates": [
            {"currency": "USD", "rate": currency_rates_one},
            {"currency": "EUR", "rate": currency_rates_two},
        ],
        "stock_prices": stock_prices,
    }
    return json.dumps(response, ensure_ascii=False, indent=2)


# print(main_fun("31.12.2021 16:44:00"))
