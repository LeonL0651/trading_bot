class TaxReporter:
    def __init__(self):
        pass

    def generate_report(self, trades):
        report = "Tax Report:\n"
        for trade in trades:
            report += f"Trade: {trade}\n"
        return report