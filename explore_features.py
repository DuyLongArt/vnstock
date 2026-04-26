from vnstock import Vnstock
import pandas as pd

v = Vnstock()

def test_features():
    print("--- Testing Market Indices ---")
    try:
        # Exploring index data
        # Based on 3.x structure, indices might be under a different component or source
        # Let's try to find an index component
        pass
    except Exception as e:
        print(f"Index error: {e}")

    print("\n--- Testing Crypto ---")
    try:
        # vnstock 3.x often has a 'market' or 'quote' for non-stock assets
        # Let's see if we can get crypto
        pass
    except Exception as e:
        print(f"Crypto error: {e}")

    # I'll use dir() to explore the Vnstock object
    print("\n--- Vnstock Attributes ---")
    print(dir(v))
    
    # Test a stock instance's components
    s = v.stock(symbol='VNM', source='KBS')
    print("\n--- StockComponents Attributes ---")
    print(dir(s))

if __name__ == "__main__":
    test_features()
