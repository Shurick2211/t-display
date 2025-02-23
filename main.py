import gc
import time

import st7789
from command_handler import running_command, picture, measured
from tdisplay_esp32.tft_config import config
from wifi_connection import connect_wifi
import fonts.vector.scripts as font_g

def loop(sc:st7789.ST7789):
    while True:
        running_command(sc)
        time.sleep(0.2)
        gc.collect()

def start():
    print("Program started!")

    screen = config()
    screen.init()
    screen.rotation(1)
    screen.jpg("jpg/bigbuckbunny-240x135.jpg", 0, 0, st7789.SLOW)
    screen.draw(font_g, "Wait!", 60, 80, st7789.WHITE, 2.0)
    wlan = connect_wifi()

    screen.rotation(1)
    screen.fill(st7789.BLACK)
    gc.collect()
    measured(screen)
    loop(screen)


start()
