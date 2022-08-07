import logging
from typing import Optional, Dict, Any
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time

from authentication.authentication import authorize_untappd
from constants.constants import (
    BASE_URL,
    BREWERY_EXT,
    COUNTRY_EXT,
    TYPE_EXT,
    DEFAULT_COUNTRY,
    DEFAULT_TYPES,
    GLOBAL,
    AVAILABLE_COUNTRIES,
    AVAILABLE_TYPES,
)


class BreweryBase:
    def __init__(self, country: Optional[str] = DEFAULT_COUNTRY) -> None:
        self.country = country
        self.types = DEFAULT_TYPES
        self.brewery_url = BASE_URL + BREWERY_EXT
        self.brewery_map = dict()
        self.filter_countries = True
        self.check_params(country)
        self.urls = []

    def check_params(self, country: Optional[str]):
        if not self.types:
            self.types = DEFAULT_TYPES
        for t in self.types:
            if t not in AVAILABLE_TYPES:
                logging.warning(f"Next time choose from the following: {AVAILABLE_TYPES}. Loading default values...")
                self.types = DEFAULT_TYPES
        if not country:
            self.country = DEFAULT_COUNTRY
        elif country not in AVAILABLE_COUNTRIES:
            logging.warning(f"Next time choose from the following: {AVAILABLE_COUNTRIES}. Loading default values...")
            self.country = DEFAULT_COUNTRY
        else:
            if country == GLOBAL:
                self.filter_countries = False

    def url_constructor(self) -> None:
        url = self.brewery_url
        ext_sign = '?'
        if self.filter_countries:
            url += ext_sign + COUNTRY_EXT + self.country
            ext_sign = '&'
        if type(self.types) != list:
            logging.warning(f"Types should be a list, not '{type(self.types)}'. Loading default values...")
            self.types = DEFAULT_TYPES
        self.urls = [url + ext_sign + TYPE_EXT + t for t in self.types]

    def add_breweries(self):
        if not self.urls:
            self.url_constructor()
        auth_urls = authorize_untappd(self.urls)
        for url in auth_urls:
            time.sleep(1)
            try:
                with urlopen(url) as file:
                    text = file.read().decode('utf-8')
                    soup = BeautifulSoup(text, features="html.parser")
                    page = soup.select("#slide div div div.box div div.beer-container.beer-list")[0]
                    for brewery in page.select("div"):
                        name = brewery.select("p a")
                        if not name:
                            continue
                        name = name[0].contents[0]
                        name = str(name)
                        url = brewery.find('a', href=True)
                        url = str(url['href'])
                        if url and name not in self.brewery_map.keys():
                            self.brewery_map[name] = url
            except HTTPError:
                logging.error("You've probably reached request limit. Saving already collected data...")
                break

    def __call__(self) -> Dict[str, Any]:
        if not self.brewery_map:
            self.add_breweries()
        return self.brewery_map
