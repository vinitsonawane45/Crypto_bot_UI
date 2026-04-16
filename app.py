# from flask import Flask, render_template, jsonify, request
# from trading_core import TradingBot

# app = Flask(__name__)
# bot = TradingBot()

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/api/balance', methods=['GET'])
# def get_balance():
#     bal = bot.get_balance()
#     return jsonify({"balance": f"{bal:,.2f}"})

# @app.route('/api/trade', methods=['POST'])
# def trade():
#     data = request.json
#     side = data.get('side')  # 'BUY' or 'SELL'
#     result = bot.execute_trade(side)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)



from flask import Flask, render_template, jsonify, request
from trading_core import TradingBot

app = Flask(__name__)
bot = TradingBot()

# Simple bot ON/OFF state
BOT_ENABLED = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/balance", methods=["GET"])
def get_balance():
    bal = bot.get_balance()
    return jsonify({
        "status": "OK",
        "balance": f"{bal:,.2f}"
    })


@app.route("/api/trade", methods=["POST"])
def trade():
    global BOT_ENABLED

    if not BOT_ENABLED:
        return jsonify({
            "status": "ERROR",
            "message": "Bot is OFF"
        }), 400

    if not request.is_json:
        return jsonify({
            "status": "ERROR",
            "message": "JSON required"
        }), 400

    data = request.get_json(silent=True)
    side = data.get("side")

    if side not in ["BUY", "SELL"]:
        return jsonify({
            "status": "ERROR",
            "message": "Side must be BUY or SELL"
        }), 400

    result = bot.execute_trade(side)
    return jsonify(result)


@app.route("/api/toggle", methods=["POST"])
def toggle_bot():
    global BOT_ENABLED
    BOT_ENABLED = not BOT_ENABLED

    return jsonify({
        "status": "OK",
        "enabled": BOT_ENABLED,
        "message": "Bot enabled" if BOT_ENABLED else "Bot disabled"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
