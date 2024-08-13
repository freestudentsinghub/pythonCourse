# -*- coding: utf-8 -*-
import os
from unittest.mock import Mock, patch

from pandas import DataFrame

from src.utils import func_user_currencies, func_user_stocks, read_excel


def test_func_user_currencies():
    """тест для функции которая достает из файла данные о 'пользовательских настройках' для курса валют"""
    user_currencies = func_user_currencies()
    assert user_currencies == ["USD", "EUR"]


def test_func_user_stocks():
    """тест для функции которая достает из файла данные о 'пользовательских настройках' для стоимости акций"""
    user_stocks = func_user_stocks()
    assert user_stocks == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


@patch("pandas.read_excel")
def test_read_excel(mock_open: Mock) -> None:
    """тест для функции которая считывает финансовые операции с файла excel"""

    mock_open.return_value = DataFrame(
        {
            "id": [650703.0],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": [16210.0],
            "currency_name": ["Sol"],
            "currency_code": ["PEN"],
            "from": ["Счет 58803664561298323391"],
            "to": ["Счет 39745660563456619397"],
            "description": ["Перевод организации"],
        }
    )
    assert read_excel(os.path.join("data/transactions_excel.xlsx")) == [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]
