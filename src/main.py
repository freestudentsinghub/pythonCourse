# -*- coding: utf-8 -*-
import json

from src.views import (currency_rates_eur, currency_rates_usd, for_each_card,
                       get_greeting, get_stock_prices, symbols,
                       top_transactions_by_payment_amount, transactions)
from src.logger import setup_logger

logger = setup_logger("main", "main.log")


def main_func(datetime_str: str) -> str:
    """Главная функция, принимающая строку с датой и временем и возвращающая JSON-ответ."""
    greeting = get_greeting(datetime_str)
    cards, total_spend, cashback = for_each_card(transactions)
    top_five_transactions = top_transactions_by_payment_amount(transactions)
    currency_rates_one = currency_rates_usd()
    currency_rates_two = currency_rates_eur()
    stock_prices = get_stock_prices(symbols)
    logger.info("start main_func")
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
    logger.info("end main_func")
    return json.dumps(response, ensure_ascii=False, indent=2)


print(main_func("31.12.2021 16:44:00"))
