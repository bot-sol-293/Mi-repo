from flask import Flask
import requests, os, threading, time
from datetime import datetime

app = Flask(__name__)

def get_sol():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd", timeout=10).json()
        return r['solana']['usd']
    except:
        return None

def bot():
    time.sleep(5)
    print("✅ Bot SOL 2.5% iniciado")
    while True:
        p = get_sol()
        if p:
            print(f"{datetime.now().strftime('%H:%M:%S')} SOL ${p}")
        time.sleep(20)

threading.Thread(target=bot, daemon=True).start()

@app.route('/')
def home():
    return "Bot SOL OK - Live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
