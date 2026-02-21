from flask import Flask
import requests
import os

app = Flask(__name__)

symbols = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT"]

def get_signal(symbol):
    try:
        url="https://scanner.tradingview.com/crypto/scan"

        payload={
        "symbols":{"tickers":[f"BINANCE:{symbol}"],"query":{"types":[]}},
        "columns":["close","EMA20","EMA50","RSI"]
        }

        r=requests.post(url,json=payload,timeout=5).json()

        data=r["data"][0]["d"]

        close,ema20,ema50,rsi=data

        if ema20>ema50 and rsi>55:
            return "LONG"
        elif ema20<ema50 and rsi<45:
            return "SHORT"
        else:
            return "BEKLE"

    except:
        return "VERİ YOK"


@app.route("/")
def home():

    cards=""

    for coin in symbols:
        signal=get_signal(coin)

        color="#22c55e"
        if signal=="SHORT":
            color="#ef4444"
        if signal=="VERİ YOK":
            color="gray"

        cards+=f"""
        <div class='card'>
        <h2>{coin}</h2>
        <p style='color:{color};font-size:24px'>{signal}</p>
        </div>
        """

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#0f172a;color:white;text-align:center;font-family:Arial}}
    .card{{background:#1e293b;margin:20px;padding:20px;border-radius:15px}}
    </style>
    </head>
    <body>
    <h1>🚀 TradingView Sinyal Paneli</h1>
    {cards}
    </body>
    </html>
    """

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
