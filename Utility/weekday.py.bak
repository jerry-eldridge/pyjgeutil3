import time
from datetime import datetime
from math import floor
def weekday(year,month,day):
    s = '%d/%d/%d' % (year,month,day)
    print s,
    m = (month-3)%12 + 1
    Y = year
    d = day
    if (month == 1) or (month == 2):
        Y = Y - 1
    y = Y%100
    c = int(Y/100)
    days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    s = days[(d + int(floor(2.6*m-0.2)) + y + int(floor(y/4.0))+int(floor(c/4.0))-2*c)%7]
    return s
def Date(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def Seconds(year,month,day):
     sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
     return sec
