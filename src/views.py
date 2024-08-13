# -*- coding: utf-8 -*-


import os
import requests
from datetime import datetime
from typing import List, Optional, Tuple, Any

from dotenv import load_dotenv

from src.utils import read_excel, user_currencies, user_stocks


from src.logger import setup_logger

logger = setup_logger("views", "views.log")
load_dotenv()

def get_greeting(datetime_str) -> str:
    """Функция для определения времени суток на основе переданной даты и времени."""

    dt = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S")
    current_hour = dt.hour
    logger.info(f"func get_greeting do {datetime_str}")
    if 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


transactions = read_excel("../data/operations.xls")


def for_each_card(transactions: List[dict]) -> Tuple[List[str | None], List[Any | None], List[Any | None]]:
    """По каждой карте: последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""
    logger.info("func for_each_card start")
    cards = [transaction.get("Номер карты") for transaction in transactions]
    total_spend = [transaction.get("Сумма платежа") for transaction in transactions]
    cashback = [transaction.get("Сумма платежа") // 100 for transaction in transactions]
    logger.info("func for_each_card done")
    return cards, total_spend, cashback


# print(for_each_card(transactions))


def top_transactions_by_payment_amount(transactions: List[dict]) -> List[Any]:
    """Топ-5 транзакций по сумме платежа."""
    logger.info("func top_transactions_by_payment_amount start")
    total_spend = [
        transaction.get("Сумма платежа")
        for transaction in transactions
        if transaction.get("Сумма платежа") >= 0
    ]
    top_five = sorted([spend for spend in total_spend if spend is not None], reverse=True)[:5]

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
        logger.info("func top_transactions_by_payment_amount done")
        return result
    else:
        logger.info("func top_transactions_by_payment_amount done")
        return []


# print(top_transactions_by_payment_amount(transactions))


def currency_rates_usd() -> Optional[float]:
    """Курс валют USD"""
    symbol = user_currencies[0]
    logger.info(f"func currency_rates_usd start {symbol}")
    currency_exchange_rate = requests.get(
        f"https://v6.exchangerate-api.com/v6/04fed55e4543c3c22311996f/latest/{symbol}"
    )
    data = currency_exchange_rate.json()
    conversion_rates = data.get("conversion_rates")

    if "RUB" in conversion_rates:
        logger.info(f"func currency_rates_usd end {conversion_rates["RUB"]}")
        return conversion_rates["RUB"]
    else:
        logger.info("func currency_rates_usd end")
        return None


print(currency_rates_usd())


def currency_rates_eur() -> Optional[float]:
    """Курс валют EUR"""
    symbol = user_currencies[1]
    logger.info(f"func currency_rates_eur start {symbol}")
    currency_exchange_rate = requests.get(
        f"https://v6.exchangerate-api.com/v6/04fed55e4543c3c22311996f/latest/{symbol}"
    )
    data = currency_exchange_rate.json()
    conversion_rates = data.get("conversion_rates")

    if "RUB" in conversion_rates:
        logger.info(f"func currency_rates_eyr end {conversion_rates["RUB"]}")
        return conversion_rates["RUB"]
    else:
        logger.info("func currency_rates_eur")
        return None


# print(currency_rates_eur())


def get_stock_prices(symbols: List[str]) -> List[dict]:
    """Получение стоимости акций по списку символов компаний."""
    api_key = os.getenv("API_KEY")
    stock_prices = []
    logger.info(f"func get_stock_prices start {symbols}")
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
    logger.info("func get_stock_prices end")
    return stock_prices


symbols = user_stocks
result = get_stock_prices(symbols)
# print(result)
