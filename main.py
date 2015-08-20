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

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.initLeftPanel()
        self.initRightPanel()

    def initLeftPanel(self):
        self.left_panel = LeftPanel(self, relief=tk.RAISED, borderwidth=1)
        self.left_panel.pack(side=tk.LEFT)

    def initRightPanel(self):
        self.right_panel = RightPanel(self, relief=tk.RAISED, borderwidth=1,
                                      width=340)
        self.right_panel.pack(side=tk.LEFT, fill=tk.Y)

class LeftPanel(tk.Frame):
    '''
    Left panel of the application. Contains the main area on which to draw
    the graph.
    '''
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.draw_graph()

    def draw_graph(self):
        figure = plt.Figure(figsize=(7, 6), dpi=100)
        a = figure.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * 3.14 * t)
        a.plot(t, s)

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class RightPanel(tk.Frame):
    '''
    Right panel of the application. Contains the configuration area, where
    you tweak the statistics that you want in the graph on the left.
    '''
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master


if __name__ == '__main__':
    # initiate Tkinter
    root = tk.Tk()
    root.geometry('1200x600+300+300')
    app = Application(root)

    # plot on Tkinter
    # loop
    root.attributes("-topmost", True)
    tk.mainloop()

    # cleanup
    root.destroy()
