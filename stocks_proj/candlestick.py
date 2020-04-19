import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
from mplfinance.original_flavor import candlestick_ohlc



def pandas_candlestick_ohlc(dat, days='day', adj = False, otherseries = None):

    mondays = WeekdayLocator(MONDAY)
    all_days = DayLocator()

    fields = ['Open', 'High', 'Low','Close']
    transdat = dat.loc[:,fields] # Selects single column or subset of columns by label
    transdat.columns = pd.Index(['Open', 'High', 'Low','Close'])

    if(type(days) == str):
        if days == "day":
            plotdat = transdat
            days = 1
        elif days in ['week', 'month', 'year']:
            if days == 'week':
                transdat['week'] = pd.to_datetime(transdat.index).map(lambda x: x.isocalender()[1]) #Return a 3-tuple, (ISO year, ISO week number, ISO weekday).
            elif days == 'month':
                transdat['month'] = pd.to_datetime(transdat.index).map(lambda x: x.month)
            transdat['year'] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0])

            grouped = transdat.groupby(list({'year', days}))
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []})

            for name,group in grouped:
                plotdat = plotdat.append(pd.DataFrame({'Open':group.iloc[0,0],
                                                       'High':max(group.High),
                                                       'Low': min(group.Low),
                                                       'Close': group.iloc[-1,3]},
                                                       index = [group.index[0]]
                                                       ))
            if days == 'week':
                days = 5
            elif days == 'month':
                days = 30
            elif days == 'year':
                days = 365

    elif (type(days) == int and days >= 1):

        transdat['stick'] = [pd.np.floor(i / days) for i in range(len(transdat.index))]
        grouped = transdat.groupby('stick')
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []})

        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({'Open': group.iloc[0, 0],
                                                   'High': max(group.High),
                                                   'Low': min(group.Low),
                                                   'Close': group.iloc[-1, 3]},
                                                  index=[group.index[0]]
                                                  ))
    else:
        raise ValueError('Valid inputs - "days" include the strings or a positive integer')

    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # for example Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(all_days)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candelstick chart
    candlestick_ohlc(ax, list(
        zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
            plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                     colorup="black", colordown="red", width=days * .4)

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:, otherseries].plot(ax=ax, lw=1.3, grid=True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()


