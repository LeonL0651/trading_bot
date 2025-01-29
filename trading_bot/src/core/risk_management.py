class RiskManagement:
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital

    def calculate_position_size(self, risk_per_trade=0.01, stop_loss=0.02):
        return self.initial_capital * risk_per_trade / stop_loss

    def dynamic_stop_loss(self, df, atr_period=14, atr_multiplier=2):
        df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=atr_period)
        df['stop_loss'] = df['close'] - df['atr'] * atr_multiplier
        return df
