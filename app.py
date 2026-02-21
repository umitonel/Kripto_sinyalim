from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Kripto Sinyal Paneli</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                background-color: #0f172a;
                font-family: Arial;
                color: white;
                text-align: center;
            }
            h1 {
                margin-top: 20px;
            }
            .card {
                background: #1e293b;
                padding: 20px;
                margin: 20px;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0,255,255,0.2);
            }
            .long { color: #22c55e; }
            .short { color: #ef4444; }
            .badge {
                padding: 5px 10px;
                border-radius: 8px;
                background: gold;
                color: black;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🚀 Kripto Sinyal Paneli</h1>

        <div class="card">
            <h2>BTCUSDT</h2>
            <p class="long">LONG</p>
            <span class="badge">A+</span>
            <p>Entry: 52000</p>
            <p>Stop: 51500</p>
            <p>TP: 53000</p>
            <p>Risk: 3$</p>
            <p>Önerilen Pozisyon: 150$</p>
        </div>

        <div class="card">
            <h2>SOLUSDT</h2>
            <p class="short">SHORT</p>
            <span class="badge">A</span>
            <p>Entry: 102</p>
            <p>Stop: 104</p>
            <p>TP: 98</p>
            <p>Risk: 3$</p>
            <p>Önerilen Pozisyon: 150$</p>
        </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
