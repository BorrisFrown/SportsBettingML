import src.constants as constants
import os
from webscrape import NflScraper


class DataClass:
    """Class for handling sports data."""
    def __init__(self, read_csv=True):
        self.read_csv = read_csv
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.bet_path = os.path.join(self.file_path, 'test_bets.csv')
        self.team_stat_dict = {}
    #     TODO: If read_csv is True, automatically run get_all_team_data_from_file

    def get_all_team_data_from_web(self, start_year=1989):
        self.read_csv = False
        for team in constants.team_dict.keys():
            stat_path = os.path.join(self.file_path, f'{team}.csv')
            self.team_stat_dict[team] = NflScraper(value_dict=constants.stat_dict,
                                                   directory=stat_path,
                                                   team=team,
                                                   from_csv=self.read_csv,
                                                   start_year=start_year)
            self.team_stat_dict[team].write_to_csv(stat_path)

    def get_all_team_data_from_file(self, start_year=1989):
        self.read_csv = True
        for team in constants.team_dict.keys():
            stat_path = os.path.join(self.file_path, f'{team}.csv')
            self.team_stat_dict[team] = NflScraper(value_dict=constants.stat_dict,
                                                   directory=stat_path,
                                                   team=team,
                                                   from_csv=self.read_csv,
                                                   start_year=start_year)

