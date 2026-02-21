from flask import Flask
import requests
import os

app = Flask(__name__)

coins = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT"]

def ema(values, period):
    k = 2/(period+1)
    ema_val = values[0]
    for price in values:
        ema_val = price*k + ema_val*(1-k)
    return ema_val

def rsi(closes, period=14):
    gains = []
    losses = []

    for i in range(1,len(closes)):
        diff = closes[i]-closes[i-1]
        if diff >=0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:])/period
    avg_loss = sum(losses[-period:])/period if losses else 1

    rs = avg_gain/avg_loss
    return 100-(100/(1+rs))

def get_signal(symbol):
    url=f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=60"
    data=requests.get(url).json()

    closes=[float(x[4]) for x in data]

    ema20=ema(closes[-20:],20)
    ema50=ema(closes[-50:],50)
    rsi_val=rsi(closes)

    if ema20>ema50 and rsi_val>55:
        return "LONG","A+"
    elif ema20<ema50 and rsi_val<45:
        return "SHORT","A+"
    else:
        return "BEKLE","-"

@app.route("/")
def home():

    cards=""

    for coin in coins:
        signal,quality=get_signal(coin)

        color="#22c55e" if signal=="LONG" else "#ef4444"
        if signal=="BEKLE":
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
    <h1>🚀 Hafif Sinyal Paneli</h1>
    {cards}
    </body>
    </html>
    """

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
