from flask import Flask
import requests
import pandas as pd
import ta
import os

app = Flask(__name__)

coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]

def get_signal(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    data = requests.get(url).json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","trades","tbbav","tbqav","ignore"
    ])

    df["close"] = df["close"].astype(float)

    df["ema20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)

    last = df.iloc[-1]

    if last["ema20"] > last["ema50"] and last["rsi"] > 55:
        return "LONG", "A+"
    elif last["ema20"] < last["ema50"] and last["rsi"] < 45:
        return "SHORT", "A+"
    else:
        return "BEKLE", "-"

@app.route("/")
def home():
    cards = ""

    for coin in coins:
        signal, quality = get_signal(coin)

        color = "#22c55e" if signal == "LONG" else "#ef4444"
        if signal == "BEKLE":
            color = "gray"

        cards += f"""
        <div class="card">
            <h2>{coin}</h2>
            <p style='color:{color}; font-size:20px;'>{signal}</p>
            <p>Kalite: {quality}</p>
        </div>
        """

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                background:#0f172a;
                color:white;
                font-family:Arial;
                text-align:center;
            }}
            .card {{
                background:#1e293b;
                margin:20px;
                padding:20px;
                border-radius:15px;
                box-shadow:0 0 15px rgba(0,255,255,0.2);
            }}
        </style>
    </head>
    <body>
        <h1>🚀 Hafif Sinyal Paneli (1H)</h1>
        {cards}
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
