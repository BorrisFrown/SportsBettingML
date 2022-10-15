import requests
import pandas as pd
import bs4

from datetime import date


def _get_row(row: bs4.Tag) -> list:
    row_list = []
    for entry in row.findAll():
        if not entry.findAll():
            row_list.append(entry.text.strip())
    return row_list
#  TODO: Maybe also make an optional parameter of a [list] of row object names to leave out of the returned list


def _get_table(url: str, df, year) -> pd.DataFrame:
    # TODO: Although it's nice and clean now, it may make more sense to pass the team and year instead of URL so that
    #  the team and year can be on the dataframe as well.
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    bet_table = soup.find(id='vegas_lines')

    bet_body = bet_table.find('tbody')
    for row in bet_body.findAll('tr'):
        row = _get_row(row)
        row.insert(1, year)
        df.loc[len(df.index)] = row
    return df


def _get_team_bet_df(year_start: int, df) -> pd.DataFrame:
    bengals_url_root = f"https://www.pro-football-reference.com/teams/cin/"
    url = f"{bengals_url_root}{year_start}_lines.htm"
    if year_start == get_this_football_season():
        return _get_table(url, df, year_start)
    elif year_start > get_this_football_season():
        raise IndexError(f"Trying to get a dataframe for a football season that has not yet happened ({year_start})")
    elif year_start < 1966:
        raise IndexError(f"Trying to get a dataframe for the {year_start} football season, the first superbowl was in "
                         f"1966. This will lead to unhelpful data.")
    else:
        _get_table(url, df, year_start)
        return _get_team_bet_df(year_start + 1, df)


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

        Attributes:
            team (str): A small string correlating with what is accepted by pro-football-reference url.
            this_year(int): Takes the result of get_this_football_season() [NOT ALWAYS THIS CALENDAR YEAR].
            root_url(str): The root pro-football-reference url.
            bet_df (pd.DataFrame): The resulting dataframe from the scrape.

        Methods:
            TODO: We'll fill this in when the scraper is a bit more complete.

    """
    def __init__(self, team: str = 'cin', start_year: int = 1990):
        self.team = team
        self.start_year = start_year
        self.bet_df = None
        self.stat_df = None

        self.this_year = get_this_football_season()
        self.root_url = "https://www.pro-football-reference.com/teams/"
        # TODO: Perhaps I don't need to hardcode this url

        self.bet_df = self._initialize_df('bets')
        self.stat_df = self._initialize_df('stats')
        self._set_team_bet_df()
        # self._set_team_stat_df()

    def _initialize_df(self, type_of_data: str) -> pd.DataFrame:
        """Initializes an empty DataFrame with web-scraped columns.

            Arg:
                type_of_data (str): The string indicating the type of data you want.

            Returns:
                df (pd.DataFrame): Empty dataframe with scraped columns.
        """
        allowed_data = ['bets', 'stats']
        if type_of_data not in allowed_data:
            raise ValueError(f'Trying to get a dataframe for {type_of_data}, must be one of {allowed_data}.')
        if type_of_data == 'bets':
            suffix = '_lines.htm'
            # TODO: Hardcode the .htm so I don't need the redundant suffix
            table_id = 'vegas_lines'
        elif type_of_data == 'stats':
            suffix = '.htm'
            table_id = 'games'
        else:
            raise NotImplementedError(f'NFLScraper cannot yet handle {type_of_data} data. \n'
                                      f'Remove it from "allowed_data" or implement how to handle it.')
        # TODO: Put ^this^ chunk of logic in its own function

        url = f'{self.root_url}cin/{self.this_year}{suffix}'
        # TODO: Temporary hardcoded as bengals, make this dynamic
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id=table_id)
        bet_columns = bet_table.find('thead').text.strip()
        col_names = list(bet_columns.split('\n'))
        col_names.insert(1, 'Year')
        df = pd.DataFrame(columns=col_names)
        return df

    def _set_team_bet_df(self):
        self.bet_df = _get_team_bet_df(self.start_year, self.bet_df)

    def _set_team_stat_df(self):
        # TODO: Implement
        raise NotImplementedError
