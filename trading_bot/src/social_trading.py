import requests
from datetime import datetime

class SocialTrading:
    def __init__(self, api_client):
        self.api_client = api_client
        self.strategies = {}
        self.load_popular_strategies()

    def load_popular_strategies(self):
        # Mock-API-Aufruf
        self.strategies = {
            "strategy_123": {
                "id": "strategy_123",
                "name": "Gold Cross 50/200",
                "owner": "pro_trader_89",
                "performance": 27.4,
                "trades": 132
            }
        }

    def copy_trade(self, strategy_id):
        strategy = self.strategies.get(strategy_id)
        if not strategy:
            return "Strategy not found"

        # Simulierte Trade-Execution
        trade_details = {
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy_id,
            "action": "BUY",
            "symbol": "BTC/USDT",
            "amount": 1.0,
            "price": 30000.0
        }
        
        # API-Integration würde hier erfolgen
        # response = self.api_client.execute_trade(trade_details)
        return {
            "status": "success",
            "message": f"Copied strategy {strategy_id}",
            "trade": trade_details
        }