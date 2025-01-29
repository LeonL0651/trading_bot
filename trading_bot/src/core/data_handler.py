import ccxt
import pandas as pd
import yaml

class CEXDataHandler:
    def __init__(self, exchange_name='binance'):
        with open('config/exchanges.yaml', 'r') as file:
            config = yaml.safe_load(file)
        exchange_config = config['exchanges'][exchange_name]
        self.exchange = getattr(ccxt, exchange_name)({
            'apiKey': exchange_config['api_key'],
            'secret': exchange_config['api_secret'],
            'enableRateLimit': True,
            'options': {'adjustForTimeDifference': True}
        })
        self.exchange_name = exchange_name

    def fetch_ohlcv(self, symbol: str, timeframe: str) -> pd.DataFrame:
        data = self.exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def fetch_all_trading_pairs(self):
        """Holt alle verfügbaren Trading-Pairs von der Börse."""
        markets = self.exchange.load_markets()
        return [symbol for symbol in markets if markets[symbol]['active']]

    def fetch_liquidity(self, symbol: str) -> float:
        """Holt die Liquidität (Volumen) für ein Trading-Pair."""
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['quoteVolume']  # Volumen in der Quote-Währung (z. B. USDT)