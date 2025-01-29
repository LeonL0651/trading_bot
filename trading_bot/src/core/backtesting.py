class Backtesting:
    def __init__(self, data_handler, strategy_engine):
        self.data_handler = data_handler
        self.strategy_engine = strategy_engine

    def run_backtest(self, symbol, timeframe):
        df = self.data_handler.fetch_ohlcv(symbol, timeframe)
        df = self.strategy_engine.calculate_sma(df)
        df = self.strategy_engine.calculate_rsi(df)
        df = self.strategy_engine.calculate_macd(df)
        df = self.strategy_engine.detect_candlestick_patterns(df)
        return df