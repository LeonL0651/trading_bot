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
    
    def fetch_ohlcv(self, symbol: str, timeframe: str) -> pd.DataFrame:
        data = self.exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def fetch_order_book(self, symbol: str, limit=10) -> dict:
        return self.exchange.fetch_order_book(symbol, limit)

    def fetch_ticker(self, symbol: str) -> dict:
        return self.exchange.fetch_ticker(symbol)