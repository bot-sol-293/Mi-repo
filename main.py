import time
import threading
from flask import Flask
import requests
import os

# --- SERVIDOR PARA RENDER 24/7 ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot SOL 2.5% - $2.93 - OKX - VIVO"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- CONFIG WHATSAPP ---
WSP_PHONE = "5213121537009"
WSP_APIKEY = "4543250"

def send_whatsapp(msg):
    try:
        # Codifica el mensaje para URL
        url = f"https://api.callmebot.com/whatsapp.php?phone={WSP_PHONE}&text={msg}&apikey={WSP_APIKEY}"
        print(f"Enviando WhatsApp: {msg}")
        requests.get(url, timeout=15)
    except Exception as e:
        print(f"Error WhatsApp: {e}")

# --- CONFIG BOT ---
CAPITAL = 2.93
TAKE_PROFIT = 0.025 # 2.5%

def get_sol_price():
    try:
        url = "https://www.okx.com/api/v5/market/ticker?instId=SOL-USDT"
        r = requests.get(url, timeout=10).json()
        return float(r['data'][0]['last'])
    except Exception as e:
        print(f"Error precio: {e}")
        return None

def bot_loop():
    print("BOT INICIADO")
    send_whatsapp(f"✅ Bot SOL 2.5% iniciado en Render - Capital ${CAPITAL}")
    
    bought_price = None

    while True:
        try:
            price = get_sol_price()
            if not price:
                time.sleep(5)
                continue

            print(f"SOL: ${price} | Comprado: {bought_price}")

            if bought_price is None:
                bought_price = price
                send_whatsapp(f"🟢 COMPRA SOL a ${price:.2f} con ${CAPITAL}")
            else:
                profit = (price - bought_price) / bought_price
                if profit >= TAKE_PROFIT:
                    ganancia = CAPITAL * profit
                    send_whatsapp(f"🔵 VENTA SOL a ${price:.2f}\nGanancia: {profit*100:.2f}% = ${ganancia:.3f}\nCapital nuevo: ${CAPITAL + ganancia:.2f}")
                    bought_price = None
                elif profit <= -0.05:
                    send_whatsapp(f"🔴 STOP LOSS SOL a ${price:.2f} ({profit*100:.2f}%)")
                    bought_price = None

            time.sleep(15)
        except Exception as e:
            print(f"Error loop: {e}")
            time.sleep(15)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot_loop()
