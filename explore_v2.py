from vnstock import Vnstock

v = Vnstock()
print("Vnstock Attributes:", [a for a in dir(v) if not a.startswith('__')])

# Exploring common features from the user request
try:
    print("Market:", dir(v.market) if hasattr(v, 'market') else "No market")
except: pass

try:
    print("General:", dir(v.general) if hasattr(v, 'general') else "No general")
except: pass

try:
    print("Futures:", dir(v.futures) if hasattr(v, 'futures') else "No futures")
except: pass

try:
    print("News:", dir(v.news) if hasattr(v, 'news') else "No news")
except: pass
