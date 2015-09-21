'''
Main program to run the interactive plot that dad wants.
'''

###################
# TODO PRIORITIES #
###################
# -- properly control creation of graphs -> be able to clear, create new graphs
# -- access to reliable fetching mechanism (from Yahoo! finance)
# -- mouseover shows nearest-y data point
# -- choose date range (historic data)
# -- cleanup code
# -- not show random errors

import re
import glob
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg \
   import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# # implement the default mpl key bindings
# from matplotlib.backend_bases import key_press_handler

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import ttk
import ttk_calendar

from fetch_historical_data import fetch

UI_HEIGHT = 1000
UI_LENGTH = 1000
DATA_PATH = './data'

############
# PLOTTING #
############

STOCK_PRICES = {}

def calculate_relativity(index, window_len):
    '''
    The "relativity" (made that word up myself) of a stock index is defined
    as the % of its N stocks 0, ..., i, ..., N - 1, that, on a given day t,
    have prices greater than the M-day average of that stock. That is,

    R_t = count_N(p_{i,t} > mean(p_{i,t-1}, ... p_{i,t-M})) / N
        -- R_t = relativity on day t
        -- p_{i,t} = price of stock i on day t

    The main purpose of this program is to calculate and plot this index,
    as well as to be able to see the effect of predicting particular stock
    prices on the shape of the graph for the future.

    Returns a Pandas DataFrame, with dates as the DataFrame index and a
    column, 'Relativity', containing the relativity of the index.
    '''
    index = 'HUI'  # only HUI for now
    datatype = 'Close'
    M = window_len

    N = 0
    relativities = None  # TODO different dates
    for csv in glob.glob('%s/*.csv' % DATA_PATH):
        N += 1
        symbol = re.match(r'%s/([A-Z]+)\.csv' % DATA_PATH, csv).group(1)
        STOCK_PRICES[symbol] = prices = pd.DataFrame.from_csv(csv).iloc[::-1][datatype]
        if relativities is None:
            relativities = pd.DataFrame(index=prices.index)
        mean = pd.rolling_mean(prices, window=M)
        relativities[symbol] = (prices > mean).astype(int)

    # TODO handle merger that happened
    relativities = relativities.drop('AUQ', 1)
    index_relativity = relativities.sum(1) / N

    return (index_relativity.index, index_relativity)

##############
# Tkinter UI #
##############

class Application(ttk.Frame):
    '''
    The UI should look like this:
    ---------------------------------------------
    |                        |                  |
    |               /\       |                  |
    |          _ _ /  \      |                  |
    |         /        ---   |                  |
    |        /            \  |  OPTIONS         |
    |     /\/                |                  |
    |    /                   |                  |
    |   |                    |                  |
    |  /                     |                  |
    ---------------------------------------------
    '''
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH)
        self.config = {}
        self.initLeftPanel(self.config)
        self.initRightPanel(self.config)

    def initLeftPanel(self, config):
        self.left_panel = LeftPanel(self, config, relief=tk.RAISED, borderwidth=1)
        self.left_panel.pack(side=tk.LEFT)

    def initRightPanel(self, config):
        self.right_panel = RightPanel(self, config, relief=tk.RAISED, borderwidth=1)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class LeftPanel(ttk.Frame):
    '''
    Left panel of the application. Contains the main area on which to draw
    the graph.
    '''
    def __init__(self, master, config, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.config = config
        self.init_graph()
        # self.draw_graph()

    def init_graph(self):
        figsize = (UI_HEIGHT / 100. * 2 / 3, UI_LENGTH / 100.)
        self.figure = plt.Figure(dpi=100, figsize=figsize)
        self.subplot = self.figure.add_subplot(111)

        # TODO copy this part into draw graph
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # TODO resize_callbacks maybe
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_graph(self):
        index = self.config['index'].get()
        window_len = self.config['window_len'].get()
        if index == 'HUI':
            x, y = calculate_relativity(index, window_len)
            # TODO keep a list of current plots
            # TODO plot new graphs every time?
            self.subplot.plot(x, y)

            # rotate x-labels and fix margins
            plt.setp(self.subplot.get_xticklabels(), rotation=45)
            plt.margins(0.2)
            plt.subplots_adjust(bottom=0.15)

            self.canvas.show()

class RightPanel(ttk.Frame):
    '''
    Right panel of the application. Contains the configuration area, where
    you tweak the statistics that you want in the graph on the left.
    '''
    def __init__(self, master, config, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.config = config

        # INDEX OPTION MENU
        ttk.Label(self, text='Index:').grid(row=0, sticky=tk.W)
        index = self.config['index'] = tk.StringVar(self)
        index.set('HUI')
        omenu = ttk.OptionMenu(self, index, 'HUI', 'HUI', 'None')
        omenu.grid(row=1, sticky=tk.W)

        # WINDOW LENGTH
        ttk.Label(self, text='Window Length:').grid(row=2, column=0, sticky=tk.W)
        window_len = self.config['window_len'] = tk.IntVar(self)
        window_len.set(50)
        cbox = ttk.Combobox(self, textvariable=window_len,
                            values=[50, 100, 150], width=10)  # FIXME don't fix width
        cbox.grid(row=3, sticky=tk.W)
        ttk.Label(self, text='days').grid(row=3, column=1)

        # DRAW BUTTON
        button = ttk.Button(self, text='Draw!',
                           command=self.master.left_panel.draw_graph)
        button.grid(row=100)


if __name__ == '__main__':
    # initiate Tkinter
    root = tk.Tk()
    root.geometry('%dx%d' % (UI_HEIGHT, UI_LENGTH))
    app = Application(root)

    # lift UI to front, but not permanently
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)

    # plot on Tkinter
    # loop
    tk.mainloop()

    # cleanup
    root.destroy()
