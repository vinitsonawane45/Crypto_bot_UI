# import os
# from binance.client import Client
# from binance.enums import *
# from dotenv import load_dotenv

# class TradingBot:
#     def __init__(self):
#         load_dotenv()
#         self.api_key = os.getenv('BINANCE_TESTNET_API_KEY')
#         self.secret_key = os.getenv('BINANCE_TESTNET_SECRET_KEY')
#         self.client = None
#         self.connect()

#     def connect(self):
#         try:
#             if not self.secret_key: raise Exception("Secret Key Missing")
#             self.client = Client(self.api_key, self.secret_key, testnet=True)
#             return True
#         except:
#             return False

#     def get_balance(self):
#         try:
#             info = self.client.futures_account()
#             for asset in info['assets']:
#                 if asset['asset'] == 'USDT':
#                     return float(asset['walletBalance'])
#             return 0.0
#         except:
#             return 0.0

#     def execute_trade(self, side, symbol="BTCUSDT", qty=0.002):
#         try:
#             order = self.client.futures_create_order(
#                 symbol=symbol,
#                 side=side,
#                 type=FUTURE_ORDER_TYPE_MARKET,
#                 quantity=qty
#             )
#             return {"status": "success", "price": order.get('avgPrice', 'Market'), "id": order['orderId']}
#         except Exception as e:
#             return {"status": "error", "msg": str(e)}




import os
import time
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv


class TradingBot:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        self.secret_key = os.getenv("BINANCE_TESTNET_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise Exception("API key or secret key missing")

        self.client = None
        self.connect()

    def connect(self):
        self.client = Client(
            self.api_key,
            self.secret_key,
            testnet=True
        )

        # ---- FIX TIMESTAMP (-1021) ----
        server_time = self.client.get_server_time()["serverTime"]
        local_time = int(time.time() * 1000)
        self.client.timestamp_offset = server_time - local_time

        self.client.REQUEST_RECVWINDOW = 10000

        # Validate credentials
        self.client.futures_account_balance()

        # Set leverage
        self.client.futures_change_leverage(
            symbol="BTCUSDT",
            leverage=10
        )

    def get_balance(self):
        info = self.client.futures_account()
        for asset in info["assets"]:
            if asset["asset"] == "USDT":
                return float(asset["walletBalance"])
        return 0.0

    def execute_trade(self, side, symbol="BTCUSDT", qty=0.002):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=qty
            )

            order_id = order["orderId"]

            # Fetch executed order
            order_info = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )

            avg_price = float(order_info["avgPrice"])

            return {
                "status": "FILLED",
                "side": side,
                "price": avg_price if avg_price > 0 else "MARKET",
                "order_id": order_id
            }

        except BinanceAPIException as e:
            # 🔥 THIS IS THE IMPORTANT PART
            return {
                "status": "REJECTED",
                "error_code": e.code,
                "error_msg": e.message
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "error_msg": str(e)
            }


# ---------------- TEST ----------------
if __name__ == "__main__":
    bot = TradingBot()

    result = bot.execute_trade(SIDE_BUY)

    if result["status"] == "FILLED":
        print("[SIMULATION] ORDER FILLED")
        print(f"{result['side']} @ {result['price']}")
        print(f"ID: {result['order_id']}")
    else:
        print("✖ ORDER REJECTED")
        print(result["error_msg"])
