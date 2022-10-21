import pandas as pd
import numpy as np
import os

import sklearn.model_selection
import sklearn.linear_model

from webscrape import NflScraper


def main():
    bet_dict = {'data': 'bets',
                'url_suffix': '_lines.htm',
                'table_id': 'vegas_lines'}

    stat_dict = {'data': 'stats',
                 'url_suffix': '.htm',
                 'table_id': 'games'}

    # TODO: Put these guys somewhere cleaner

    url = "https://www.pro-football-reference.com/teams/cin/2019_lines.htm"
    bet_scraper = NflScraper(value_dict=bet_dict, team='cin', start_year=2021)
    stat_scraper = NflScraper(value_dict=stat_dict, team='cin', start_year=2021)

    print(bet_scraper.df)

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
