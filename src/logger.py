# -*- coding: utf-8 -*-
import logging


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """настройка логера, включает  метку времени,
    название модуля, уровень серьезности и сообщение
    ,описывающее событие или ошибку, которая произошла"""
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger