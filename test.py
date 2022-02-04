import datetime
import backtrader
# from strategies import TestStrategy
from _strategies.ADXMomentum import ADXMomentum

from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
                              MONTHS_PER_YEAR, DAYS_PER_WEEK,
                              SEC_PER_HOUR, SEC_PER_DAY,
                              num2date, rrulewrapper, YearLocator,
                              MicrosecondLocator)
cerebro = backtrader.Cerebro()

cerebro.broker.set_cash(1000000)

data = backtrader.feeds.YahooFinanceCSVData(
    dataname="C:\Divyam Projects\Avalor\BackTrader\BAJAJFINSV.NS.csv",
    # Do not pass values before this date
    fromdate=datetime.datetime(2005, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2021, 12, 31),
    reverse=False)
# for i in data:
#     print(i)
cerebro.adddata(data)
cerebro.addstrategy(ADXMomentum)

cerebro.addsizer(backtrader.sizers.FixedSize, stake=1000)

print('Starting porfolio value: %.2f' %cerebro.broker.getvalue())

cerebro.run()

print('Final porfolio value: %.2f' %cerebro.broker.getvalue())

cerebro.plot()