import logging
from tqdm import tqdm
from typing import List, Dict, Any
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import time
import re

from authentication.authentication import authorize_untappd
from constants.constants import (
    BASE_URL,
    BEER_EXT,
    SORT_OPTIONS,
    SORT_EXT,
    PROVIDER_FORMAT,
    TARGET_FORMAT,
    MAX_DAYS,
    PROVIDER_SELECTORS,
    DEFAULT_RATING,
    DEFAULT_SORTING,
)


def save_feed(what: Dict[str, Any], save_path: str) -> None:
    with open(save_path, 'w', encoding='utf-8') as save_file:
        logging.info("\n\tSAVING YOUR FEED: \n\n")
        for brewery, beers in tqdm(what.items()):
            if beers:
                logging.debug(f"saving {str(brewery)}")
                if isinstance(beers, list):
                    size = len(brewery) + 4
                    save_file.write('\n')
                    save_file.write(size * "-")
                    save_file.write(f"\n||{brewery}||\n")
                    save_file.write(size * "-")
                    save_file.write('\n')
                    for beer in beers:
                        try:
                            save_file.write(str(beer))
                            save_file.write('\n')
                        except UnicodeDecodeError:
                            print(f"Cannot save {brewery} - {beer}")
            else:
                logging.debug(f'rejecting {brewery} (not good enough)')


def add_sorting(url: str, option: str) -> str:
    if option not in SORT_OPTIONS:
        option = DEFAULT_SORTING
    if option:
        if '?' in url:
            sorting_sign = "&"
        else:
            sorting_sign = "?"
        if option in SORT_OPTIONS.keys():
            sorting_ext = _option_sort(option)
        else:
            return url
        url += f"{sorting_sign}{sorting_ext}"
    return url


def _option_sort(option: str):
    return f"{SORT_EXT}{SORT_OPTIONS[option]}"


class TopList:
    def __init__(self,
                 input_data: Dict[str, List[Dict[str, Any]]],
                 options: str = DEFAULT_SORTING,
                 min_rating: float = DEFAULT_RATING
                 ) -> None:
        self.init_dict = input_data
        self.top_dict = dict()  # keys: brewery_name, beer_name, rating, date_added, style
        self.options = options  # newest [default], top_rated
        self.min_rating = min_rating
        self.feed = self.download_feed()

    def validate(self):
        char = False
        if not self.options:
            self.options = DEFAULT_SORTING
        if not self.min_rating or type(self.min_rating) not in [float, int] or not 0 < self.min_rating < 5:
            self.min_rating = DEFAULT_RATING
        if self.init_dict:
            if self.options:
                if self.min_rating:
                    char = True
        return char

    def prepare_urls(self):
        if not self.validate():
            raise ValueError("Wrong data loaded...")
        prepared_urls = []
        for brewery_name, brewery_ext in self.init_dict.items():
            url = urljoin(BASE_URL, brewery_ext + BEER_EXT)
            url = add_sorting(url, self.options)
            prepared_urls.append(url)
        return prepared_urls

    def _is_added(self, name):
        if self.top_dict:
            for brewery, beer_list in self.top_dict.items():
                for beer in beer_list:
                    if "beer_name" in beer:
                        if beer["beer_name"] == name:
                            return True
        return False

    def _approve_conditions(self, container: Dict, conditions: List) -> bool:
        approvals = 0
        for param in conditions:
            if param == "rating":
                if param in container and container[param] > self.min_rating:
                    approvals += 1
            if param == "release_date":
                if param in container:
                    today = datetime.today()
                    release_date = container[param]
                    release_date = datetime.strptime(release_date, TARGET_FORMAT)
                    period = today - release_date
                    if period.days < MAX_DAYS:
                        approvals += 1
        return approvals == len(conditions)

    def download_feed(self):
        urls = self.prepare_urls()
        urls = authorize_untappd(urls)
        logging.info("\n\tCOLLECTING DATA: \n")
        for url in tqdm(urls):
            time.sleep(0.5)
            try:
                with urlopen(url) as file:
                    text = file.read().decode('utf-8')
                    soup = BeautifulSoup(text, features="html.parser")
                    brewery = soup.select("#slide div.cont.brewery-page div div.box.b_info div div.top div.basic div h1")
                    brewery = str(brewery[0].contents[0]).strip()
                    beers = soup.select("#slide div div div.box.beer-list div div.beer-container")
                    brewery_feed = []
                    counter = 0
                    for beer in beers[0].select("div.beer-item"):
                        beer_entry = dict()
                        counter += 1
                        if counter > 10:
                            break
                        try:
                            for name, selector in PROVIDER_SELECTORS.items():
                                var = beer.select(selector)
                                if var:
                                    var = var[0].contents[0]
                                    var = str(var).strip()
                                    if name == "rating":
                                        var = re.sub('[()]', '', var)
                                        if not var:
                                            var = 0
                                        else:
                                            var = float(var)
                                    if name == "release_date":
                                        var = var.split()[1]
                                        var = datetime.strptime(var, PROVIDER_FORMAT).strftime(TARGET_FORMAT)
                                    beer_entry[name] = var
                        except (
                                IndexError,
                                ValueError,
                                KeyError,
                        ) as error:
                            logging.warning(f"Cannot save {var} of {name} due to {repr(error)}\n\n")
                            break
                        conditions = ["rating", 'release_date']
                        if self._approve_conditions(beer_entry.copy(), conditions):
                            brewery_feed.append(beer_entry)
                    if brewery not in self.top_dict:
                        self.top_dict[brewery] = []
                    for entry in brewery_feed:
                        self.top_dict[brewery].append(entry)
            except HTTPError:
                logging.warning("You've probably reached request limit. Saving already collected data...")
                break
        return self.top_dict
