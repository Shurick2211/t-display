import gc
import urequests

def get_crypto_price():
  while True:
    gc.collect()
    print(f"mem = {gc.mem_free()}")
    try:
      url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd"
      data = urequests.get(url).json()
      print("Crypto price: " + str(data))
      return data
    except Exception as e:
      print( f"Error crypto: {str(e)}")
      return None
