# -*- coding: utf-8 -*-
from typing import Dict, List
from unittest.mock import Mock, patch

import pytest

from src.utils import read_excel
from src.views import (currency_rates_eur, currency_rates_usd, for_each_card,
                       get_greeting, get_stock_prices,
                       top_transactions_by_payment_amount)


@pytest.mark.parametrize(
    "datetime_str, expected_greeting",
    [
        ("31.12.2021 06:00:00", "Доброе утро"),
        ("31.12.2021 12:00:00", "Добрый день"),
        ("31.12.2021 18:00:00", "Добрый вечер"),
        ("31.12.2021 00:00:00", "Доброй ночи"),
    ],
)
def test_get_greeting(datetime_str: str, expected_greeting: str) -> None:
    """тест для функции для определения времени суток на основе переданной даты и времени."""
    assert get_greeting(datetime_str) == expected_greeting


@pytest.mark.parametrize(
    "transactions, expected_cards, expected_total_spend, expected_cashback",
    [
        (
            [
                {"Номер карты": "*7197", "Сумма платежа": -160.89},
                {"Номер карты": "*5091", "Сумма платежа": -564},
                {"Номер карты": "*4556", "Сумма платежа": 5046},
            ],
            ["*7197", "*5091", "*4556"],
            [-160.89, -564, 5046],
            [-2.0, -6.0, 50.0],
        )
    ],
)
def test_for_each_card(
    transactions: List[Dict],
    expected_cards: List[str],
    expected_total_spend: List[float],
    expected_cashback: List[float],
) -> None:
    """тест для функции которая:
    По каждой карте: последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""
    cards, total_spend, cashback = for_each_card(transactions)
    assert cards == expected_cards
    assert total_spend == expected_total_spend
    assert cashback == expected_cashback


transactions = read_excel("../data/operations.xls")


@pytest.fixture
def test_data() -> List[Dict]:
    return [
        {
            "date": "30.12.2021 17:50:17",
            "amount": 174000.0,
            "category": "Пополнения",
            "description": "Пополнение через Газпромбанк",
        },
        {
            "date": "14.09.2021 14:57:42",
            "amount": 150000.0,
            "category": "Пополнения",
            "description": "Перевод с карты",
        },
        {
            "date": "31.07.2020 22:27:45",
            "amount": 150000.0,
            "category": "Пополнения",
            "description": "Перевод с карты",
        },
        {
            "date": "21.03.2019 17:01:38",
            "amount": 190044.51,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "date": "23.10.2018 12:26:15",
            "amount": 177506.03,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
    ]


def test_top_transactions_by_payment_amount(test_data: List[Dict]) -> None:
    """тест для функции Топ-5 транзакций по сумме платежа."""
    assert top_transactions_by_payment_amount(transactions) == test_data


def test_currency_rates_eur() -> None:
    """тест для функции курса валют EUR"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "conversion_rates": {"RUB": 93.2726, "EUR": 0.85}
    }
    with patch("requests.get", return_value=mock_response):
        result = currency_rates_eur()
        assert result == 93.2726


def test_currency_rates_usd() -> None:
    """тест для функции курса валют usd"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "conversion_rates": {"RUB": 85.1446, "EUR": 0.85}
    }
    with patch("requests.get", return_value=mock_response):
        result = currency_rates_usd()
        assert result == 85.1446


@pytest.fixture
def test_data_two() -> List[Dict]:
    return [
        {"stock": "AAPL", "price": None},
        {"stock": "AMZN", "price": None},
        {"stock": "GOOGL", "price": None},
        {"stock": "MSFT", "price": None},
        {"stock": "TSLA", "price": None},
    ]


def test_get_stock_prices(test_data_two: List[Dict]) -> None:
    """тест для функции которая получает стоимости акций по списку символов компаний"""
    assert (
        get_stock_prices(symbols=["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        == test_data_two
    )
