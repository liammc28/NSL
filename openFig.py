import csv
import matplotlib.dates as mdts
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pickle
import time

figure_location = '/home/pmb/NetSpeedLogger/FigureObject.fig.pickle'

figx = pickle.load(open(figure_location,'rb'))
figx.show()
plt.show()
time.sleep(10)
