from flask import Flask
import requests
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# CONFIG - pon tus datos en Render > Environment
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "TU_TOKEN_AQUI")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "TU_PHONE_ID_AQUI")
WSP_PHONE = os.environ.get("WSP_PHONE", "5213121537009")

capital = 2.93
PORCENTAJE = 2.5

def enviar_whatsapp(msg):
    try:
        url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": WSP_PHONE, "type": "text", "text": {"body": msg}}
        r = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"WSP: {msg} -> {r.status_code}")
    except Exception as e:
        print(f"Error wsp: {e}")

def get_sol_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd", timeout=10).json()
        return float(r['solana']['usd'])
    except:
        return None

def bot_loop():
    global capital
    time.sleep(5)
    enviar_whatsapp(f"✅ Bot SOL {PORCENTAJE}% iniciado - Capital ${capital} - Render OK")
    while True:
        precio = get_sol_price()
        if precio:
            print(f"{datetime.now().strftime('%H:%M:%S')} - SOL ${precio}")
        time.sleep(20)

threading.Thread(target=bot_loop, daemon=True).start()

@app.route('/')
def home():
    return f"Bot SOL {PORCENTAJE}% OK - Live {datetime.now()}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
