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
import gspread 
from oauth2client.service_account import ServiceAccountCredentials

system = os.uname()
if system[1] == 'pmblaptop':
    #directory to write xlsx file
    xlsx_direc = '/home/pmb/NSL/Results/results.xlsx'
    #directory to write xlsx info to csv
    csv_direc = '/home/pmb/NSL/Results/ResultsPulled.csv'
    #directory for plot format to be converted to so it can be pulled for analysis
    plotcsv = '/home/pmb/NSL/Results/ResultsPulled.csv'
elif system[1] == 'raspberrypi':
    #directory to write xlsx file
    xlsx_direc = '/home/pi/NSL/Results/results.xlsx'
    #directory to write xlsx info to csv
    csv_direc = '/home/pi/NSL/Results/ResultsPulled.csv'
    #directory for plot format to be converted to so it can be pulled for analysis
    plotcsv = '/home/pi/NSL/Results/ResultsPulled.csv'
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
        
        
def GoogleSheetsLogger(table_line):
    '''Logs bad results to google sheets document'''

    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pmb/NSL/client_secret.json',scope)
    client = gspread.authorize(creds)
    sheet = client.open('results').sheet1
    
    download = table_line[2]
    upload = table_line[3]
    ping = table_line[4]
    
    if (download or upload < 8) or (ping > 80):
        sheet.append_row(table_line)


def mainz():
    
    currentResults = SpeedTester()
    Writer(currentResults['log_to_sheet'],currentResults['log_to_csv'])
    GoogleSheetsLogger(currentResults['log_to_sheet'])
    
mainz()


