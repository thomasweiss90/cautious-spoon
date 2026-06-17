import requests
import json
from datetime import datetime

# LfULG Sachsen Pegel-Datenquelle
URL = "https://www.umwelt.sachsen.de/umwelt/infosysteme/hwis/pegel/aktuell.json"

def fetch_lhw_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        
        # Speichern als Artefakt
        with open('data/raw_pegel.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"[{datetime.now()}] Daten erfolgreich abgerufen.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    fetch_lhw_data()
