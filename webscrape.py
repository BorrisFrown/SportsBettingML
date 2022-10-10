import requests
import pandas as pd
import bs4

from datetime import date

# TODO: Perhaps write a class that inherits from the ML class with attributes such as this year and df and make all
#  these functions a part of that class.


def create_initial_df(url) -> pd.DataFrame:
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    bet_table = soup.find(id='vegas_lines')
    bet_columns = bet_table.find('thead').text.strip()
    col_names = list(bet_columns.split('\n'))
    df = pd.DataFrame(columns=col_names)
    return df


def get_this_football_season() -> int:
    today = date.today()
    if today.month <= 8:
        return today.year - 1
    elif today.month > 8:
        return today.year
    else:
        raise RuntimeError("Something is wrong with the datetime module")


def get_row(row: bs4.Tag) -> list:
    row_list = []
    for entry in row.findAll():
        if not entry.findAll():
            row_list.append(entry.text.strip())
    return row_list
#  TODO: Maybe also make an optional parameter of a [list] of row object names to leave out of the returned list


def get_table(url: str, df) -> pd.DataFrame:
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    bet_table = soup.find(id='vegas_lines')

    bet_body = bet_table.find('tbody')
    for row in bet_body.findAll('tr'):
        df.loc[len(df.index)] = get_row(row)
    return df


def get_team_df(year_start: int, df):# -> pd.DataFrame:
    bengals_url_root = f"https://www.pro-football-reference.com/teams/cin/"
    url = f"{bengals_url_root}{year_start}_lines.htm"
    if year_start == get_this_football_season():
        return get_table(url, df)
    elif year_start > get_this_football_season():
        raise IndexError("Trying to get a year for a football season that has not yet happened")
    elif year_start < 1966:
        raise IndexError("Trying to get a year for a football season before the superbowl, this may lead to unhelpful data")
    else:
        return pd.concat([get_table(url, df), get_team_df(year_start + 1, df)])

