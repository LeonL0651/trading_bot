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

def main():
    data_handler = CEXDataHandler('binance')
    strategy_engine = StrategyEngine(data_handler)
    risk_management = RiskManagement()
    execution = Execution(data_handler)
    backtesting = Backtesting(data_handler, strategy_engine)
    mifid_logger = MiFIDLogger()
    tax_reporter = TaxReporter()
    social_trading = SocialTrading()
    dashboard = Dashboard()

    symbol = 'BTC/USDT'
    timeframe = '1h'

    df = backtesting.run_backtest(symbol, timeframe)
    print(df)

    # Example usage of other components
    mifid_logger.log_trade({"symbol": symbol, "amount": 1, "price": 50000})
    tax_report = tax_reporter.generate_report([{"symbol": symbol, "amount": 1, "price": 50000}])
    print(tax_report)
    social_trading.copy_trade("strategy_123")
    dashboard.display_metrics({"win_rate": 0.75, "sharpe_ratio": 1.5})

if __name__ == "__main__":
    main()