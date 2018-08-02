
# coding: utf-8

# In[21]:


import csv
import matplotlib.dates as mdts
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pickle
get_ipython().run_line_magic('matplotlib', 'tk')

figure_location = '/home/pmb/NetSpeedLogger/FigureObject.fig.pickle'

def plotter(x, downloads, uploads):
    
    fig = plt.figure(figsize = (18,9))
    ax1 = plt.subplot2grid((2,1),(0,0), colspan=1, rowspan=1)
    ax2 = plt.subplot2grid((2,1),(1,0), colspan=1, rowspan=1)
    
    
    ax1.plot_date(x,downloads,'r.-',label='Download')
    ax1.set_xlabel('Time of Day')
    ax1.set_ylabel('Mb/s')
    ax1.legend(['Download'],loc=1,shadow=True)
    ax1.grid(True)
    
    ax2.plot_date(x, uploads, 'b.-',label='Upload')
    ax2.set_xlabel('Time of Day')
    ax2.set_ylabel('Mb/s')
    ax2.legend(['Upload'],loc=1,shadow=True)
    ax2.grid(True)
    
    fig.subplots_adjust(left=0.05, bottom=0.07, right=0.97, top=0.94, wspace=0.45,hspace=0.35)
    plt.show()
    
    pickle.dump(fig, open(figure_location,'wb'))
    
times, downloads, uploads, standardtimes = np.loadtxt('/home/pmb/NetSpeedLogger/ResultsPulled.csv',
                                                      delimiter=',',
                                                      unpack=True)


dateconv = np.vectorize(dt.datetime.fromtimestamp)
date = dateconv(times)
plotter(date, downloads, uploads)


# In[22]:


figure_location = '/home/pmb/NetSpeedLogger/FigureObject.fig.pickle'



