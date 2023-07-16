import security_agency3 as sa_m
import agent_bureau3 as ab_m
import stock3 as sk_m
import consumer3 as cmr_m

import time
from datetime import datetime

def Date(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def YYMMDD(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d')

def Seconds(year,month,day):
     sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
     return sec

SA = sa_m.Security_Agency()
encode = SA.get_encode()

##currency = 1
##A = 1 * currency
##B = 10 * currency
##C = 100 * currency

pwd_AB = "AB_secret_3"
AB = ab_m.Agent_Bureau(0, SA, pwd_AB, 0,
               domain='A')
enc_pwd_AB = encode(pwd_AB)

pwd_AA1 = "AA1_secret_3"
key_AA1 = AB.open_agency(enc_pwd_AB,
                pwd_AA1,"AA1",
               domain='A')
enc_AA1_pwd = encode(pwd_AA1)

pwd_AA2 = "AA2_secret_3"
key_AA2 = AB.open_agency(enc_pwd_AB,
                pwd_AA2,"AA2",
               domain='B')
enc_AA2_pwd = encode(pwd_AA2)

pwd_AA3 = "AA2_secret_3"
key_AA3 = AB.open_agency(enc_pwd_AB,
                pwd_AA3,"AA3",
               domain='C')
enc_AA3_pwd = encode(pwd_AA3)

# open an accounts at Account_Agency A
name0 = "cash"
pwd0 = "0_secret_3_cash"
amount0 = 0.00

name1 = "FAKE_TKR_1"
pwd1 = "1_secret_3_fake"
amount1 = 1000.0

name2 = "FAKE_TKR_2"
pwd2 = "2_secret_3_fake"
amount2 = 1000.0

name3 = "FAKE_C1"
pwd3 = "3_secret_3_fake"
amount3 = 10000.00

key0 = AB.open_account(enc_pwd_AB,enc_AA1_pwd,
            key_AA1, pwd0, name0, amount0)
key1 = AB.open_account(enc_pwd_AB,enc_AA1_pwd,
            key_AA1, pwd1, name1, amount1)
key2 = AB.open_account(enc_pwd_AB,enc_AA1_pwd,
            key_AA1, pwd2, name2, amount2)
key3 = AB.open_account(enc_pwd_AB,enc_AA3_pwd,
            key_AA3, pwd3, name3, amount3)

print(AB)

def to_sig(AB,agency_id, account_id):
     sig = AB.get_signature(agency_id, account_id)
     return sig
def to_msg(key1, key2, amount, desc):
     s = f"{key1}!{key2};{amount};{desc}"
     return s
def tx(pwd1, key1, key2, amount, desc):
     msg = to_msg(key1, key2, amount, desc)
     AB.transaction(enc_pwd_AB, pwd1, msg, False)
     #print(AB)
     return

##tx(pwd1, key1, key2, 1.00, "1")
##tx(pwd2, key2, key0, 1.00, "2")
##tx(pwd0, key0, key3, 1.00, "3")
##tx(pwd3, key3, key1, 1.00, "4")
##print(AB.report())


secs0 = Seconds(2023,6,1) # now

t_now = 0
year0 = 1
period0 = 4 # four quarterly periods
dt0 = year0/period0
# Arbitrary dval0. Approximate say by use change
# in stock price in a day as high - low. This suppose
# was the change per day. One unit of time is one
# quarter so the change per quarter suppose was dt0*(high-low)
# but this will not be accurate. 
high1,low1 = 335.23 , 327.59
high2,low2 = 155.50 , 154.32
dval0_1 = dt0*(high1 - low1) # change in stock price per period
dval0_2 = dt0*(high2 - low2) # change in stock price per period

minute_real = 60 # seconds
hour_real = 60*minute_real
day_real = 24*hour_real
year_real = 365*day_real
dt0_real = (year_real * dt0)
current_yield = 0.81 # annual percent

# p0 determines martingale, sub-martingale,
# or super-martingale perhaps for this.
# but it depends on actual plot.
p0 = 0.7 # probability value in [0,1] arbitrary

# [1] https://www.nasdaq.com/
# two example NASDAQ stock market stocks are:
# [2] https://www.nasdaq.com/market-activity/stocks/msft
# [3] https://www.nasdaq.com/market-activity/stocks/wmt
M = [
    sk_m.Stock(
          AB,enc_pwd_AB,
          key1,
          key0,
          t_now,
          ticker_symbol=name1,
          stock_price=327.59,
          period=period0,current_yield=0.81,
          p=p0,
          volatility=dval0_1,
          pwd = pwd1,
          ),
    sk_m.Stock(
          AB,enc_pwd_AB,
          key2,
          key0,
          t_now,
          ticker_symbol=name2,
          stock_price=154.32,
          period=period0,
          current_yield=1.49,
          p=p0,
          volatility=dval0_2,
          pwd = pwd2,
          ),    
    ]

S = [M[0],M[1]]
Q = [0, 0]
O = []

C1 = cmr_m.Consumer(
          AB,enc_pwd_AB,
          key3, # C1
          key0, # cash
          S,Q,O,
          max_options=3,
          pwd = pwd3)#pwd3)

N_years = 5
N = period0*N_years
C = [C1]

for t in range(N):
    secs = secs0 + t*dt0_real
    print("*"*40)
    s = f"t={t}, date= {Date(secs)}"
    print(s)
    print("*"*40)
    # display Account Agency accounts
    print(AB)
    
    # display Portfolio i
    for i in range(len(C)):
        print(f"{C[i]}")
        s_names = C[i].get_portfolio().stock_names()
        C[i].strategize(["FAKE_MSFT"],
            expires=4,budget=1000.00,
            price_option=327.59,
            wealth_thresh=2000.0) # previous day
        C[i].strategize(["FAKE_WMT"],
            expires=4,
            budget=1000.00,
            price_option=154.32,
            wealth_thresh=2000.0) # previous day
        C[i].sim_step() # after day
    # sim_step the market
    for i in range(len(M)):
        M[i].sim_step()

s = AB.report()
print(s)

