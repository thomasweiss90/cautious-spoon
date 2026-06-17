import os
import json
import requests

def send_telegram_message():
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Hier laden wir die Daten, die der Fetcher gerade gespeichert hat
    with open('data/raw_pegel.json', 'r') as f:
        data = json.load(f)
    
    # Platzhalter: Hier kommt später deine Logik rein
    message = "🎣 **Petri-Check Leipzig:**\nPegel Burghausen: [Wert] cm\nTrend: [Stabil/Steigend]"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
    
    requests.post(url, data=payload)

if __name__ == "__main__":
    send_telegram_message()
