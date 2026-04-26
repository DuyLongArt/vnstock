from vnstock import Vnstock
import pandas as pd

v = Vnstock()

print("--- Testing VNINDEX ---")
try:
    # Most sources handle indices if the ticker is right
    idx = v.stock(symbol='VNINDEX', source='VCI')
    print("VCI VNINDEX Historical:")
    print(idx.trading.historical_data('2024-04-01', '2024-04-26', '1D').tail(2))
except Exception as e:
    print(f"VNINDEX VCI failed: {e}")

try:
    idx_kbs = v.stock(symbol='VNINDEX', source='KBS')
    print("\nKBS VNINDEX Price Board:")
    print(idx_kbs.trading.price_board())
except Exception as e:
    print(f"VNINDEX KBS failed: {e}")

print("\n--- Testing World Index (DJI) ---")
try:
    world = v.world_index(symbol='DJI', source='MSN')
    print("DJI History:")
    print(world.quote.history().tail(2))
except Exception as e:
    print(f"DJI failed: {e}")

print("\n--- Testing FX (USDVND) ---")
try:
    # MSN might use different symbols for FX. Let's try EURUSD as per signature
    fx = v.fx(symbol='EURUSD', source='MSN')
    print("EURUSD History:")
    print(fx.quote.history().tail(2))
except Exception as e:
    print(f"FX failed: {e}")

print("\n--- Testing Fund ---")
try:
    f = v.fund(source='FMARKET')
    print("FMARKET Fund List (first 2):")
    # Need to check Fund methods. explorer/fmarket/fund.py
    # Let's try generic methods if any
    print(dir(f))
except Exception as e:
    print(f"Fund failed: {e}")
