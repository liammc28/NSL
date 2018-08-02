#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 18:39:46 2018

@author: pmb
"""
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pmb/NetSpeedLogger/client_secret.json',scope)
client = gspread.authorize(creds)

ws = client.open('NSLSheet').worksheet('1')

with open('/home/pmb/NetSpeedLogger/NSLResults/ResultsPulled.csv','r') as cf:
    cr = csv.reader(cf)
    next(cr)
    
    for line in cr:
        ws.append_row(line)
        


    
    
    