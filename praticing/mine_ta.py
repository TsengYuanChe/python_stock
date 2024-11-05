import pandas as pd
def mine_add_all_features(df:pd.DataFrame):
    Hightest_high = df['High'].rolling(6).max()
    Lowest_low = df['Low'].rolling(6).min()
    O_C_high = df['High'].rolling(6).apply(lambda x : x[0]-x[-1])
    df['OCHIGH'] = O_C_high
    df['Hightest_high'] = Hightest_high
    df['Lowest_low'] = Lowest_low
    return df