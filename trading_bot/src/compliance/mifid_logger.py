import logging

class MiFIDLogger:
    def __init__(self):
        logging.basicConfig(filename='mifid.log', level=logging.INFO)

    def log_trade(self, trade_details):
        logging.info(f"Trade executed: {trade_details}")