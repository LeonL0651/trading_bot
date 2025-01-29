class Execution:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def place_market_order(self, symbol, side, amount):
        order = self.data_handler.exchange.create_market_order(symbol, side, amount)
        return order

    def place_limit_order(self, symbol, side, amount, price):
        order = self.data_handler.exchange.create_limit_order(symbol, side, amount, price)
        return order

    def place_stop_order(self, symbol, side, amount, stop_price):
        order = self.data_handler.exchange.create_order(symbol, 'stop', side, amount, stop_price)
        return order