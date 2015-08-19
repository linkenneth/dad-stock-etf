'''
Plots the % of HUI companies that are above or below the N-day moving
average.
'''

import re
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

N = 50
stock_count = 0
FIELD = 'Close'
dfs = {}
means = {}
relativities = {}

for csv in glob.glob('data/*.csv'):
    stock_count += 1
    stock_name = re.match(r'data/([A-Z]+)\.csv', csv).group(1)
    dfs[stock_name] = df = pd.DataFrame.from_csv(csv)[FIELD]
    reversed_df = df.iloc[::-1]
    means[stock_name] = mean = pd.rolling_mean(reversed_df, window=N)
    relativities[stock_name] = (reversed_df > mean).astype(int)

if __name__ == '__main__':
    relativity = pd.DataFrame(0.0, index=reversed_df.index,
                              columns=['Relativity'], dtype=float)
    for stock_name, r in relativities.items():
        # TODO handle merger
        if stock_name == 'AUQ':
            continue
        relativity += r

    relativity.plot()
    plt.show()
