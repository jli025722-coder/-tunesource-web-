import os
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

YANDEX_TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "114399307"

@app.route("/api/metrica_visits")
def metrica_visits():
    if not YANDEX_TOKEN:
        return jsonify({"error": "Token not set"}), 500
    url = "https://api-metrika.yandex.net/stat/v1/data"
    params = {
        "ids": COUNTER_ID,
        "metrics": "ym:s:visits",
        "date1": "2026-01-01",
        "date2": "today"
    }
    headers = {"Authorization": f"OAuth {YANDEX_TOKEN}"}
    resp = requests.get(url, params=params, headers=headers)
    return jsonify(resp.json())

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
