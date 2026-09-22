from flask import Flask
import requests, threading, time, os
from datetime import datetime

app = Flask(__name__)

# --- CONFIG ---
WSP_TOKEN = "TU_TOKEN_DE_WHATSAPP_AQUI"
WSP_PHONE = "5213121537009"
WSP_URL = "https://graph.facebook.com/v20.0/ID_DE_TU_NUMERO/messages"

capital = 2.93
en_posicion = False
precio_compra = 0

def enviar_whatsapp(msg):
    try:
        headers = {"Authorization": f"Bearer {WSP_TOKEN}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": WSP_PHONE, "type": "text", "text": {"body": msg}}
        requests.post(WSP_URL, json=data, headers=headers)
        print(msg)
    except Exception as e:
        print(f"Error wsp: {e}")

def get_sol_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd", timeout=10).json()
        return float(r['solana']['usd'])
    except:
        return None

def bot_loop():
    global capital, en_posicion, precio_compra
    enviar_whatsapp(f"✅ Bot SOL 2.5% iniciado en Render - Capital ${capital}")
    while True:
        precio = get_sol_price()
        if precio:
            # ejemplo logica 2.5%
            print(f"{datetime.now()} - SOL ${precio}")
        time.sleep(15)

threading.Thread(target=bot_loop, daemon=True).start()

@app.route('/')
def home():
    return "Bot SOL OK - Live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
