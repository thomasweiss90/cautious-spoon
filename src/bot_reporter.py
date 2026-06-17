import os
import requests
from pathlib import Path
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def load_json(path):
    try:
        import json
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"Fehler: Datei nicht gefunden: {path}"
    except Exception as e:
        return None, f"Fehler beim Lesen von {path}: {e}"

def send_telegram_message(text):
    if not TOKEN or not CHAT_ID:
        raise RuntimeError("TELEGRAM_TOKEN oder TELEGRAM_CHAT_ID fehlt")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    resp = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()

def build_message():
    data, error = load_json("data/raw_pegel.json")

    if error:
        return (
            "Bot-Report\n\n"
            f"{error}\n"
            "Hinweis: Der Workflow hat die Datei vermutlich nicht erzeugt."
        )

    lines = []
    lines.append("Bot-Report")
    lines.append("")
    lines.append(f"Zeit: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append("Pegel-Daten geladen.")

    if isinstance(data, dict):
        lines.append(f"Einträge: {len(data)}")
    else:
        lines.append("Warnung: Unerwartetes Datenformat.")

    return "\n".join(lines)

def main():
    try:
        msg = build_message()
        send_telegram_message(msg)
        print("Telegram-Nachricht gesendet.")
    except Exception as e:
        print(f"Fehler: {e}")
        raise

if __name__ == "__main__":
    main()
