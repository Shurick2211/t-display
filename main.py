import gc
import time

import st7789
from command_handler import running_command, picture
from tdisplay_esp32.tft_config import config
from wifi_connection import connect_wifi

def loop(sc:st7789.ST7789):
    while True:
        running_command(sc)
        time.sleep(0.2)
        gc.collect()

def start():
    print("Program started!")

    screen = config()
    screen.init()
    picture(screen)

    wlan = connect_wifi()

    screen.rotation(1)
    screen.fill(st7789.BLACK)
    gc.collect()

    loop(screen)


start()
