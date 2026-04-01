import asyncio
from metaapi_cloud_sdk import MetaApi
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- البيانات الخاصة بك ---
API_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NGY5NzUzMThmZjYxYjQwNjkwZDlmYWZhYTIzMTA3NyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW5"
ACCOUNT_ID = "260d9abb-8251-439c-bb45-f5d72add80c1"
SYMBOL = "XAGUSD"

# --- خادم وهمي لإرضاء منصة Render ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_http_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

# --- منطق التداول السحابي ---
async def trade_logic():
    api = MetaApi(API_TOKEN)
    account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
    await account.wait_connected()
    connection = account.get_rpc_connection()
    await connection.connect()
    
    print("✅ الوحش متصل بالسحاب ويراقب الفضة...")
    
    while True:
        try:
            candles = await connection.get_candles(SYMBOL, '1h', None, 1)
            h1 = candles[0]
            price_info = await connection.get_symbol_price(SYMBOL)
            current_price = price_info['bid']
            
            # استراتيجيتك (الذيل والعودة للافتتاح)
            if h1['low'] < h1['open'] - 0.02 and current_price >= h1['open']:
                print("🎯 اقتناص ذيل سفلي!")
                await connection.create_market_buy_order(SYMBOL, 0.1, h1['low'], h1['open'] + 0.40)
                await asyncio.sleep(3600)
                
            await asyncio.sleep(15)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(15)

if __name__ == "__main__":
    # تشغيل الخادم الوهمي في خيط منفصل
    threading.Thread(target=run_http_server, daemon=True).start()
    # تشغيل البوت
    asyncio.run(trade_logic())
