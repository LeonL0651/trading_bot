import pandas as pd

class StrategyEngine:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def find_profitable_pairs(self, timeframe='1h', min_liquidity=100000):
        """
        Analysiert alle Trading-Pairs und gibt die profitabelsten zurück.
        :param timeframe: Zeitrahmen für die Analyse (z. B. '1h', '1d')
        :param min_liquidity: Mindestliquidität, um ein Pair zu berücksichtigen
        :return: Liste von profitablen Pairs mit Metriken
        """
        profitable_pairs = []
        all_pairs = self.data_handler.fetch_all_trading_pairs()

        for pair in all_pairs:
            try:
                # Liquiditätsprüfung
                liquidity = self.data_handler.fetch_liquidity(pair)
                if liquidity < min_liquidity:
                    continue

                # OHLCV-Daten holen
                df = self.data_handler.fetch_ohlcv(pair, timeframe)

                # Technische Indikatoren berechnen
                df = self.calculate_sma(df, period=50)
                df = self.calculate_rsi(df, period=14)
                df = self.calculate_macd(df)

                # Trendanalyse (z. B. SMA-Kreuzung)
                last_close = df['close'].iloc[-1]
                last_sma = df['sma'].iloc[-1]
                trend = "up" if last_close > last_sma else "down"

                # RSI-Überkauft/Überverkauft
                last_rsi = df['rsi'].iloc[-1]
                rsi_signal = "overbought" if last_rsi > 70 else "oversold" if last_rsi < 30 else "neutral"

                # MACD-Signal
                last_macd = df['macd'].iloc[-1]
                last_macd_signal = df['macdsignal'].iloc[-1]
                macd_signal = "bullish" if last_macd > last_macd_signal else "bearish"

                # Pair als profitabel markieren, wenn bestimmte Bedingungen erfüllt sind
                if trend == "up" and rsi_signal == "oversold" and macd_signal == "bullish":
                    profitable_pairs.append({
                        "pair": pair,
                        "liquidity": liquidity,
                        "trend": trend,
                        "rsi": last_rsi,
                        "macd_signal": macd_signal
                    })
            except Exception as e:
                print(f"Fehler bei der Analyse von {pair}: {e}")

        # Sortieren nach Liquidität (absteigend)
        profitable_pairs.sort(key=lambda x: x['liquidity'], reverse=True)
        return profitable_pairs

    def calculate_sma(self, df, period=50):
        """Berechnet den Simple Moving Average"""
        df['sma'] = df['close'].rolling(window=period).mean()
        return df

    def calculate_rsi(self, df, period=14):
        """Berechnet den Relative Strength Index"""
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        
        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
        
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))
        df['rsi'].fillna(100.0, inplace=True)  # Handle division by zero
        return df

    def calculate_macd(self, df):
        """Berechnet MACD und Signal-Linie"""
        ema12 = df['close'].ewm(span=12, adjust=False).mean()
        ema26 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = ema12 - ema26
        df['macdsignal'] = df['macd'].ewm(span=9, adjust=False).mean()
        return df
