import ccxt, time, os
from datetime import datetime

API_KEY = os.getenv('OKX_KEY')
API_SECRET = os.getenv('OKX_SECRET')
API_PASS = os.getenv('OKX_PASS')

exchange = ccxt.okx({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': API_PASS,
    'enableRateLimit': True,
})

print("BOT SOL INICIADO con $2.93")

while True:
    try:
        ticker = exchange.fetch_ticker('SOL/USDT')
        print(f"{datetime.now()} Precio SOL: {ticker['last']}")
        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(30)
