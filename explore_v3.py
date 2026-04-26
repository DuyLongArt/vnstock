from vnstock import Vnstock
import inspect

v = Vnstock()

print("--- Crypto ---")
try:
    print(v.crypto(symbol='BTC', source='binance').quote.history())
except Exception as e:
    print(f"Crypto failed: {e}")

print("\n--- FX ---")
try:
    # Based on explorer/misc/exchange_rate.py
    # Maybe v.fx()?
    pass
except Exception as e:
    print(f"FX failed: {e}")

print("\n--- Fund ---")
try:
    # Based on explorer/fmarket/fund.py
    pass
except Exception as e:
    print(f"Fund failed: {e}")

print("\n--- Checking v properties ---")
for name in ['crypto', 'fund', 'fx', 'world_index']:
    attr = getattr(v, name)
    print(f"{name}: {type(attr)}")
    # if it's a method, print signature
    if inspect.ismethod(attr):
        print(f"  Signature: {inspect.signature(attr)}")
