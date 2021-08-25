# GENERAL
BASE_URL = "https://untappd.com/"
API_URL = "https://untappd.com/api/"
# DEFAULT
DEFAULT_COUNTRY = "poland"
DEFAULT_TYPES = ["micro_brewery", "contract_brewery"]
DEFAULT_RATING = 3.8
MAX_DAYS = 60
DEFAULT_SORTING = 'newest'
# DATE FORMAT
PROVIDER_FORMAT = "%m/%d/%y"
TARGET_FORMAT = "%d-%m-%Y"
# BREWERY
GLOBAL = "global"
BREWERY_EXT = "brewery/top_rated"
COUNTRY_EXT = "country="
TYPE_EXT = "brewery_type="
AVAILABLE_COUNTRIES = [DEFAULT_COUNTRY, GLOBAL]
AVAILABLE_TYPES = DEFAULT_TYPES
BREWERY_SEARCH = BASE_URL + "/v4/search/brewery?q="
# TOP LISTS
BEER_EXT = "/beer"
PROVIDER_SELECTORS = {
    "beer_name": "div.beer-details p.name a",
    "rating": "div.details div.details-item.rating-container div span",
    "release_date": "div.details div.details-item.date",
    "style": "div.beer-details p.style",
}
# SORTING OPTIONS
SORT_EXT = "sort="
COUNTRY_ID_EXT = "country_id="
SORT_OPTIONS = {
    'newest': "created_at_desc",
    'top_rated': "highest_rated",
}
COUNTRY_IDS = {
    'poland': '72'
}
AVAILABLE_AREA = [country for country in COUNTRY_IDS] + [GLOBAL]
