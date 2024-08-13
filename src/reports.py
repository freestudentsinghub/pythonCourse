from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.utils import read_excel


transactions_data = read_excel("../data/operations.xls")
transactions = pd.DataFrame(transactions_data)


def report_to_file_default(func):
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)
        with open("reports_file.txt", "w") as file:
            file.write(str(result))
        return result

    return wrapper


@report_to_file_default
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""

    if date is None:
        parsed_date = datetime.now()
    else:
        parsed_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    transactions = transactions[transactions["Сумма операции"] < 0]
    transactions = transactions[transactions["Категория"] == category]

    end_data = parsed_date - timedelta(days=90)

    transactions = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= parsed_date
    ]

    transactions = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) > end_data
    ]

    return pd.DataFrame(transactions)


print(spending_by_category(transactions, "Супермаркеты", "31.12.2021 16:42:04"))
