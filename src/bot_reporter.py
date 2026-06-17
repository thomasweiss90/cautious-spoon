import os
import json
import requests
from pathlib import Path
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def main():
    # 1. Prüfen ob Datei existiert
    json_path = Path("data/raw_pegel.json")
    if not json_path.exists():
        print("Abbruch: data/raw_pegel.json nicht gefunden")
        return  # Kein Post, kein Fehler im Channel

    # 2. Daten laden
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        return  # Kein Post

    if not data:
        print("Keine Daten vorhanden")
        return

    # 3. Nachricht bauen
    msg = f"""🎣 Angel-Check
Stand: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Einträge: {len(data)}"""

    # 4. Senden
    if not TOKEN or not CHAT_ID:
        print("Fehlende Telegram-Credentials")
        return

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        r = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_web_page_preview": "true"
        }, timeout=20)
        
        if r.status_code == 200:
            print("Erfolgreich gepostet")
        else:
            print(f"Fehler {r.status_code}: {r.text}")
            
    except Exception as e:
        print(f"Sendefehler: {e}")

if __name__ == "__main__":
    main()
