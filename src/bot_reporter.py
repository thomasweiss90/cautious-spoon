import os
import json
import requests
from pathlib import Path
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def load_json(path):
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {path}")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen von {path}: {e}")
        return None

def send_telegram_message(text):
    if not TOKEN or not CHAT_ID:
        print("Fehler: TELEGRAM_TOKEN oder TELEGRAM_CHAT_ID fehlt")
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        resp = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text,
                "disable_web_page_preview": True,
            },
            timeout=20,
        )
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"Fehler beim Senden an Telegram: {e}")
        return False

def build_message():
    data = load_json("data/raw_pegel.json")
    if data is None:
        return None

    # Falls du hier weitere Pflichtdaten prüfst:
    if not isinstance(data, dict) or not data:
        print("Fehler: Unerwartetes oder leeres Datenformat")
        return None

    lines = []
    lines.append("Angel-Check")
    lines.append("")
    lines.append(f"Zeit: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append(f"Einträge: {len(data)}")

    return "\n".join(lines)

def main():
    msg = build_message()
    if msg is None:
        print("Kein Post, weil der Build fehlgeschlagen ist.")
        return

    ok = send_telegram_message(msg)
    if not ok:
        print("Kein Post, weil Telegram-Versand fehlgeschlagen ist.")
        return

    print("Telegram-Nachricht erfolgreich gesendet.")

if __name__ == "__main__":
    main()
