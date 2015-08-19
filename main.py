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
        self.pack()
        self.createWidgets()

    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

if __name__ == '__main__':
    # initiate Tkinter
    root = tk.Tk()
    app = Application(root)

    figure = plt.Figure(figsize=(5, 4), dpi=100)
    a = figure.add_subplot(111)
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * 3.14 * t)
    a.plot(t, s)
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # plot on Tkinter
    # loop
    tk.mainloop()

    # cleanup
    root.destroy()
