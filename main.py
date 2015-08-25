'''
Main program to run the interactive plot that dad wants.
'''

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

from fetch_historical_data import fetch

DATA_PATH = './data'

############
# PLOTTING #
############

def plot_relativity(index):
    '''
    The "relativity" (made that word up myself) of a stock index is defined
    as the % of its N stocks 0, ..., i, ..., N - 1, that, on a given day t,
    have prices greater than the N-day average of that stock. That is,

    R_t = count(p_{i,t} > mean(p_{i,t-1}, ... p_{i,t-N})) / N
        -- R_t = relativity on day t
        -- p_{i,t} = price of stock i on day t

    The main purpose of this program is to calculate and plot this index,
    as well as to be able to see the effect of predicting particular stock
    prices on the shape of the graph for the future.
    '''
    index = 'HUI'  # only HUI for now

##############
# Tkinter UI #
##############

class Application(tk.Frame):
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
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH)
        self.initLeftPanel()
        self.initRightPanel()

    def initLeftPanel(self):
        self.left_panel = LeftPanel(self, relief=tk.RAISED, borderwidth=1)
        self.left_panel.pack(side=tk.LEFT)

    def initRightPanel(self):
        self.right_panel = RightPanel(self, relief=tk.RAISED, borderwidth=1)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class LeftPanel(tk.Frame):
    '''
    Left panel of the application. Contains the main area on which to draw
    the graph.
    '''
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.init_graph()
        # self.draw_graph()

    def init_graph(self):
        self.figure = plt.Figure()  # TODO set size?

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # TODO resize_callbacks maybe
        self.canvas.get_tk_widget().pack()

    # TODO which index? parameters etc.
    def draw_graph(self):
        if self.master.right_panel.index.get() == 'HUI':
            subplot = self.figure.add_subplot(111)
            x = np.arange(0.0, 3.0, 0.01)
            y = np.sin(2 * 3.14 * x)
            subplot.plot(x, y)
            self.canvas.show()

class RightPanel(tk.Frame):
    '''
    Right panel of the application. Contains the configuration area, where
    you tweak the statistics that you want in the graph on the left.
    '''
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        # INDEX OPTION MENU
        tk.Label(self, text='Index:').grid(row=0, sticky=tk.W)
        self.index = tk.StringVar(self)
        self.index.set('HUI')
        tk.OptionMenu(self, self.index, 'HUI', 'None').grid(row=1, sticky=tk.W)

        # DRAW BUTTON
        button = tk.Button(self, text='Draw!',
                           command=self.master.left_panel.draw_graph)
        button.grid(row=2)


if __name__ == '__main__':
    # initiate Tkinter
    root = tk.Tk()
    root.geometry('1000x500')
    app = Application(root)

    # plot on Tkinter
    # loop
    root.attributes("-topmost", True)
    tk.mainloop()

    # cleanup
    root.destroy()
