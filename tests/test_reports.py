# -*- coding: utf-8 -*-
import pandas as pd

from src.reports import spending_by_category
from src.utils import read_excel

transactions_data = read_excel("../../pythonProject7/mywork/data/operations.xls")
transactions = pd.DataFrame(transactions_data)
category = "Супермаркеты"
date = "31.12.2021 16:42:04"


