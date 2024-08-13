from typing import Any, Hashable

import pandas as pd


def read_excel(path: str) -> list[dict[Hashable, Any]]:
    """считывает финансовые операции с файла excel"""

    excel_file = pd.read_excel(path)

    return excel_file.to_dict(orient="records")


# print(read_excel('../data/operations.xls'))
