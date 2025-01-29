import json
import os

class I18n:
    def __init__(self, language='en'):
        self.language = language
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        lang_file = f"translations/{self.language}.json"
        if os.path.exists(lang_file):
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        else:
            # Fallback to English
            self.translations = {
                "trade_executed": "Trade executed",
                "portfolio_value": "Portfolio Value",
                "current_balance": "Current Balance"
            }

    def translate(self, key):
        return self.translations.get(key, key)

# Erstellen Sie den translations/ Ordner mit JSON-Dateien:
# translations/de.json
{
    "trade_executed": "Trade ausgeführt",
    "portfolio_value": "Portfoliowert",
    "current_balance": "Aktueller Kontostand"
}