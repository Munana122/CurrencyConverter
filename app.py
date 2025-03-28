from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)
CORS(app)


API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

def get_exchange_rate(base_currency, target_currency):
    """Fetches exchange rate from base_currency to target_currency."""
    response = requests.get(BASE_URL + base_currency)
    data = response.json()

    if response.status_code != 200:
        return {"error": data.get("error-type", "Unknown error")}

    rates = data.get("conversion_rates", {})
    if target_currency not in rates:
        return {"error": "Invalid target currency"}

    return {"rate": rates[target_currency]}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["GET"])
def convert_currency():
    """API Endpoint: Converts currency based on user input"""
    base_currency = request.args.get("from")
    target_currency = request.args.get("to")
    amount = request.args.get("amount")

    if not base_currency or not target_currency or not amount:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    exchange_data = get_exchange_rate(base_currency.upper(), target_currency.upper())

    if "error" in exchange_data:
        return jsonify(exchange_data), 400

    converted_amount = amount * exchange_data["rate"]
    
    return jsonify({
        "from": base_currency.upper(),
        "to": target_currency.upper(),
        "amount": amount,
        "converted_amount": round(converted_amount, 2)
    })

@app.route("/currencies", methods=["GET"])
def get_currencies():
    """Fetches the list of available currencies from ExchangeRate-API."""
    response = requests.get(BASE_URL + "USD")  # Default to USD to get currency list
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch currencies"}), 500

    currencies = list(data.get("conversion_rates", {}).keys())
    return jsonify({"currencies": currencies})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
