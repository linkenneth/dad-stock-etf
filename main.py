'''
Main program to run the interactive plot that dad wants.
'''

###################
# TODO PRIORITIES #
###################
# -- properly control creation of graphs -> be able to clear, create new graphs (DONE)
# -- legend, and list of current plots (DONE)
# -- access to reliable fetching mechanism (from Yahoo! finance)
# -- reliable calculations
# -- mouseover shows nearest-y data point
# -- choose date range (historic data) (make this crude! just type in)
# -- cleanup code
# -- fail gracefully (eg. when no data)

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
import tkintertable

from fetch_historical_data import fetch

UI_HEIGHT = 1000
UI_WIDTH = 1500
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
        self.current_plots = {}  # dict of label : (x, y)

    def init_graph(self):
        figsize = (UI_WIDTH / 100. * 0.6, UI_HEIGHT / 100.)
        self.figure = plt.Figure(dpi=100, figsize=figsize)
        self.subplot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # TODO resize_callbacks maybe
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # TODO make toolbar work
        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_graph(self):
        index = self.config['index'].get()
        window_len = self.config['window_len'].get()
        if index == 'HUI':
            x, y = calculate_relativity(index, window_len)
            label = '%s %s-day %s' % (index, window_len, 'relativity')
            if label in self.current_plots:
                return

            self.current_plots[label] = (x, y)
            self.config['table'].addRow(label, **{
                'Index': index,
                'Statistic': 'relativity',
                'Window Length': window_len
            })

            self.config['message'].config(text='Plotting graph...')
            self.subplot.plot(x, y, label=label)
            self.subplot.legend()

            # rotate x-labels and fix margins
            plt.setp(self.subplot.get_xticklabels(), rotation=45)
            plt.margins(0.2)
            plt.subplots_adjust(bottom=0.15)

            self.config['message'].config(text='Done.')
            self.canvas.show()

    def clear_graph(self):
        self.current_plots = {}
        self.subplot.cla()
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

        # TABLE VIEW OF CURRENT PLOTS
        tframe = tk.Frame(self)
        tframe.grid(row=99, columnspan=3, sticky=tk.W+tk.E, in_=self)
        table = self.config['table'] = \
          tkintertable.TableCanvas(tframe, width=450, rows=0, cols=0)
        table.createTableFrame()
        table.addColumn('')  # checkbox + color
        table.addColumn('Index')
        table.addColumn('Statistic')
        table.addColumn('Window Length')

        # PLOT BUTTON
        button = ttk.Button(self, text='Plot',
                           command=self.master.left_panel.draw_graph)
        button.grid(row=100, column=0)

        # CLEAR BUTTON
        button = ttk.Button(self, text='Clear',
                           command=self.master.left_panel.clear_graph)
        button.grid(row=100, column=1)

        # CLEAR BUTTON
        button = ttk.Button(self, text='Fetch Data!',
                           command=fetch)
        button.grid(row=100, column=2)

        # NOTIFICATIONS
        message = tk.Message(self, text='')
        message.grid(row=101, columnspan=3, sticky=tk.W+tk.E)
        self.config['message'] = message


if __name__ == '__main__':
    # initiate Tkinter
    root = tk.Tk()
    root.geometry('%dx%d' % (UI_WIDTH, UI_HEIGHT))
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
