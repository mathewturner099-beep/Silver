import asyncio
from metaapi_cloud_sdk import MetaApi
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- البيانات الخاصة بك ---
API_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NGY5NzUzMThmZjYxYjQwNjkwZDlmYWZhYTIzMTA3NyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiNDRmOTc1MzE4ZmY2MWI0MDY5MGQ5ZmFmYWEyMzEwNzciLCJpYXQiOjE3NzUwODcxNTAsImV4cCI6MTc4Mjg2MzE1MH0.Mtwgyj1yBfJAb7frHIznfmI-BdaU3CNTdrq7mtiSvrtPJhCq_TzrU-Ax4hR9H5f37hvTS_yT-cMVzyQ0MGsXNLyHHRrsnnl-WBHsFsrq4Bs90HJNzW8iDnFuTWtfFU8L38hkiIGRtdzHdDxDhDEqBKPXJXGOml-wvzofezbOKe-gN5JGg1Gw2VChPsqp02FSF89xNeIL1wUqVRokR-hoq0eHICau92wANPtQEbWAlmg_KPFRuY0RCnW9LudqK_UhRW90uQE1WD3Yzf-jEXIYX29IzwtLPL7AfUUlpb3W9J0bksJEDT6L2yzKsAkx5IxlLkLNjIP3IO6J57tIdKK0yaqnNIklWQoFxl4pdyyuzAddo_HDtzpeqERRPDiINMuwmuSYBZYwqv93YixDjUWouHMIfhadKsyNmscsmCJqtHsBjL6oqscg6R2oqpaquW4kVL4ipYq72ujv3GdAjhrUWbaVvAb1SebUEgUv3LSlZDZCvqrEsXF3wx4VuXlO9Krw66URWPQatV3lYS8vqWDhSBu7RSFU-Fpv6bzeS_VYPN_e_tTUkC599iSc17DdhiZjtvn2K5LdO-LjR1qdvGTaosmSPQNv5UBBTFTHnRukgoZY_bYZIslYItdQi0c1AFXp1G9U8jYKLo3Tzl0f9a2ry_yAjAAtpmdm2GjfTPp2t6I"
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
