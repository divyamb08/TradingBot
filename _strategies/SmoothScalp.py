# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from typing import Dict, List
from functools import reduce
from pandas import DataFrame, DatetimeIndex, merge
# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy  # noqa


class SmoothScalp(IStrategy):
    """
        this strategy is based around the idea of generating a lot of potentatils buys and make tiny profits on each trade

        we recommend to have at least 60 parallel trades at any time to cover non avoidable losses
    """

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        # "0": 0.01
        "0": 0.05 #custom
    }
    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    # should not be below 3% loss

    stoploss = -0.1 #custom
    # stoploss = -0.5
    # Optimal ticker interval for the strategy
    # the shorter the better
    ticker_interval = '1m'
    timeframe = '1T'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['ema_high'] = ta.EMA(dataframe, timeperiod=5, price='high')
        dataframe['ema_low'] = ta.EMA(dataframe, timeperiod=5, price='low')
        stoch_fast = ta.STOCHF(dataframe, 5, 3, 0, 3, 0)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']
        dataframe['adx'] = ta.ADX(dataframe)
        dataframe['mfi'] = ta.MFI(dataframe)
        dataframe['cci'] = ta.CCI(dataframe)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                        (dataframe['open'] < dataframe['ema_low']) &
                        (dataframe['adx'] > 30) &
                        (dataframe['mfi'] < 30) &
                        (
                                (dataframe['fastk'] < 30) &
                                (dataframe['fastd'] < 30) &
                                (qtpylib.crossed_above(dataframe['fastk'], dataframe['fastd']))
                        ) &
                        (dataframe['cci'] < -150)
                )

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (
                            (
                                (dataframe['open'] >= dataframe['ema_high'])

                            ) |
                            (
                                    (qtpylib.crossed_above(dataframe['fastk'], 70)) |
                                    (qtpylib.crossed_above(dataframe['fastd'], 70))

                            )
                    ) & (dataframe['cci'] > 150)
            )
            ,
            'sell'] = 1
        return dataframe
