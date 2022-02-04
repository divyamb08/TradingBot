FROM python:3.8

# MAINTAINER Olivier TASSEL <https://github.com/otassel>

RUN pip install numpy 
RUN pip install python-binance
RUN pip install pandas
RUN pip install backtrader

# TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz
RUN pip install freqtrade
RUN pip install websocket-client
COPY . /TradingBot
CMD python /TradingBot/tradingBot.py