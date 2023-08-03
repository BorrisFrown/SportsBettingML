import constants
import os

from dataclass import DataClass

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
    # read_csv = False

    # stat_path = os.path.join(file_path, 'test_stats.csv')

    dataclass = DataClass()
    dataclass.get_all_team_data_from_file(start_year=2002)

    # bet_scraper = NflScraper(value_dict=constants.bet_dict, out_path=bet_path, team='cin', start_year=2020)
    # TODO: value_dict and directory should be mutually inclusive.
    # stat_scraper = NflScraper(value_dict=constants.stat_dict,
    #                           directory=stat_path,
    #                           team='crd',
    #                           from_csv=read_csv,
    #                           start_year=2020)
    # stat_scraper.write_to_csv(stat_path)
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
