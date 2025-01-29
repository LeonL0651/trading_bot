from src.core.data_handler import CEXDataHandler
from src.core.strategy_engine import StrategyEngine
from src.core.risk_management import RiskManagement
from src.core.execution import Execution
from src.core.backtesting import Backtesting
from src.compliance.mifid_logger import MiFIDLogger
from src.compliance.tax_reporter import TaxReporter
from src.web.api import app as web_api
from src.social_trading import SocialTrading
from src.ui.dashboard import Dashboard
from src.api_client import APIClient
from src.web.i18n import I18n
import threading
import time

# Konfiguration
EXCHANGE_NAME = "binance"
SYMBOL = "BTC/USDT"
TIMEFRAME = "1h"

# API-Client für Social Trading
SOCIAL_TRADING_API_URL = "https://api.socialtrading.com/v1"
SOCIAL_TRADING_API_KEY = "your_social_trading_api_key"

# Initialisierung der Komponenten
data_handler = CEXDataHandler(EXCHANGE_NAME)
strategy_engine = StrategyEngine(data_handler)
risk_management = RiskManagement(initial_capital=10000)
execution = Execution(data_handler)
backtesting = Backtesting(data_handler, strategy_engine)
mifid_logger = MiFIDLogger()
tax_reporter = TaxReporter()
api_client = APIClient(SOCIAL_TRADING_API_URL, SOCIAL_TRADING_API_KEY)
social_trading = SocialTrading(api_client)
i18n = I18n(language="en")

# Dashboard-Metriken
def get_metrics():
    return {
        "win_rate": 0.75,
        "sharpe_ratio": 1.5,
        "daily_profit": 2450.50,
        "open_positions": 3
    }

dashboard = Dashboard(metrics_callback=get_metrics)

# Hauptfunktion
def main():
    # Initialisierung der Komponenten
    data_handler = CEXDataHandler('kraken')  # Kraken als Börse
    strategy_engine = StrategyEngine(data_handler)
    risk_management = RiskManagement(initial_capital=10000)
    execution = Execution(data_handler)
    backtesting = Backtesting(data_handler, strategy_engine)
    mifid_logger = MiFIDLogger()
    tax_reporter = TaxReporter()
    api_client = APIClient(SOCIAL_TRADING_API_URL, SOCIAL_TRADING_API_KEY)
    social_trading = SocialTrading(api_client)
    i18n = I18n(language="en")

    # Profitable Pairs finden
    profitable_pairs = strategy_engine.find_profitable_pairs(timeframe='1h', min_liquidity=100000)
    print("Profitable Pairs:")
    for pair in profitable_pairs:
        print(f"{pair['pair']} - Liquidität: {pair['liquidity']}, Trend: {pair['trend']}, RSI: {pair['rsi']:.2f}")

    # Handel mit den profitablen Pairs
    for pair in profitable_pairs:
        symbol = pair['pair']
        print(f"Handel mit {symbol}...")

        # Backtest durchführen
        df = backtesting.run_backtest(symbol, '1h')
        print(df.tail())

        # Trade ausführen (Beispiel: Kaufen)
        trade_details = {
            "symbol": symbol,
            "amount": 1,
            "price": df['close'].iloc[-1],
            "side": "buy"
        }
        order = execution.place_market_order(symbol, "buy", 1)
        mifid_logger.log_trade(trade_details)

    # Dashboard starten
    dashboard_thread = threading.Thread(target=dashboard.start_live_view)
    dashboard_thread.daemon = True
    dashboard_thread.start()

    # Web-API starten
    web_api_thread = threading.Thread(target=web_api.run, kwargs={"port": 5000})
    web_api_thread.daemon = True
    web_api_thread.start()

    # Hauptprogramm am Laufen halten
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
