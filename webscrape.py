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


def _get_team_df(year_start: int, df) -> pd.DataFrame:
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
        return _get_team_df(year_start + 1, df)


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
            df (pd.DataFrame): The resulting dataframe from the scrape.

        Methods:
            TODO: We'll fill this in when the scraper is a bit more complete.

    """
    def __init__(self, team: str = 'cin'):
        self.team = team

        self.this_year = get_this_football_season()
        self.root_url = "https://www.pro-football-reference.com/teams/"
        # TODO: Perhaps I don't need to hardcode this url

        self.df = self._initialize_df()  # This will initial

    def _initialize_df(self):
        url = f'{self.root_url}cin/{self.this_year}_lines.htm'
        # TODO: Temporary hardcoded as bengals, make this dynamic
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        bet_table = soup.find(id='vegas_lines')
        bet_columns = bet_table.find('thead').text.strip()
        col_names = list(bet_columns.split('\n'))
        col_names.insert(1, 'Year')
        df = pd.DataFrame(columns=col_names)
        return df

    def set_team_df(self, start_year: int = 2000):
        self.df = _get_team_df(start_year, self.df)
