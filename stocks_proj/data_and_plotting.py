from api import api
from candlestick import pandas_candlestick_ohlc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl
import datetime

# showing all columns


desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',15)

#datetime
start = datetime.datetime(2017,1,1)
end = datetime.date.today()

#tickers_per_stocks
cd_ticker = 'CDPROJEKT'
plw_ticker = 'PLAYWAY'
bit_ticker = '11BIT'
wig20_ticker = "WIG20"


def get_data_CDR(ticker):
    cdr = quandl.get("WSE/" + ticker,start_date=start,end_date=end, paginate= True)
    return(cdr)


def get_data_PLW(ticker):
    plw = quandl.get("WSE/" + ticker,start_date=start,end_date=end, paginate= True)
    return(plw)


def get_data_BIT(ticker):
    bit = quandl.get("WSE/" + ticker, start_date=start, end_date=end, paginate = True)
    return(bit)


def get_data_WIG20(ticker):
    wig = quandl.get("WSE/" + ticker, start_date=start, end_date=end, paginate = True)
    return(wig)


def get_closing(cdr,plw,bit):
    stocks = pd.DataFrame({
        "CDR":cdr["Close"],
        "PLAYWAY":plw["Close"],
        "11BIT":bit["Close"]

    })
    return stocks


def get_stocks_return(stocks): # return = price_t/price_0
    stocks_return = stocks.apply(lambda x: x/x[0]) #lambda x is an anonymous function accepting parameter x
    return stocks_return -1


def get_stocks_change(stocks):
    stocks_change = stocks.apply(lambda x:np.log(x) - np.log(x.shift(1))) # dates back by 1
    return stocks_change


def adding_wig_closing(wig,stocks):
    wig20_data = pd.DataFrame({
        "WIG20":wig["Close"]
    })
    stocks_with_wig = stocks.join(wig20_data)
    return stocks_with_wig


def single_plot_data(x):
    x["Close"].plot(grid=True)


def plot_closings_all(stocks):
    stocks.plot(secondary_y = ['CDR','PLAYWAY'],grid=True)


def plot_stocks_return(stock_return):
    stock_return.plot(grid = True).axhline(y=1, color ="red", lw = 2) #axhline - horizontalline

def plot_stocks_change(stocks_change):
    stocks_change.plot(grid = True).axhline(y=0, color = "red", lw = 2)


cdr = get_data_CDR(cd_ticker)
plw = get_data_PLW(plw_ticker)
bit = get_data_BIT(bit_ticker)
wig = get_data_WIG20(wig20_ticker)

stocks = get_closing(cdr,plw,bit)
stocks_return = get_stocks_return(stocks)
stocks_change = get_stocks_change(stocks)

stocks_and_wig = adding_wig_closing(wig,stocks)
stocks_return_with_wig = get_stocks_return(stocks_and_wig)
stocks_change_with_wig = get_stocks_change(stocks_and_wig)


#print(cdr,plw,bit)
#print(stocks)
#print(stocks_return)
#print(stocks_change)
#print(stocks_and_wig)


#single_plot_data(cdr)
#plot_closings_all(stocks)

#plot_stocks_return(stocks_return)
#plot_stocks_change(stocks_change)

#plot with WIG20
#plot_stocks_return(stocks_return_with_wig)
#plot_stocks_change(stocks_change_with_wig)


#pandas_candlestick_ohlc(cdr, adj=True, stick="day")

plt.show()