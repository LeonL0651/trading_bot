import pandas as pd
import talib

class StrategyEngine:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def calculate_sma(self, df, period=14):
        df['sma'] = talib.SMA(df['close'], timeperiod=period)
        return df

    def calculate_rsi(self, df, period=14):
        df['rsi'] = talib.RSI(df['close'], timeperiod=period)
        return df

    def calculate_macd(self, df, fastperiod=12, slowperiod=26, signalperiod=9):
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        return df

    def detect_candlestick_patterns(self, df):
        df['doji'] = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
        df['hammer'] = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
        df['engulfing'] = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
        return df