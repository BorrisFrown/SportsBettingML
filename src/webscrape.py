import src.constants as constants
from src.loading_animation import Animation
from requests_html import HTMLSession
from datetime import date

import pandas as pd
import bs4
import os
import time
import calendar


# TODO: Make imports look nice.


def _html_row_to_list(row: bs4.Tag) -> list:
    """Given a soup tag, unpack the contents to a row."""
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
            url(str): The root pro-football-reference url.
            df (pd.DataFrame): The resulting dataframe from the scrape.
    """
    this_year = get_this_football_season()

    # TODO: Rename the misleading this_year to this_season

    def __init__(self,
                 value_dict: dict[str, str],
                 directory: str,
                 # TODO: Support nonetype directory
                 team: str = 'cin',
                 from_csv: bool = False,
                 start_year: int = 2002):
        self.value_dict = value_dict
        # TODO: There has got to be a better way to handle the dict, perhaps an init function to
        #  set self.value_dict based on the type of scraper
        self.directory = directory
        self.team = team
        self.from_csv = from_csv
        self.year = start_year

        self.url = self._get_url(NflScraper.this_year)
        self.header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,de;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1"
        }
        # TODO: Put this stuff in constants.py
        self.df = None
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
        url = self.url
        # TODO: Temporary hardcoded as bengals, make this dynamic
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
        """Scrapes the data from the internet if from_csv is False, otherwise, pulls the data from a csv"""
        if self.from_csv:
            self._get_from_csv()
            # TODO: (MORE URGENT) check the current date,
            #  and if the csv has an empty row before the current date, scrape it.

            # TODO: If the start date is before the date in the csv, offer to scrape that data
        else:
            print('Scraping data')
            ani = Animation()
            ani.start()
            self.df = self._initialize_df()
            self._scrape_team_df(self.year)
            ani.stop()

    def _scrape_team_df(self, year_start):
        """Recursively appends the given year's data to self.df.

        This method is also used any time additional years need to be appended to self.df given its recursive nature.

        Arg:
            year_start: The football season to scrape.
        """
        time.sleep(5)
        # TODO: Make the team an instance attribute
        url = self._get_url(year_start)
        # TODO: url should be an instance attribute

        if year_start == get_this_football_season():  # Base case
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
        # TODO: It makes more sense to pass the base url and year instead of the fully functional url
        # req = requests.Session()
        req = HTMLSession()
        page = req.get(url, headers=self.header)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id=self.value_dict['table_id'])
        try:
            bet_body = bet_table.find('tbody')
        except AttributeError:
            raise AttributeError(f"Error found in team {self.team}")

        for row_html in bet_body.findAll('tr'):
            row = _html_row_to_list(row_html)  # Gently down the stream
            row.insert(0, year)
            row = list(filter(lambda a: a != '', row))
            try:
                self.df.loc[len(self.df.index)] = row
            except ValueError:
                print(f"Omitting row: {row}")


    def _get_from_csv(self):
        full_csv_df = pd.read_csv(self.directory)
        desired_years_df = full_csv_df.loc[full_csv_df['Year'] >= self.year]
        desired_years_df.reset_index(inplace=True)
        self.df = desired_years_df.drop(columns='index')
        first_bad_year = self._first_outdated_year(self.df)
        if first_bad_year > 0:  # Set to > 0 because first_bad_year == -1 if it's up to date
            def pull_latest_input():
                scrape_input = input(
                    f"There is some missing data in this csv, would you like to pull the latest data?\n"
                    f"Type 'y' for yes or 'n' for no.")
                if scrape_input == 'n':
                    return False
                elif scrape_input == 'y':
                    return True
                print(f'Improper input: ({scrape_input}), please enter y or n.\n')
                pull_latest_input()

            if pull_latest_input():
                self.df = self.df[self.df['Year'] < first_bad_year]  # Removes any outdated seasons from self.df.
                self._scrape_team_df(first_bad_year)

    def _first_outdated_year(self, df) -> int:
        """Checks the df to see if there is an empty row that should not be empty given today's date.

       Arg:
           df: The dataframe to be tested.

       Returns:
           The earliest season with missing data or -1 if no missing data.
        """
        today = date.today()
        for idx in reversed(df.index):
            row_date = self._get_row_date(df.loc[idx])
            if row_date <= today and df.loc[idx]['Result'] == ' ':
                return df.loc[idx]['Year']
            elif row_date <= today and df.loc[idx]['Result'] != ' ':
                return -1

    @staticmethod
    def _get_row_date(df_row):
        row_month_day = df_row['Date']
        row_month_str = row_month_day.split(' ')[0]
        row_day = int(row_month_day.split(' ')[1])
        row_year = df_row['Year']
        row_month_int = list(calendar.month_abbr).index(row_month_str[:3])
        # This logic ensures a correct date because the 'Year' column actually indicates the season
        if row_month_int < 3:
            row_year += 1
        return date(row_year, row_month_int, row_day)

    def _get_url(self, year):
        base_url = constants.base_football_url
        url = f"{base_url}{self.team}/{year}{self.value_dict['url_suffix']}"
        return url
