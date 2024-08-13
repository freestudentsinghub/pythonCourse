import json
from typing import List

from src.utils import read_excel
from src.logger import setup_logger

logger = setup_logger("services", "services.log")

def simple_search(transactions: List[dict], search_bar: str) -> str:
    """Пользователь передает строку для поиска,
    возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""
    logger.info(f"func simple_search start {search_bar}")
    list_tran = []
    for transaction in transactions:
        if (
            search_bar == transaction["Описание"]
            or search_bar == transaction["Категория"]
        ):
            list_tran.append(transaction)
    logger.info("func simple_search end")
    return json.dumps(list_tran, ensure_ascii=False)


search_bar = "Супермаркеты"
transactions = read_excel("../data/operations.xls")
print(simple_search(transactions, search_bar))
