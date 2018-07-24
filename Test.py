
 

def mainz():
    import time
    import openpyxl
    import sys
    from openpyxl import Workbook
    import random
    import csv

    wb = openpyxl.load_workbook('/home/pmb/NetSpeedLogger/results.xlsx')
    ws = wb.active
    tme = time.strftime("%H:%M", time.gmtime())
    date = time.strftime("%b-%d", time.gmtime())

    try:
        import speedtest as sp
    except:
        fail_tuple = (date, tme, 0, 0, 0)
        ws.append(fail_tuple)
        wb.save('/home/pmb/NetSpeedLogger/results.xlsx')
        wb.close()
        sys.exit(69)

    try:
        res = sp.shell()
        dwn = round((res.download / 1000.0 / 1000.0), 2)
        up = round((res.upload / 1000.0 / 1000.0), 2)
        png = round(res.ping, 2)


    except:
        fail_tuple = (date, tme, 'FAIL', 'FAIL', 'FAIL')
        ws.append(fail_tuple)
        wb.save('/home/pmb/NetSpeedLogger/results.xlsx')
        wb.close()
        sys.exit()

    results = (date, tme, dwn, up, png)
    ws.append(results)
    wb.save('/home/pmb/NetSpeedLogger/results.xlsx')
    wb.close()
    
    with open('/home/pmb/NetSpeedLogger/Results.csv','a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(results)
        csv_file.close()

mainz()


