import numpy as np
import pandas as pd
from moving_average import cdr, older_stock_data

cdr = cdr

#backtesting
cdr["20d-50d"] = cdr["20d"] - cdr["50d"]
cdr["Buy/Sell"] = np.where(cdr["20d-50d"] > 0,1,0)
cdr["Buy/Sell"] = np.where(cdr["20d-50d"]<0,-1,cdr["Buy/Sell"])

#cdr["Buy/Sell"].value_counts()

#change last row as closing position
last_scope = cdr.loc[:,"Buy/Sell"].iloc[-1]
cdr.loc[:,"Buy/Sell"].iloc[-1] = 0
#sign function returns -1 if x < 0, 0 if x==0, 1 if x > 0
cdr["Signal"] = np.sign(cdr["Buy/Sell"] - cdr["Buy/Sell"].shift(1))
#cdr.loc[:,"Buy/Sell"].iloc[-1] = last_scope -


def show_signals(stock):
    stock_signal = pd.concat([
        pd.DataFrame({"Price": stock.loc[stock["Signal"] == 1, "Close"],
                      "Buy/Sell": stock.loc[stock["Signal"] == 1, "Buy/Sell"],
                      "Signal": "Buy"
                      }),
        pd.DataFrame({"Price": stock.loc[stock["Signal"] == -1, "Close"],
                      "Buy/Sell": stock.loc[stock["Signal"] == -1, "Buy/Sell"],
                      "Signal": "Sell"
                      })

    ])
    stock_signal.sort_index(inplace=True)

    return stock_signal


signals = show_signals(cdr)


def show_me_profit(stock_signal):
    stock_profit = pd.DataFrame({
        "Price":stock_signal.loc[(stock_signal["Signal"] == "Buy") & stock_signal["Buy/Sell"] == 1, "Price"],
        "Profit":pd.Series(stock_signal["Price"] - stock_signal["Price"].shift(1)).loc[
            stock_signal.loc[(stock_signal["Signal"].shift(1) == "Buy") & (stock_signal["Buy/Sell"].shift(1) == 1)].index].to_list(),
        "End Date": stock_signal["Price"].loc[stock_signal.loc[(stock_signal["Signal"].shift(1) == "Buy") & (stock_signal["Buy/Sell"].shift(1) == 1)].index].index
    })

    return stock_profit

cdr_profits = show_me_profit(signals)

def adding_low_price(stock_profit, stock):
    profit_period = pd.DataFrame({
        "Start": stock_profit.index,
        "End": stock_profit["End Date"]
    })

    stock_profit["Low"] = profit_period.apply(lambda x:min(stock.loc[x["Start"]:x["End"],"Low"]),axis= 1)

    return stock_profit


stock_gain = adding_low_price(cdr_profits,cdr)


def lets_trade(stock_profit,cash,portfolio_risk,batch,stoploss):
    portfolio = pd.DataFrame({
        "Portfolio Value": [],
        "Final Portfolio Value": [],
        "End Date": [],
        "Shares":[],
        "Price per Share": [],
        "Trade Value": [],
        "Gain per Share": [],
        "Total Gain": [],
        "Stop Loss": [],
    })

    for index, row in stock_profit.iterrows():
        batches = np.floor(cash * portfolio_risk) // np.ceil(batch * row["Price"])
        action_value = batches * batch * row["Price"]

        if row["Low"] < (1 -stoploss) * row["Price"]:
            profit_per_share = np.round((1-stoploss) * row["Price"],2)
            stop_loss = True
        else:
            profit_per_share = row["Profit"]
            stop_loss = False

        total_profit = profit_per_share * batches * batch

        portfolio = portfolio.append(pd.DataFrame({
            "Portfolio Value": cash,
            "Final Portfolio Value": cash + total_profit,
            "End Date": row["End Date"],
            "Shares":batch * batches,
            "Price per Share": row["Price"],
            "Trade Value": action_value,
            "Gain per Share": profit_per_share,
            "Total Gain": total_profit,
            "Stop Loss": stop_loss,
            }, index = [index]))
        cash = max(0, cash + total_profit)

    portfolio["Portfolio Value"].plot(grid=True)
    return portfolio

xyz = lets_trade(stock_gain,100000,0.1, 50,0.2)

