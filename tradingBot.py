# from ast import Constant
from operator import imod
import os, sys
import config
from binance.client import Client
import backtrader
import pandas as pd
import datetime, time
# sys.path.insert(0, 'C:\Divyam Projects\Avalor\TradingBot\_strategies\ADXMomentum.py')
# from ADXMomentum import ADXMomentum
from _strategies.strat1 import TestStrategy

client = Client(config.Binanceapikey, config.BinancesecretKey)


def GetHistoricalData(howLong):
    # howLong = howLong
    # Calculate the timestamps for the binance api function
    untilThisDate = datetime.datetime.now()
    sinceThisDate = untilThisDate - datetime.timedelta(days = howLong)
    # Execute the query from binance - timestamps must be converted to strings !
    candle = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, str(sinceThisDate), str(untilThisDate))

    # Create a dataframe to label all the columns returned by binance so we work with them later.
    df = pd.DataFrame(candle, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    # as timestamp is returned in ms, let us convert this back to proper timestamps.
    df.dateTime = pd.to_datetime(df.dateTime, unit='ms').dt.strftime("%Y-%m-%d")
    df.set_index('dateTime', inplace=True)

    # Get rid of columns we do not need
    df = df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol','takerBuyQuoteVol', 'ignore'], axis=1)
    df.to_csv('C:\Divyam Projects\Avalor\TradingBot\qtrade.csv')
    print(df)
GetHistoricalData(1)
data = pd.read_csv('C:\Divyam Projects\Avalor\TradingBot\qtrade.csv',delimiter=",", index_col="dateTime", parse_dates= True)
feed = backtrader.feeds.PandasData(dataname=data)

cerebro = backtrader.Cerebro()

cerebro.broker.set_cash(100000)

cerebro.adddata(feed)
cerebro.addstrategy(TestStrategy)

print('Starting porfolio value: %.2f' %cerebro.broker.getvalue())

cerebro.run()

print('Final porfolio value: %.2f' %cerebro.broker.getvalue())

