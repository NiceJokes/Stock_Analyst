import pandas as pd
from data_and_plotting import start, end,stocks_change_with_wig

# Polish virtual risk free - 10y Bonds
risk_free_rate = pd.read_csv("/Users/lt/Desktop/coders/Stock_Analyst/10ply_b_d.csv")


risk_free_rate = pd.DataFrame(risk_free_rate.loc[:,["Open","High","Low","Close"]].iloc[1:].to_numpy(),
                         index= pd.DatetimeIndex(risk_free_rate.iloc[1:,0]),
                         columns=["Open","High","Low","Close"]).sort_index()

risk_free_rate = risk_free_rate[start:end].tail(1)
risk_free_rate = risk_free_rate.iloc[0]['Close']


#Annual Percentage Rate APR
apr = stocks_change_with_wig * 252 * 100

''' Linear regression model:
    y_i = alpha + beta_xi 
    a linear regression model tells you how x_i and y_i are related, 
    and how values of x_i can be used to predict values of y_i
    
    CAPM:
    R_t - r_{RF} = alpha + beta (R_Mt - r_RF) 
    
    beta = r * {s_y}/{s_x} / r = correlation between stock return and market index
                            s_y/x = standard deviations
    alpha =  y(mean) - beta * x(mean) 

    the risk premium of individual stock depends on two components: 
    market risk and the market risk-premium
    
    alpha - average excess return over the market
    beta - how much a stock moves in relation to the market, the expected market risk-premium increases by
    1%, the individual stock's expected return would increase by β% and vice versa
'''

# correlation between stocks and index
stocks_index_corr = apr.drop("WIG20",1).corrwith(apr.WIG20)
#print(stocks_index_corr)

# standard deviations
std_y = apr.drop("WIG20",1).std()
std_x = apr.WIG20.std()

# sample mean
y_mean = apr.drop("WIG20",1).mean() - risk_free_rate
x_mean = apr.WIG20.mean() - risk_free_rate

# alpha and beta
beta = stocks_index_corr * std_y/std_x
alpha = y_mean - (beta * std_x)

print(beta,"*******\n",alpha)

# sharpe ration /  return of an investment compared to its risk
sharp_r_y = (y_mean - risk_free_rate)/std_y
sharp_r_x = (x_mean - risk_free_rate)/std_x
print(sharp_r_y,"*******\n",sharp_r_x)