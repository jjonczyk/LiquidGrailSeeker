import os
from datetime import datetime
from typing import Optional

from constants.constants import AVAILABLE_COUNTRIES, SORT_OPTIONS

SAVE_DATA_DIR = "./data"


def _get_logger(logger: Optional[str] = '') -> str:
    if not logger or logger == 'today':
        logger = str(datetime.date(datetime.now()))
    elif type(logger) != str:
        logger = str(logger)
    return logger


def get_file_path(country: str, options: str, logger_tag: Optional[str] = '') -> str:
    """
    :param country: poland or global
    :param options: newest or top_rated
    :param logger_tag: custom tag or actual date
    :return: "./data/country/options_logger.txt"
    """
    logger = _get_logger(logger_tag)
    if country in AVAILABLE_COUNTRIES:
        if options in SORT_OPTIONS:
            if logger:
                dir_path = os.path.join(SAVE_DATA_DIR, country)
                file_name = f"{options}-{logger}.txt"
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                return os.path.join(dir_path, file_name)
