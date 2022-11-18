import pandas as pd
import numpy as np
import os

import sklearn.model_selection
import sklearn.linear_model

from webscrape import NflScraper


def get_average_row(ave_data: list, row: list):
    # TODO: This could probably do all the row to int stuff as well
    week = row[0]
    new_ave = [week]
    start_idx = 1
    for idx, data in enumerate(row[start_idx:]):
        ave_point = (data + ave_data[idx + start_idx] * (week - 1)) / week
        new_ave.append(ave_point)
    return new_ave


def row_to_int(df, index):
    """ Takes a df and an index, and returns the row of the given index with the contents having been mapped to int"""
    def to_int(x: str):
        if x == ' ' or x == '':
            return 0
        else:
            return int(x)
    formatted_row = map(to_int, [df['Week'][index], df['Tm'][index], df['Opp'][index], df['1stD_o'][index], df['TotYd_o'][index],
                            df['PassY_o'][index], df['RushY_o'][index], df['TO_o'][index]])
    return list(formatted_row)


def formatted(df: pd.DataFrame) -> list[list]:
    last_year = 0
    data = []
    formatted_data = []
    for index in df.index:
        year = df['Year'][index]

        if df['Week'][index] == '1':
            average_data = row_to_int(df, index)
            formatted_data.append(list(average_data))
        # TODO: This is where it gets tough, I will have to get stats for every team and average them for the defense.

        else:
            average_data = get_average_row(average_data, row_to_int(df, index))
            formatted_data.append(average_data)
            # TODO: (CRUCIAL) ignore bye weeks and fix playoff divide by 0 error
            # TODO: Maybe add day, time, record, away

        last_year = year

    print(formatted_data)
#     TODO: Because there's so many functions, this may be able to be moved to another file or a method of webscrape
# TODO: I will either have to find a way to do deep learning, or go back to the original averaging idea
#

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

    # TODO: Put these guys somewhere cleaner

    url = "https://www.pro-football-reference.com/teams/cin/2019_lines.htm"
    bet_scraper = NflScraper(value_dict=bet_dict, team='cin', start_year=2020)
    stat_scraper = NflScraper(value_dict=stat_dict, team='cin', start_year=2020)

    # print(stat_scraper.df.columns)
    formatted(stat_scraper.df)

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
