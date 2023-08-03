import pandas as pd


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

#     TODO: Explore making these functions methods of webscrape.
