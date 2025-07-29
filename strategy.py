from notifier import send_telegram_message
from utils import connect_to_binance
import pandas as pd
import pandas_ta as ta
import os

TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT"))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT"))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT"))

symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]

def fetch_ohlcv(exchange, symbol, tf):
    return exchange.fetch_ohlcv(symbol, timeframe=tf, limit=100)

def generate_signal(df):
    df['EMA20'] = ta.ema(df['close'], length=20)
    df['EMA50'] = ta.ema(df['close'], length=50)
    if df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]:
        return "BUY"
    elif df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1]:
        return "SELL"
    else:
        return "HOLD"

def check_trade_signal():
    exchange = connect_to_binance()
    for symbol in symbols:
        ohlcv_h4 = fetch_ohlcv(exchange, symbol, "4h")
        df = pd.DataFrame(ohlcv_h4, columns=["time", "open", "high", "low", "close", "volume"])
        signal = generate_signal(df)
        current_price = df['close'].iloc[-1]  # Last candle close price
        message = f"{symbol} => Signal: {signal} at ${current_price:.2f}"
        print(message)
        send_telegram_message(message)