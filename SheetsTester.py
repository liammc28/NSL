from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/NSL/client_secret.json',scope)
client = gspread.authorize(creds)
sheet = client.open('results').sheet1

download = 10
upload = 3
ping = 25
date = 'Yeet'
time = 'Skeet'

x = (date,time,download,upload,ping)
if (download or upload < 8) or (ping > 80):
    sheet.append_row(x)
