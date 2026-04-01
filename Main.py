import asyncio
import os
from metaapi_cloud_sdk import MetaApi
import datetime

# --- الإعدادات الأسطورية (تأكد من وضع بياناتك الصحيحة هنا) ---
API_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NGY5NzUzMThmZjYxYjQwNjkwZDlmYWZhYTIzMTA3NyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiNDRmOTc1MzE4ZmY2MWI0MDY5MGQ5ZmFmYWEyMzEwNzciLCJpYXQiOjE3NzUwODA4MzYsImV4cCI6MTc4Mjg1NjgzNn0.Dbah9AsS9TfBtEm-I5k8_WBT35y72FjghvPjtdnni27WrC5-_SjyrUfZsfRQUoJBLkFCA__NdmGAtMfFnGzmiMTdN40EtzPv-TwEs1utD4xBYAsHDDduOv8rkp5sMYdWDXDUICX9BJ0ZrWh4OF80D-mzhx3Vo32zz7ikuLA4U3HZ51cGFlACN8ZQzTDQcOLQZDUsI9JbwpMRpBRA4npsAoJYz8A3na_mK2bNlb5e4XXf-A6AE9YMs_1g7VlX9y03h1QXRq6CglaB1Pxk4sQbnD_hl7o04JEZcTLwYzkgbxdw1BZ28Ti3i3aiYy3KtaQ5NBUn-ga5_RyiCaSHXmc8Vr68B8ZmtbBwPnaGq4lU7lCPr7jOJ9sWViySsgk7YLAKKdupmoYdKcCiXZcrEjQUpUOkgBz_-bdeBsVym7gUAb9rX1ILMmKY5GQmGKQ_yV4nkzd_JXGuOIpcEElt6v58Xsx0jbg3tbtrxxJUdH0hqacScTWLjifOzrRrh6q1oaDFRFW7VMrRHupiqCmf-z4i8FWrot7xUJNiVzokxrpw6flt5OdXwTcfPypvDv8kxIcfZm4Du4_CBB4n4rVLaBfgd6yNkjH5ygObsrJRU9hhHrtQvQmyB_siTLrYP4ivNTwyFglVBIxwi4ZEat_90uvJVtqAgs9zJBn-oZ4p8BtNOGM" # التوكن الذي نسخته
ACCOUNT_ID = "260d9abb-8251-439c-bb45-f5d72add80c1" # الآيدي الخاص بك في MetaApi
SYMBOL = "XAGUSD"
RISK_PERCENT = 0.01  # مخاطرة 1% من الرصيد
MAGIC_NUMBER = 999999

async def run_bot():
    api = MetaApi(API_TOKEN)
    try:
        # الاتصال بالحساب عبر السحاب
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        await account.wait_connected()
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        print(f"✅ الوحش الأسطوري متصل الآن ويراقب {SYMBOL} في السحاب...")

        while True:
            try:
                # 1. جلب بيانات فريم الساعة (H1) لتمثيل "القائد"
                h1_candles = await connection.get_candles(SYMBOL, '1h', None, 1)
                if not h1_candles: continue
                h1 = h1_candles[0]
                h1_open = h1['open']
                h1_low = h1['low']
                h1_high = h1['high']

                # 2. جلب بيانات فريم 5 دقائق (M5) لتمثيل "القناص"
                m5_candles = await connection.get_candles(SYMBOL, '5m', None, 2)
                if len(m5_candles) < 2: continue
                m5_current_close = m5_candles[0]['close']
                m5_prev_close = m5_candles[1]['close']

                # 3. جلب السعر اللحظي
                price_info = await connection.get_symbol_price(SYMBOL)
                current_bid = price_info['bid']
                current_ask = price_info['ask']

                # جلب رصيد الحساب لحساب اللوت
                account_information = await connection.get_account_information()
                balance = account_information['balance']

                # --- منطق الشراء (الارتداد من ذيل ساعة هابط) ---
                # الشرط: السعر صنع ذيلاً تحت افتتاح الساعة + عاد للافتتاح + M5 صاعد
                if h1_low < h1_open - 0.02:
                    if current_ask >= h1_open and m5_current_close > m5_prev_close:
                        sl = h1_low - 0.01
                        risk_dist = abs(current_ask - sl)
                        
                        if risk_dist > 0:
                            tp = current_ask + (risk_dist * 2) # هدف 2:1
                            # حساب اللوت بناءً على المخاطرة
                            lot = round((balance * RISK_PERCENT) / (risk_dist * 50), 2)
                            lot = max(0.01, min(lot, 10.0)) # حدود اللوت

                            print(f"🔥 إشارة شراء أسطورية! لوت: {lot} | SL: {sl} | TP: {tp}")
                            await connection.create_market_buy_order(SYMBOL, lot, sl, tp, {"comment": "Legendary Buy"})
                            await asyncio.sleep(3600) # الانتظار للساعة القادمة لمنع تكرار الصفقات

                # --- منطق البيع (الارتداد من ذيل ساعة صاعد) ---
                elif h1_high > h1_open + 0.02:
                    if current_bid <= h1_open and m5_current_close < m5_prev_close:
                        sl = h1_high + 0.01
                        risk_dist = abs(sl - current_bid)
                        
                        if risk_dist > 0:
                            tp = current_bid - (risk_dist * 2)
                            lot = round((balance * RISK_PERCENT) / (risk_dist * 50), 2)
                            lot = max(0.01, min(lot, 10.0))

                            print(f"❄️ إشارة بيع أسطورية! لوت: {lot} | SL: {sl} | TP: {tp}")
                            await connection.create_market_sell_order(SYMBOL, lot, sl, tp, {"comment": "Legendary Sell"})
                            await asyncio.sleep(3600)

            except Exception as error:
                print(f"❌ خطأ أثناء المراقبة: {error}")
            
            # فحص كل 15 ثانية للحفاظ على موارد السيرفر
            await asyncio.sleep(15)

    except Exception as e:
        print(f"❌ فشل الاتصال النهائي: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())
