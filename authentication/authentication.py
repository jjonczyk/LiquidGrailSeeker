import sys
import logging
from os.path import join
from typing import List

CLIENT_PATH = {
    "id": "client_id.txt",
    "secret": "client_secret.txt",
    "user": "username.txt"
}

ID = "id"
SECRET = 'secret'
USER = 'user'
AVAILABLE_DATA = [key for key in CLIENT_PATH]
AUTH_DIR = "authentication"


def _get_data(what: str):
    if what not in AVAILABLE_DATA:
        raise ValueError
    path = join(AUTH_DIR, CLIENT_PATH[what])
    try:
        with open(path) as file:
            line = file.readline()
            if line:
                return line
    except FileNotFoundError:
        logging.error(f"\nPlease, save your {what} to the {CLIENT_PATH[what]} file")
        sys.exit(1)


def authorize(urls: List[str]):
    result = []
    for url in urls:
        my_id = _get_data(ID)
        my_secret = _get_data(SECRET)
        url += f"&client_id={my_id}&client_secret={my_secret}"
        result.append(url)
    return result
