import time

import ntptime
import fonts.bitmap.vga1_16x32 as font
import st7789

TZ_OFFSET = 2 * 3600


def set_time():
  ntptime.settime()


def get_current_time():
  try:
    current_time = time.localtime(time.time() + TZ_OFFSET)
    formatted_time = "{:02}:{:02}".format(current_time[3], current_time[4])
    return "Time: " + str(formatted_time)
  except Exception as e:
    print(f"Time error: {str(e)}")
    return None


def starting_time(sc:st7789.ST7789):
  sc.text(font, get_current_time(), 0, 0, st7789.GREEN)
  # print(get_current_time())

