import pandas as pd
import numpy as np
import os

import sklearn.model_selection
import sklearn.linear_model

from webscrape import NflScraper


def get_average_row(ave_data: list, row: list):
    week = row[0]
    new_ave = [week]
    start_idx = 1
    for idx, data in enumerate(row[start_idx:], start=start_idx):
        ave_point = (data + ave_data[idx] * (week - 1)) / week
        new_ave.append(ave_point)
    return new_ave


def row_to_int(df, index):
    """ Takes a df and an index, and returns the row of the given index with the contents having been mapped to int"""
    # TODO: Make this cleaner by passing column_list
    def to_int(x: str):
        if x == ' ' or x == '':
            return 0
        else:
            return int(x)

    try:
        # TODO: Use df.loc first to clean up the mess
        formatted_row = map(to_int, [df['Week'][index], df['Tm'][index],
                                     df['Opp'][index], df['1stD_o'][index],
                                     df['TotYd_o'][index], df['PassY_o'][index],
                                     df['RushY_o'][index], df['TO_o'][index]])
        return list(formatted_row)

    except ValueError:
        playoff_dict = {'Wild Card': 1,
                        'Division': 2,
                        'Conf. Champ.': 3,
                        'SuperBowl': 4}
        # TODO: If results are fucky for playoff games, instead of doing week number,
        #  find a way to feed a model a string or something
        week_str = df['Week'][index]
        week_num = int(df['Week'][index - (1 + playoff_dict[week_str])]) + playoff_dict[week_str]
        data_row = map(to_int, [df['Tm'][index], df['Opp'][index], df['1stD_o'][index], df['TotYd_o'][index],
                                df['PassY_o'][index], df['RushY_o'][index], df['TO_o'][index]])
        formatted_row = [week_num] + list(data_row)
        return formatted_row
#         TODO: Translate this to index - 1 or whatever it is


def formatted(df: pd.DataFrame) -> pd.DataFrame:
    last_year = 0
    average_data = []
    column_list = ['Week', 'Tm', 'Opp', '1stD_o', 'TotYd_o', 'PassY_o', 'RushY_o', 'TO_o']
    formatted_df = pd.DataFrame(columns=column_list)
    for index in df.index:
        year = df['Year'][index]
        if df['Week'][index] == '1':
            average_data = row_to_int(df, index)
            formatted_df.loc[len(formatted_df)] = average_data
        # TODO: This is where it gets tough, I will have to get stats for every team and average them for the defense.

        else:
            if df['Opp_name'][index] != 'Bye Week' and df['Opp_name'][index] != ' ':
                average_data = get_average_row(average_data, row_to_int(df, index))
                formatted_df.loc[len(formatted_df)] = average_data
            # TODO: Maybe add day, time, record, away
    return formatted_df

#     TODO: Because there's so many functions, this may be able to be moved to another file or a method of webscrape

# def get_target():
# def get_week_averages(df: pd.DataFrame) -> pd.DataFrame:
#     """Gets average stats of the season prior to the given week.
#
#     ALT: Returns a df of the average stats leading up to each week"""
#     for index in df.index:
#
#         print(df['Year'][index])

# TODO: Take the opposing team's averages as well instead


def main():
    bet_dict = {'data': 'bets',
                'url_suffix': '_lines.htm',
                'table_id': 'vegas_lines'}

    stat_dict = {'data': 'stats',
                 'url_suffix': '.htm',
                 'table_id': 'games'}

    team_dict = {'crd': 'Arizona Cardinals',
                 'atl': 'Atlanta Falcons',
                 'rav': 'Baltimore Ravens',
                 'buf': 'Buffalo Bills',
                 'car': 'Carolina Panthers',
                 'chi': 'Chicago Bears',
                 'cin': 'Cincinnati Bengals',
                 'cle': 'Cleveland Browns',
                 'dal': 'Dallas Cowboys',
                 'den': 'Denver Broncos',
                 'det': 'Detroit Lions',
                 'gnb': 'Green Bay Packers',
                 'htx': 'Houston Texans',
                 'clt': 'Indianapolis Colts',
                 'jax': 'Jacksonville Jaguars',
                 'kan': 'Kansas City Chiefs',
                 'rai': 'Las Vegas Raiders',
                 'sdg': 'Los Angeles Chargers',
                 'ram': 'Los Angeles Rams',
                 'mia': 'Miami Dolphins',
                 'min': 'Minnesota Vikings',
                 'nwe': 'New England Patriots',
                 'nor': 'New Orleans Saints',
                 'nyg': 'New York Giants',
                 'nyj': 'New York Jets',
                 'phi': 'Philadelphia Eagles',
                 'pit': 'Pittsburgh Steelers',
                 'sfo': 'San Francisco 49ers',
                 'sea': 'Seattle Seahawks',
                 'tam': 'Tampa Bay Buccaneers',
                 'oti': 'Tennessee Titans',
                 'was': 'Commanders'}
    # TODO: This should probably be in a json or literally anything better.

    file_path = os.path.dirname(os.path.realpath(__file__))
    bet_path = os.path.join(file_path, 'test_bets.csv')
    stat_path = os.path.join(file_path, 'test_stats.csv')

    # bet_scraper = NflScraper(value_dict=bet_dict, out_path=bet_path, team='cin', start_year=2020)
    stat_scraper = NflScraper(value_dict=stat_dict, directory=stat_path, team='cin', read_data=False, start_year=2020)
    stat_scraper.write_to_csv(stat_path)
    # ave_data = formatted(stat_scraper.df)
    pass

    # get_week_averages(stat_scraper.df, 1)

    # aapl_dir = "C:/Users/forre/OneDrive/Documents/Datasets/Stocks/AAPL.csv"
    # df = pd.read_csv(aapl_dir)
    #
    # predict_label = 'Close'
    # formatted_df = df.drop(columns='Date')
    #
    # data = np.array(formatted_df.drop(columns=predict_label))
    # target = np.array(formatted_df[predict_label])
    #
    # data_train, data_test, target_train, target_test = sklearn.model_selection.train_test_split(data, target, test_size=0.2)
    #
    # model = sklearn.linear_model.LinearRegression()
    #
    # model.fit(data_train, target_train)
    #
    # acc = model.score(data_test, target_test)
    #
    # print(acc)


main()
