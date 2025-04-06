import gc
import time
from time import sleep

import fonts.vector.romant as font_g

import fonts.bitmap.vga1_16x32 as font

import sensor
import st7789
from crypto_price import get_crypto_price
from my_ble import BLEUART
from sensor import move_sensor_read
from tdisplay_esp32.tft_buttons import Buttons
from time_utils import set_time_periodically, get_current_time

button_up = Buttons().right
button_down = Buttons().left
isPic = False
isCrypto = False
move_counter = 0
ble_uart = BLEUART("MyESP32")

def running_command(sc:st7789.ST7789, wlan):
  global isPic
  global isCrypto
  global move_counter
  move_listener(sc)
  if not isPic and not isCrypto:
    measured(sc)
  if button_up.value() == 0:
    print("UP")
    if not isPic and not isCrypto:
      picture(sc)
    elif(isCrypto):
      sc.fill(st7789.BLACK)
      measured(sc, True)
  if button_down.value() == 0:
    print("DOWN")
    if isPic:
      sc.rotation(1)
      sc.fill(st7789.BLACK)
      measured(sc, True)
    else:
      wait(sc)
      crypto(sc)
  set_time_periodically()
  # print(f"mem = {gc.mem_free()}")

def move_listener(sc:st7789.ST7789):
  global move_counter
  if move_counter == 0 and next(move_sensor_read()) == 1:
    sc.on()
    print("Move!")
    move_counter += 1
  if move_counter in range(1,100):
    move_counter += 1
  else:
    move_counter = 0
    sc.off()
    # print(f"mem = {gc.mem_free()}")

def wait(sc):
  sc.fill(st7789.BLACK)
  sc.draw(font_g, "WAIT...", 70, 60, st7789.RED)

def measured(sc:st7789.ST7789, after_switch = False):
  cur_seconds = time.time()
  global isCrypto
  isCrypto = False
  global isPic
  isPic = False

  def __display():
    sc.text(font, get_current_time(), 0, 0, st7789.GREEN)
    thp = dht_read(sc)
    sleep(1)
    after_switch = False
    ble_uart.send(str(thp))


  if cur_seconds % 10 == 0:
    __display()
  elif after_switch:
    __display()
  gc.collect()

def dht_read(sc: st7789.ST7789):
  TMP, HUM = sensor.aht20_read()
  T, P = sensor.bme_read()
  sc.fill_rect(43,37, 90, 25, st7789.BLACK)
  sc.draw(font_g,TMP , 0, 50, st7789.RED)
  sc.fill_rect(43, 70, 90, 25, st7789.BLACK)
  sc.draw(font_g, HUM, 0, 82, st7789.BLUE)
  sc.fill_rect(43, 101, 105, 25, st7789.BLACK)
  sc.draw(font_g, P, 0, 115, st7789.YELLOW)
  return TMP, HUM, P

def picture(screen: st7789.ST7789):
  global isPic
  isPic = True
  screen.rotation(0)
  screen.jpg("jpg/flat-lay-gift-concept-mini.jpg", 0, 0, st7789.SLOW)

def crypto(sc:st7789.ST7789):
  global isCrypto
  isCrypto = True
  price = get_crypto_price()
  try:
    btc = f"Btc: {price["bitcoin"]["usd"]}$ "
    eth = f"Eth: {price["ethereum"]["usd"]}$"
    xpr = f"Xpr: {price["ripple"]["usd"]}$  "
    sc.fill(st7789.BLACK)
    sc.draw(font_g, btc, 0, 20, st7789.MAGENTA)
    sc.draw(font_g, eth, 0, 60, st7789.CYAN)
    sc.draw(font_g, xpr, 0, 100, st7789.YELLOW)
  except Exception as e:
    print(e)