import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
import config

client = Client(config.Binanceapikey, config.BinancesecretKey)

bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')
await socket.__aenter__()
msg = await socket.recv()
print(msg)