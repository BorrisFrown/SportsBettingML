import pytest
import src.constants as constants
import os

from pathlib import Path

from src.webscrape import NflScraper


@pytest.fixture
def base_stat_scraper_2019_cin():
    file_path = os.path.dirname(os.path.realpath(__file__))
    stat_path = os.path.join(file_path, 'test_stats_2019_cin.csv')
    stat_scraper = NflScraper(value_dict=constants.stat_dict,
                              directory=stat_path,
                              team='cin',
                              from_csv=True,
                              start_year=2022)
    return stat_scraper
