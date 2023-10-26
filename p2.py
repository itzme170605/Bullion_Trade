import yfinance as yf
import yahoo_finance as yf1
gold=yf1.Share("SI=F")

print(gold.get_price())



