import numpy as np
import quandl
import datetime
from data_and_plotting import end
from candlestick import pandas_candlestick_ohlc

start= datetime.datetime(2015, 1, 1)
end = datetime.datetime(2020,4,16)

def older_stock_data(ticker):
    stock = quandl.get("WSE/" + ticker, start_date=start, end_date=end)
    return stock

def get_one_month_average(stocks,window):
    avg_month = np.round(stocks["Close"].rolling(window=window, center= False).mean(),2)
    return avg_month


cdr = older_stock_data("PLAYWAY")

cdr["20d"] = get_one_month_average(cdr,20)
cdr["50d"] = get_one_month_average(cdr,50)
cdr["200d"] = get_one_month_average(cdr,200)



pandas_candlestick_ohlc(cdr.loc["2017-01-02":"2020-04-09",:], otherseries=["20d","50d","200d"],adj=True)