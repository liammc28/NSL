<<<<<<< HEAD
import time
import openpyxl
import sys
import csv
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdts
import matplotlib




def plotter(utimes, uploads, downloads):
    conved_times = []
    
    dateconv = np.vectorize(dt.datetime.fromtimestamp)
    
    for i in utimes:
        i = round(float(i),-1)
        t = dateconv(i)
        conved_times.append(str(t))
    
    locator = mdts.AutoDateLocator()
    fmtter = mdts.AutoDateFormatter('%H:%M\n%a %d\n%b %y')
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((2,1),(0,0))
    ax2 = plt.subplot2grid((2,1),(1,0))
    
    ax1.plot_date(conved_times,downloads,'r-')
    plt.title = ("Internet Speed Report")
    ax1.ylabel = "Download"
    
    ax2.plot_date(conved_times, uploads, 'r-')
    ax2.ylabel = "Upload"
    
    fig.autofmt_xdate()
    plt.show()
    
    
def mainz():
    

    pcxlsx = '/home/pmb/NetSpeedLogger/results.xlsx'
    pccsv = '/home/pmb/NetSpeedLogger/Results.csv'
    
    
    wb = openpyxl.load_workbook(pcxlsx)
    ws = wb.active
    tme = time.strftime("%H:%M", time.gmtime())
    date = time.strftime("%b-%d", time.gmtime())
    unix_time = time.time()
    day_date = time.strftime("%y%m%d")

    try:
        import speedtest as sp
    except:
        fail_tuple = (date, tme, 0, 0, 0, unix_time, day_date)
        ws.append(fail_tuple)
        wb.save(pcxlsx)
        wb.close()
        sys.exit(69)

    try:
#        res = sp.shell()
#        dwn = round((res.download / 1000.0 / 1000.0), 2)
#        up = round((res.upload / 1000.0 / 1000.0), 2)
#        png = round(res.ping, 2)
        
        dwn = 9.99
        up = 3.33
        png = 69


    except:
        fail_tuple = (date, tme, 0, 0, 0, unix_time, day_date)
        ws.append(fail_tuple)
        wb.save(pcxlsx)
        wb.close()
        sys.exit()


    results = (date, tme, dwn, up, png, unix_time, day_date)
    
    ws.append(results)
    wb.save(pcxlsx)
    wb.close()
    
    with open(pccsv ,'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(results)
        csv_file.close()
        
    
    utimes = []
    downloads = []
    uploads = []
    lines=[]
    
    with open('/home/pmb/NetSpeedLogger/Results.csv' ,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for line in csv_reader:
            utimes.append(float(line[5]))
            downloads.append(float(line[2]))
            uploads.append(float(line[3]))
            
    
    plotter(utimes,uploads,downloads)
        
    

mainz()


=======

"""
Created on Mon Jul 30 15:34:04 2018

@author: pmb

NetSpeedLoggerBeta0.5
Main Application

Notes:
    *Cleaned code by using functions so it is more condensed now
    *New Feature: OS Detection- now the program detects whether it is running
     on RPi or PC to write to the correct directories

Planned Updates:
    *Google Sheets Database for online access to sheet format data
    *Daily upload/email of csv file for analysis 
    *Github 
"""

import os
import csv
import openpyxl
import sys
import time
import numpy as np
import datetime as dt

system = os.uname()
if system[1] == 'pmblaptop':
    #directory to write xlsx file
    xlsx_direc = '/home/pmb/NetSpeedLogger/NSLResults/results.xlsx'
    #directory to write xlsx info to csv
    csv_direc = '/home/pmb/NetSpeedLogger/NSLResults/Results.csv'
    #directory for plot format to be converted to so it can be pulled for analysis
    plotcsv = '/home/pmb/NetSpeedLogger/NSLResults/ResultsPulled.csv'
elif system[1] == 'raspberrypi':
    #directory to write xlsx file
    xlsx_direc = '/home/pi/NetSpeedLogger/results.xlsx'
    #directory to write xlsx info to csv
    csv_direc = '/home/pi/NetSpeedLogger/ResultsPulled.csv'
    #directory for plot format to be converted to so it can be pulled for analysis
    plotcsv = '/home/pi/NetSpeedLogger/ResultsPulled.csv'
else:
    print("Not programmed for this device, set up directories")
    sys.exit(-1)

standard_time = int(time.strftime('%y%m%d%H%M'))
tme = time.strftime("%H:%M", time.localtime())
date = time.strftime("%b-%d", time.localtime())
unix_time = time.time()
    
def SpeedTester():
    #attempt to import speedtest module, will log fail if fail occurs
    try:
        import speedtest as sp
        print()
    except:
        log_to_sheet = [date, tme, 0, 0, 0]
        log_to_csv = [unix_time, 0, 0, standard_time]

    try:
        res = sp.shell()
        dwn = round((res.download / 1000.0 / 1000.0), 2)
        up = round((res.upload / 1000.0 / 1000.0), 2)
        png = round(res.ping, 2)
        log_to_sheet = [date, tme, dwn, up, png]
        log_to_csv = [unix_time, dwn, up, standard_time]

    except:
        log_to_sheet = [date, tme, 0, 0, 0]
        log_to_csv = [unix_time, 0, 0, standard_time]
    return {'log_to_csv':log_to_csv, 'log_to_sheet':log_to_sheet}
        


def Writer(table_line, csv_line):
    #Excel
    wb = openpyxl.load_workbook(xlsx_direc)
    ws = wb.active
    ws.append(table_line)
    wb.save(xlsx_direc)
    wb.close()
    #CSVFile
    with open(csv_direc,'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(csv_line)
        csv_file.close()
    

def mainz():
    
    currentResults = SpeedTester()
    Writer(currentResults['log_to_sheet'],currentResults['log_to_csv'])
    
mainz()

>>>>>>> 8174f6c57c2147952ab714f0e5a757adc07c3f47
