import gc
import time

import fonts.vector.romant as font_g

import sensor
import st7789
from crypto_price import get_crypto_price
from my_server import server_handler
from tdisplay_esp32.tft_buttons import Buttons
from time_utils import starting_time, set_time_periodically


button_up = Buttons().right
button_down = Buttons().left
isPic = False
isCrypto = False

def running_command(sc:st7789.ST7789, wlan):
  cur_seconds = time.time()
  global isPic
  global isCrypto
  if not isPic and not isCrypto and cur_seconds % 10 == 0:
    measured(sc)
  if button_up.value() == 0:
    print("UP")
    if not isPic and not isCrypto:
      picture(sc)
    elif(isCrypto):
      sc.fill(st7789.BLACK)
      measured(sc)

  if button_down.value() == 0:
    print("DOWN")
    if isPic:
      sc.rotation(1)
      sc.fill(st7789.BLACK)
      measured(sc)
    else:
      sc.fill(st7789.BLACK)
      crypto(sc)
  set_time_periodically()
  server_handler()

def measured(sc:st7789.ST7789):
  global isCrypto
  isCrypto = False
  global isPic
  isPic = False
  gc.collect()
  starting_time(sc)
  dht_read(sc)


def dht_read(sc:st7789.ST7789):
  TMP, HUM = sensor.dht_sensor_read()
  sc.fill_rect(35,40, 78, 80, st7789.BLACK)
  sc.draw(font_g,TMP , 0, 60, st7789.RED)
  sc.draw(font_g, HUM, 0, 100, st7789.BLUE)

def picture(screen: st7789.ST7789):
  global isPic
  isPic = True
  screen.rotation(0)
  screen.jpg("jpg/flat-lay-gift-concept-mini.jpg", 0, 0, st7789.SLOW)

def crypto(sc:st7789.ST7789):
  global isCrypto
  isCrypto = True
  price = get_crypto_price()
  btc = f"Btc: {price["bitcoin"]["usd"]}$ "
  eth = f"Eth: {price["ethereum"]["usd"]}$"
  xpr = f"Xpr: {price["ripple"]["usd"]}$  "
  sc.draw(font_g, btc, 0, 20, st7789.MAGENTA)
  sc.draw(font_g, eth, 0, 60, st7789.CYAN)
  sc.draw(font_g, xpr, 0, 100, st7789.YELLOW)