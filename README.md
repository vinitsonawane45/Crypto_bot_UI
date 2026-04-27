# 🤖 Crypto Bot

A web-based **Cryptocurrency Trading Bot Dashboard** built with **Python (Flask)** on the backend and **HTML/CSS/JavaScript** on the frontend. It connects to the **Binance Futures Testnet** and provides a clean UI to monitor your account balance, execute live BUY/SELL trades, and toggle the bot on or off — all from your browser.

---

## 📸 Preview

> _A real-time trading dashboard with bot toggle, balance display, and manual trade execution controls._

---

## 🚀 Features

- 🔗 **Binance Futures Testnet Integration** — connects securely using your API credentials
- 💰 **Live Balance Display** — fetches real-time USDT wallet balance from your futures account
- 📈 **Manual BUY / SELL Execution** — place market orders for BTCUSDT directly from the UI
- 🔁 **Bot ON/OFF Toggle** — enable or disable the bot before executing any trades
- ⚙️ **Auto Leverage Setup** — automatically sets 10x leverage on BTCUSDT at startup
- 🕒 **Timestamp Sync Fix** — resolves Binance `-1021` timestamp errors automatically
- 🛡️ **Robust Error Handling** — catches `BinanceAPIException` and returns structured error responses
- 📋 **Trade Logging** — activity is logged to `trading_bot.log`

---

## 🗂️ Project Structure

```
Crypto_bot_UI/
│
├── app.py                  # Flask web server & API routes
├── trading_core.py         # Binance client logic (TradingBot class)
├── trading_bot.log         # Runtime trade activity log
│
├── templates/
│   └── index.html          # Main dashboard HTML template
│
├── static/
│   ├── style.css           # Dashboard styling
│   └── script.js           # Frontend JS (API calls, UI updates)
│
├── .gitignore
└── .vscode/                # VS Code editor settings
```

---

## 🧱 Tech Stack

| Layer      | Technology                     |
|------------|-------------------------------|
| Backend    | Python 3, Flask                |
| Frontend   | HTML5, CSS3, JavaScript (ES6)  |
| Exchange   | Binance Futures Testnet API    |
| Libraries  | `python-binance`, `python-dotenv` |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vinitsonawane45/Crypto_bot_UI.git
cd Crypto_bot_UI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask python-binance python-dotenv
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```env
BINANCE_TESTNET_API_KEY=your_testnet_api_key_here
BINANCE_TESTNET_SECRET_KEY=your_testnet_secret_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

To get testnet credentials, visit: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

### 5. Run the App

```bash
python app.py
```

Open your browser at: **[http://localhost:5000](http://localhost:5000)**

---

## 🔌 API Endpoints

| Method | Endpoint       | Description                              |
|--------|---------------|------------------------------------------|
| `GET`  | `/`           | Renders the main dashboard UI            |
| `GET`  | `/api/balance` | Returns current USDT futures balance    |
| `POST` | `/api/trade`   | Executes a BUY or SELL market order     |
| `POST` | `/api/toggle`  | Toggles the bot ON or OFF               |

### `/api/trade` — Request Body

```json
{
  "side": "BUY"   // or "SELL"
}
```

### `/api/trade` — Response (Success)

```json
{
  "status": "FILLED",
  "side": "BUY",
  "price": 68432.50,
  "order_id": 123456789
}
```

### `/api/trade` — Response (Error)

```json
{
  "status": "REJECTED",
  "error_code": -2019,
  "error_msg": "Margin is insufficient."
}
```

---

## 💡 How It Works

1. **On startup**, `TradingBot` loads your API keys from `.env`, connects to the Binance Futures Testnet, syncs the local clock with the server to prevent timestamp errors, and sets 10x leverage on BTCUSDT.

2. **The Flask server** exposes REST endpoints that the frontend JavaScript calls via `fetch`.

3. **The UI** displays your balance and allows you to toggle the bot active state. Only when the bot is `ON` will trade requests be forwarded to Binance.

4. **Trade results** (filled price, order ID, errors) are returned as JSON and displayed in the dashboard.

---

## 🔒 Security Notes

- All trades run on the **Binance Futures Testnet** — no real money is at risk.
- API keys are stored in a `.env` file and loaded via `python-dotenv`, never hardcoded.
- The bot must be explicitly toggled ON before any trade executes.

---

## 🐛 Known Issues / Troubleshooting

| Issue | Fix |
|-------|-----|
| `-1021` Timestamp error | Handled automatically via server time sync in `connect()` |
| `API key missing` error | Ensure `.env` file exists with valid keys |
| Balance shows `0.0` | Check that testnet account has funded USDT balance |
| `Bot is OFF` error on trade | Toggle the bot ON from the UI first |

---

## 🛣️ Roadmap / Future Improvements

- [ ] Add automated trading strategy (RSI, MACD, Moving Average)
- [ ] Live price chart with WebSocket feed
- [ ] Trade history table with P&L tracking
- [ ] Email/Telegram alerts on trade execution
- [ ] Docker support for easy deployment

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change, then submit a pull request.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Vinit Sonawane**
- GitHub: [@vinitsonawane45](https://github.com/vinitsonawane45)

---

> ⚠️ **Disclaimer:** This project is for educational purposes only. Cryptocurrency trading involves significant financial risk. Always trade responsibly and never risk funds you cannot afford to lose.
