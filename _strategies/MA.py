"""
3. sma ema with complicated support
4. sma ema with simple support
4-0.2. sma ema with simple support with 0.2 SL
5. sma wma with simple support
6. sma wma with VWAP simple support
"""
# --- Do not remove these libs ---
from datetime import datetime
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

# from finta import TA as F
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta
import numpy as np # noqa


class MA(IStrategy):

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    # minimal_roi = {
    #     "45": 0.5,
    #     "30": 0.06,
    #     "15": 0.08,
    #     "0":  0.10
    # }
    minimal_roi = {
        "0": 0.1,
        "83": 0.05,
        "142": 0.02,
        "161": 0
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.02

    # Optimal ticker interval for the strategy
    ticker_interval = '15m'
    timeframe = '15min'

    # trailing stoploss
    trailing_stop = False

    # run "populate_indicators" only for new candle
    process_only_new_candles = True

    # Experimental settings (configuration will overide these if set)
    use_sell_signal = True
    sell_profit_only = True
    ignore_roi_if_buy_signal = True

    # Optional order type mapping
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    startup_candle_count = 55

    def informative_pairs(self):
        return []

    def populate_indicators(dataframe: DataFrame, metadata=None) -> DataFrame:
        # dataframe['close'] = dataframe['close'].str.strip("'").dropna().astype(float)
        # dataframe['close'] = dataframe['Close'].copy()
        # if 'close' not in dataframe.columns: dataframe['close'] = dataframe['Close']
        dataframe["SLOWMA"] = ta.EMA(dataframe, 6, )
        dataframe["FASTMA"] = ta.TEMA(dataframe, 6, )
        dataframe["SupportMA"] = ta.SMA(dataframe, 50, )
        
        # dataframe = ods(dataframe)
        return dataframe

    def populate_buy_trend(dataframe: DataFrame, metadata=None) -> DataFrame:
        dataframe.loc[
            (qtpylib.crossed_above(dataframe['FASTMA'], dataframe['SLOWMA'])) &
            (dataframe['close'].astype(float) >= (dataframe['SupportMA'] * 0.95))
            ,'buy'] = 1

        return dataframe

    def populate_sell_trend(dataframe: DataFrame, metadata=None) -> DataFrame:
        dataframe.loc[
            (qtpylib.crossed_below(dataframe['FASTMA'], dataframe['SLOWMA'])) &
            (dataframe['close'].astype(float) <= (dataframe['SupportMA'] * 0.95))
            ,'sell'] = 1
        return dataframe