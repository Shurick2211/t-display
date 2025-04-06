import gc
import time
from time import sleep

import fonts.vector.scripts as font_g

import st7789
from command_handler import running_command, measured
from tdisplay_esp32.tft_config import config
from wifi_connection import connect_wifi, create_ap

wlan = None

def loop(sc:st7789.ST7789):
    while True:
        running_command(sc, wlan)
        time.sleep(0.2)
        gc.collect()


def async_start_server():
    pass


def start():
    print("Program started!")
    global wlan
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
    sleep(1)

    print(f"Free mem = {gc.mem_free()}")
    loop(screen)


start()
