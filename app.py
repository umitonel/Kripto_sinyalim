from flask import Flask
import requests
import os

app = Flask(__name__)

coins = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT"]

def get_signal(symbol):
    try:
        url=f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=60"
        r=requests.get(url,timeout=5)
        data=r.json()

        if not isinstance(data,list):
            return "HATA","-"

        closes=[float(x[4]) for x in data]

        ema20=sum(closes[-20:])/20
        ema50=sum(closes[-50:])/50

        if ema20>ema50:
            return "LONG","A"
        else:
            return "SHORT","A"

    except:
        return "VERİ YOK","-"


@app.route("/")
def home():

    cards=""

    for coin in coins:
        signal,quality=get_signal(coin)

        color="#22c55e"
        if signal=="SHORT":
            color="#ef4444"
        if signal=="VERİ YOK":
            color="gray"

        cards+=f"""
        <div class='card'>
        <h2>{coin}</h2>
        <p style='color:{color};font-size:22px'>{signal}</p>
        <p>Kalite: {quality}</p>
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
    <h1>🚀 Kripto Hafif Panel</h1>
    {cards}
    </body>
    </html>
    """

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
