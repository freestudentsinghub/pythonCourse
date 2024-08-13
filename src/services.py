import json
from typing import List

from src.utils import read_excel


def simple_search(transactions: List[dict], search_bar: str) -> str:
    """Пользователь передает строку для поиска,
    возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    list_tran = []
    for transaction in transactions:
        if (
            search_bar == transaction["Описание"]
            or search_bar == transaction["Категория"]
        ):
            list_tran.append(transaction)

    return json.dumps(list_tran, ensure_ascii=False)


search_bar = "Супермаркеты"
transactions = read_excel("../../pythonProject7/mywork/data/operations.xls")
print(simple_search(transactions, search_bar))
