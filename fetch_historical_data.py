import os
import glob
import urllib
from datetime import datetime

HUI_STOCKS = [
    'ABX'  ,  # NYSE : Barrick Gold
    'GG'   ,  # NYSE : Goldcorp
    'NEM'  ,  # NYSE : Newmont Mining
    'AEM'  ,  # NYSE : Agnico Eagle Mines
    'BVN'  ,  # NYSE : Compania de Minas Buenaventura
    'SBGL' ,  # NYSE : Sibanye Gold Limited
    'AU'   ,  # NYSE : AngloGold Ashanti
    'GOLD' ,  # NASDAQ : Randgold Resources
    'KGC'  ,  # NYSE : Kinross Gold
    'BTG'  ,  # NYSE : B2Gold Corp
    'AUQ'  ,  # NYSE : AuRico Gold
    'AUY'  ,  # NYSE : Yamana Gold
    'EGO'  ,  # NYSE : Eldorado Gold Corp
    'NGD'  ,  # NYSE : New Gold Inc
    'AGI'  ,  # NYSE : Alamos Gold Inc
    'HMY'  ,  # NYSE : Harmony Gold Mining
    'GFI'  ,  # NYSE : Gold Fields Limited
    'IAG'  ,  # NYSE : Iamgoldcorp
]

BASE_URL = 'http://ichart.yahoo.com/table.csv?s='
START_DATE = datetime(2010, 01, 01)
END_DATE = datetime.today()

if __name__ == '__main__':
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
