
import constants
import numpy as np
import os

import sklearn.model_selection
import sklearn.linear_model

from webscrape import NflScraper
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

    # TODO: This should probably be in a json or literally anything better.

    file_path = os.path.dirname(os.path.realpath(__file__))
    bet_path = os.path.join(file_path, 'test_bets.csv')
    stat_path = os.path.join(file_path, 'test_stats.csv')

    # bet_scraper = NflScraper(value_dict=constants.bet_dict, out_path=bet_path, team='cin', start_year=2020)
    stat_scraper = NflScraper(value_dict=constants.stat_dict, directory=stat_path, team='cin', read_data=False, start_year=2020)
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
