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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

system = os.uname()
if system[1] == 'pmblaptop':
    #directory for json gspread file
    json_direc = '/home/pmb/NSL/client_secret.json'
    #directory to write xlsx file
    xlsx_direc = '/home/pmb/NSL/Results/results.xlsx'
    #directory to write xlsx info to csv
    csv_direc = '/home/pmb/NSL/Results/ResultsPulled.csv'
    #directory for plot format to be converted to so it can be pulled for analysis
    plotcsv = '/home/pmb/NSL/Results/ResultsPulled.csv'
elif system[1] == 'raspberrypi':
    #directory for json gspread file
    json_direc = '/home/pi/NSL/client_secret.json'
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
    try:
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_direc,scope)
        client = gspread.authorize(creds)
        sheet = client.open('NSL-Duds').sheet1
        download = table_line[2]
        upload = table_line[3]
        ping = table_line[4]
	sheet.append_row(table_line)
    except:
        print("oops!")

def Emailer(table_line):
    try:
        
        download = table_line[2]
        upload = table_line[3]
        ping = table_line[4]
        results_tuple = (download, upload, ping)
        
        email_sender = 'paulmcbrien99@gmail.com'
        email_receiver = 'paulmcbrien10@gmail.com'
        PASSWORD = 'cotton10'
        subject = "Internet Speed Warning"

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        msg.attach
        body = ("Well Dad, what's the craic!\n \n \tDownload is %.2fMb/s\n \tUpload is %.2fMb/s\n \tPing is %.2fms \n \n \nPlease check with your internet service provider" % (results_tuple))
        msg.attach(MIMEText(body,'plain'))
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(email_sender,PASSWORD)
        server.sendmail(email_sender,email_receiver,text)
        server.sendmail(email_sender,'anthonymcbrien67@gmail.com',text)
        #server.sendmail(email_sender,'paulinemcbrien66@gmail.com',text)
        server.quit() 
    except:
        print("Whoah!")

def mainz():
    
    currentResults = SpeedTester()
    Writer(currentResults['log_to_sheet'],currentResults['log_to_csv'])
    
    dates = currentResults['log_to_sheet']
    
    print(dates)

    if (dates[2] < 3) or (dates[3] < 3):
        GoogleSheetsLogger(currentResults['log_to_sheet'])
        Emailer(currentResults['log_to_sheet'])

mainz()


