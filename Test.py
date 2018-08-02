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


