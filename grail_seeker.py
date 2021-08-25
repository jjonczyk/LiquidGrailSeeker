import argparse
import logging
from typing import Optional, Sequence
from breweries import BreweryBase
from download_feed import TopList
from file_config import get_file_path
from download_feed import save_feed
from constants.constants import (
    DEFAULT_RATING,
    DEFAULT_SORTING,
    DEFAULT_COUNTRY,
)


class GrailSeeker:
    def __init__(
            self,
            country: Optional[Sequence[str]] = None,
            options: Optional[Sequence[str]] = None,
            rating: Optional[Sequence[float]] = None,
            logger: Optional[Sequence[str]] = None,
    ) -> None:

        self.country = country
        self.options = options
        self.rating = rating
        self.logger = logger

    def launch(self):
        # Load configuration
        brewery_base = BreweryBase(self.country)
        breweries = brewery_base()
        self.country = brewery_base.country
        top_list = TopList(breweries, self.options, self.rating)
        self.options = top_list.options
        self.rating = top_list.min_rating

        # Collect specified data feed
        top_feed = top_list.feed
        save_path = get_file_path(self.country, self.options, self.logger)
        save_feed(top_feed, save_path)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Type the params to customize your Untappd feed. Unfilled parameters "
                                                 "will be replaced with [default] configuration.")
    parser.add_argument('-c', '--country',
                        metavar='country',
                        type=str,
                        default=DEFAULT_COUNTRY,
                        help="Available: [poland] / global")
    parser.add_argument('-o', '--options',
                        metavar='options',
                        type=str,
                        default=DEFAULT_SORTING,
                        help="Best of the last few releases - [newest] / All-time highest rated - top_rated")
    parser.add_argument('-r', '--rating',
                        metavar='min_rating',
                        type=str,
                        default=DEFAULT_RATING,
                        help="Specify min. rating in float eg. [3.80]")
    parser.add_argument('-l', '--logger',
                        metavar='logger_tag',
                        type=str,
                        default='today',
                        help="Custom file tag or current date [today]")
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_arguments()

    # Display info
    logging.info("\nLaunching the app with configuration:")
    for arg, value in vars(args).items():
        logging.info("%s: %r", arg, value)

    # Launch the app, default configuration is:
    # country='poland', options='newest', rating=3.80, logger='today'
    app = GrailSeeker(args.country, args.options, args.rating, args.logger)
    app.launch()
