from flask import Flask
import requests
import os

app = Flask(__name__)

coins={
"bitcoin":"BTCUSDT",
"ethereum":"ETHUSDT",
"solana":"SOLUSDT",
"ripple":"XRPUSDT"
}

def get_price(coin):
    try:
        url=f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        data=requests.get(url,timeout=5).json()
        return data[coin]["usd"]
    except:
        return None

@app.route("/")
def home():

    cards=""

    for cg,name in coins.items():

        price=get_price(cg)

        if price:
            signal="LONG" if price%2>1 else "SHORT"
            color="#22c55e" if signal=="LONG" else "#ef4444"
        else:
            signal="VERİ YOK"
            color="gray"

        cards+=f"""
        <div class='card'>
        <h2>{name}</h2>
        <p style='color:{color};font-size:22px'>{signal}</p>
        <p>Fiyat: {price}</p>
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
    <h1>🚀 Kripto Sinyal Paneli</h1>
    {cards}
    </body>
    </html>
    """

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
