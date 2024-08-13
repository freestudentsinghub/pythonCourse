import json

from src.services import simple_search


def test_simple_search():
    """тест для функции которая возвращаетя JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""
    search_bar = "Супермаркеты"
    transactions = [
        {"Описание": "Покупка продуктов", "Категория": "Супермаркеты"},
        {"Описание": "Оплата счета", "Категория": "Утилиты"},
        {"Описание": "Покупка одежды", "Категория": "Магазины"},
    ]
    expected_result = json.dumps(
        [{"Описание": "Покупка продуктов", "Категория": "Супермаркеты"}],
        ensure_ascii=False,
    )

    assert simple_search(transactions, search_bar) == expected_result
