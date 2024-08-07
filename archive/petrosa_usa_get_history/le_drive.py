import yfinance as yf

def get_ticker_data(symbol: str) -> None:
    symbol_action = yf.Ticker(symbol)
    hist = symbol_action.history(period="max",
                                    interval="1d",
                                    timeout=60,
                                    start="2022-01-27",
                                    end="2022-01-28",
                                    actions=True,
                                    back_adjust=False)
    # hist = symbol_action.history(interval=INTERVAL, start=since)

    print(hist)

get_ticker_data("AAPL")



# data = yf.download(  # or pdr.get_data_yahoo(...
#     # tickers list or string as well
#     tickers="AAPL",

#     # use "period" instead of start/end
#     # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#     # (optional, default is '1mo')
#     start="2010-01-12",
#     end="2010-01-13",

#     # fetch data by interval (including intraday if period < 60 days)
#     # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#     # (optional, default is '1d')
#     interval="1d",

#     # adjust all OHLC automatically
#     # (optional, default is False)
#     auto_adjust=True,

#     # attempt repair of missing data or currency mixups e.g. $/cents
#     repair=False,

#     # download pre/post regular market hours data
#     # (optional, default is False)
#     prepost=True,

#     # use threads for mass downloading? (True/False/Integer)
#     # (optional, default is True)
#     threads=True,

#     # proxy URL scheme use use when downloading?
#     # (optional, default is None)
#     proxy=None
# )

# print(data)