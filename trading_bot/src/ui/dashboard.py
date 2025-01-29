from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
import time

class Dashboard:
    def __init__(self, metrics_callback):
        self.console = Console()
        self.layout = Layout()
        self.metrics_callback = metrics_callback
        
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )

    def update_display(self):
        metrics = self.metrics_callback()
        
        # Header
        header = Text("CRYPTO TRADING BOT", justify="center", style="bold blue")
        self.layout["header"].update(header)

        # Main Content
        main_table = Table(title="Live Metrics")
        main_table.add_column("Metric", justify="left")
        main_table.add_column("Value", justify="right")
        
        main_table.add_row("Win Rate", f"{metrics['win_rate']*100:.2f}%")
        main_table.add_row("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
        main_table.add_row("24h Profit", f"${metrics['daily_profit']:+.2f}")
        main_table.add_row("Open Positions", str(metrics['open_positions']))
        
        self.layout["main"].update(main_table)

        # Footer
        footer = Text(f"Last update: {time.strftime('%H:%M:%S')}", style="italic")
        self.layout["footer"].update(footer)

        self.console.clear()
        self.console.print(self.layout)

    def start_live_view(self, refresh_interval=1):
        with Live(self.layout, refresh_per_second=4) as live:
            while True:
                self.update_display()
                time.sleep(refresh_interval)