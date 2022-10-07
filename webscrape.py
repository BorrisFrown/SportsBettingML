import requests
import pandas as pd
import bs4


def get_row(row: bs4.Tag) -> list:
    row_list = []
    for entry in row.findAll():
        if not entry.findAll():
            row_list.append(entry.text.strip())
    return row_list
#  Maybe also make an optional parameter of a [list] of row object names to leave out of the returned list


def nfl_web_scrape():
    url = "https://www.pro-football-reference.com/teams/cin/2019_lines.htm"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    bet_table = soup.find(id='vegas_lines')
    bet_columns = bet_table.find('thead').text.strip()
    col_names = list(bet_columns.split('\n'))

    bet_body = bet_table.find('tbody')

    df = pd.DataFrame(columns=col_names)

    for row in bet_body.findAll('tr'):
        data_row = get_row(row)
        df.loc[len(df.index)] = get_row(row)
    print(df)

