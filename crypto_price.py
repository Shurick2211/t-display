import urequests


def get_crypto_price():
  try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd"
    response = urequests.get(url)
    data = response.json()
    print("Crypto price: " + str(data))
    return data
  except Exception as e:
    print( f"Error crypto: {str(e)}")
    return None