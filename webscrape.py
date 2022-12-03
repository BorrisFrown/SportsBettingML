import requests
from requests_html import HTMLSession
from loading_animation import Animation
import pandas as pd
import bs4
import os
import time
# TODO: Make imports look nice.

from datetime import date


def _get_row(row: bs4.Tag) -> list:
    row_list = []
    for entry in row.findAll():
        if not entry.findAll():
            if not entry.text.strip():
                next_val = ' '
            else:
                next_val = entry.text.strip()
            row_list.append(next_val)
    return row_list
#  TODO: Maybe also make an optional parameter of a [list] of row object names to leave out of the returned list


def get_this_football_season() -> int:
    today = date.today()
    if today.month <= 8:
        return today.year - 1
    elif today.month > 8:
        return today.year
    else:
        raise RuntimeError(f"Datetime module thinks that this month is {today.month}.\n"
                           f"Please check the code.")


class NflScraper:
    """This scraper is designed specifically for scraping various data from pro-football-reference.com

        TODO: Put class attributes under attributes and put instance attributes in the init.
        Attributes:
            this_year(int): (class attribute) Takes the result of get_this_football_season() [NOT ALWAYS THIS CALENDAR YEAR].
            value_dict (dict[str, str]): A dict of values for variables that will be different across different classes.
                e.g. {'url_suffix': '_line.htm', 'table_id': 'vegas_lines'}
            team (str): A small string correlating with what is accepted by pro-football-reference url.
            root_url(str): The root pro-football-reference url.
            df (pd.DataFrame): The resulting dataframe from the scrape.

        Methods:
            TODO: Put this under the actual methods

    """
    this_year = get_this_football_season()

    def __init__(self,
                 value_dict: dict[str, str],
                 directory: str,
                 team: str = 'cin',
                 read_data: bool = False,
                 start_year: int = 2002):
        self.value_dict = value_dict
        # TODO: There has got to be a better way to handle the dict, perhaps an init function to
        #  set self.value_dict based on the type of scraper
        self.directory = directory
        self.team = team
        self.read_data = read_data
        self.start_year = start_year

        self.root_url = "https://www.pro-football-reference.com/teams/"
        self.header = {
                        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
                        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "accept-encoding" : "gzip, deflate, br",
                        "accept-language" : "en-GB,en;q=0.9,en-US;q=0.8,de;q=0.7",
                        "cache-control"   : "no-cache",
                        "pragma" : "no-cache",
                        "upgrade-insecure-requests" : "1"
                        }
        # TODO: Put this stuff in constants.py
        self._get_team_df()
    #     TODO: Instead of doing very similar but different functions, these should maybe be different instances of
    #      the web scraper class.

    def write_to_csv(self, path: str):
        if os.path.exists(path):
            ow = input(f'There is already data at {path}, would you like to continue and overwrite existing data?\n'
                       f'(Type "y" for yes and "n" for no.): ')
            if ow == 'n':
                print(f'You have selected not to overwrite the existing csv.\n'
                      f'Cancelling overwrite...')
                return
            elif ow == 'y':
                print(f'Overwriting file at {path}')
                self.df.to_csv(path, index=False)
            else:
                print(f'Incorrect input: {ow}. Please try again.\n')
                self.write_to_csv(path)
        else:
            print(f'Writing to {path}...')
            self.df.to_csv(path, index=False)

    def _initialize_df(self) -> pd.DataFrame:
        """Initializes an empty DataFrame with web-scraped columns.

            Returns:
                df (pd.DataFrame): Empty dataframe with scraped columns.
        """
        url = f"{self.root_url}cin/{NflScraper.this_year}{self.value_dict['url_suffix']}"
        # TODO: Temporary hardcoded as bengals, make this dynamic
        # req = requests.Session()
        req = HTMLSession()
        page = req.get(url, headers=self.header)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id=self.value_dict['table_id'])
        bet_columns = bet_table.find('thead')
        bet_columns = bet_columns.find_all('tr')[-1].text.strip()
        col_names = list(bet_columns.split('\n'))

        if self.value_dict['data'] == 'stats':
            col_names[3] = 'Time'
            col_names[4] = 'Boxscore'
            col_names[5] = 'Result'
            col_names[8] = 'Away'
            col_names[9] = f'{col_names[9]}_name'
            for i in range(12, 17):
                col_names[i] = f'{col_names[i]}_o'
            for i in range(17, 22):
                col_names[i] = f'{col_names[i]}_d'
            # TODO: Boxscore is a placeholder, this whole column and data needs to be deleted
        col_names.insert(0, 'Year')
        col_names = list(filter(lambda a: a != '', col_names))
        df = pd.DataFrame(columns=col_names)
        return df

    def _get_team_df(self):
        if self.read_data:
            self.df = pd.read_csv(self.directory)
        #     TODO: Only read from start_year
        else:
            print('Scraping data')
            ani = Animation()
            ani.start()
            self.df = self._initialize_df()
            self._scrape_team_df(self.start_year)
            ani.stop()

    def _scrape_team_df(self, year_start):
        time.sleep(5)
        # TODO: Make year_start iterate the instance attribute
        # TODO: docstring mention the recursion
        bengals_url_root = f"{self.root_url}cin/"
        # TODO: Make the team an instance attribute
        url = f"{bengals_url_root}{year_start}{self.value_dict['url_suffix']}"

        if year_start == get_this_football_season():        # Base case
            self._get_table(url, year_start)
        elif year_start > get_this_football_season():
            raise IndexError(
                f"Trying to get a dataframe for a football season that has not yet happened ({year_start})")
        elif year_start < 2002:
            raise IndexError(
                f"Trying to get a dataframe for the {year_start} football season, the Houston Texans didn't exist"
                f"until 2002, this will lead to training on inactive franchises.")
        else:
            self._get_table(url, year_start)
            self._scrape_team_df(year_start + 1)

    def _get_table(self, url: str, year: int):
        # TODO: Although it's nice and clean now, it may make more sense to pass the team and year instead of URL so that
        #  the team and year can be on the dataframe as well.
        # req = requests.Session()
        req = HTMLSession()
        page = req.get(url, headers=self.header)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id=self.value_dict['table_id'])

        bet_body = bet_table.find('tbody')
        for row in bet_body.findAll('tr'):
            row = _get_row(row)
            row.insert(0, year)
            row = list(filter(lambda a: a != '', row))
            self.df.loc[len(self.df.index)] = row
