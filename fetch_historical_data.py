# Downloads price data for HUI stocks from Yahoo! Finance.
#
# See
# https://code.google.com/p/yahoo-finance-managed/wiki/csvHistQuotesDownload
# for details

import os
import glob
import urllib
from datetime import datetime

from common import HUI_STOCKS

BASE_URL = 'http://ichart.yahoo.com/table.csv?s='
START_DATE = datetime(2012, 01, 01)
END_DATE = datetime.today()

def fetch():
    for stock in HUI_STOCKS:
        file_name = 'data/%s.csv' % stock
        if not glob.glob(file_name):
            start_date = START_DATE
            end_date = END_DATE
        else:
            # TODO read file and find last start date, then do append
            start_date = START_DATE
            end_date = END_DATE

        url = BASE_URL + stock
        url += '&a={0}&b={1}&c={2}'.format(start_date.month - 1,
                                           start_date.day, start_date.year)
        url += '&d={0}&e={1}&f={2}'.format(end_date.month - 1,
                                           end_date.day, end_date.year)
        url += '&g=d&ignore=.csv'  # daily frequency and ignore .csv
        print 'Fetching from << {} >>...'.format(url)

        with open(file_name, 'w+') as f:
            f.write(urllib.urlopen(url).read())

if __name__ == '__main__':
    fetch()
