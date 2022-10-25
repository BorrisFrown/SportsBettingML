import requests
import pandas as pd
import bs4

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

    def __init__(self, value_dict: dict[str, str], team: str = 'cin', start_year: int = 1990):
        self.value_dict = value_dict
        # TODO: There has got to be a better way to handle the dict, perhaps an init function to
        #  set self.value_dict based on the type of scraper
        self.team = team
        self.start_year = start_year

        self.root_url = "https://www.pro-football-reference.com/teams/"
        # TODO: Perhaps I don't need to hardcode this url
        self.df = self._initialize_df()

        self._get_team_df(self.start_year)
    #     TODO: Instead of doing very similar but different functions, these should maybe be different instances of
    #      the web scraper class.

    def _initialize_df(self) -> pd.DataFrame:
        """Initializes an empty DataFrame with web-scraped columns.

            Arg:
                type_of_data (str): The string indicating the type of data you want.

            Returns:
                df (pd.DataFrame): Empty dataframe with scraped columns.
        """
        url = f"{self.root_url}cin/{NflScraper.this_year}{self.value_dict['url_suffix']}"
        # TODO: Temporary hardcoded as bengals, make this dynamic
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id=self.value_dict['table_id'])
        bet_columns = bet_table.find('thead')#.text.strip()
        bet_columns = bet_columns.find_all('tr')[-1].text.strip()
        col_names = list(bet_columns.split('\n'))
        if self.value_dict['data'] == 'stats':
            col_names[3] = 'Time'
            col_names[4] = 'Boxscore'
            col_names[5] = 'Result'
            col_names[8] = 'Away'
            # col_names.insert(3, 'Time')
            # col_names.insert(4, 'Boxscore')
            # # TODO: Boxscore is a placeholder, this whole column and data needs to be deleted
            # col_names.insert(5, 'Result')
            # col_names.insert(8, 'Away')
        col_names.insert(0, 'Year')
        col_names = list(filter(lambda a: a != '', col_names))
        # TODO: Fix this
        df = pd.DataFrame(columns=col_names)
        return df

    def _get_team_df(self, year_start):
        # TODO: docstring mention recursion

        bengals_url_root = f"{self.root_url}cin/"
        # TODO: Make the team an instance attribute
        url = f"{bengals_url_root}{year_start}{self.value_dict['url_suffix']}"

        if year_start == get_this_football_season():        # Base case
            self._get_table(url, year_start)
        elif year_start > get_this_football_season():
            raise IndexError(
                f"Trying to get a dataframe for a football season that has not yet happened ({year_start})")
        elif year_start < 1966:
            raise IndexError(
                f"Trying to get a dataframe for the {year_start} football season, the first superbowl was in "
                f"1966. This will lead to unhelpful data.")
        else:
            self._get_table(url, year_start)
            self._get_team_df(year_start + 1)

    def _get_table(self, url: str, year: int):
        # TODO: Although it's nice and clean now, it may make more sense to pass the team and year instead of URL so that
        #  the team and year can be on the dataframe as well.
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id=self.value_dict['table_id'])

        bet_body = bet_table.find('tbody')
        for row in bet_body.findAll('tr'):
            row = _get_row(row)
            row.insert(0, year)
            row = list(filter(lambda a: a != '', row))
            self.df.loc[len(self.df.index)] = row
