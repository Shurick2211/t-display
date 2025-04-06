import time
from time import sleep
import ntptime

TZ_OFFSET = 2 * 3600

current_time = None

def set_time():
  try:
    ntptime.settime()
    print("Time updated successfully")
  except Exception as e:
    print("Failed to update time:", e)


def set_time_periodically():
  global current_time
  if current_time is None:
    get_current_time()

  if current_time and current_time[3] % 4 == 0 and current_time[4] == 0 and current_time[5] == 0:
    set_time()
    sleep(1)


def get_current_time():
  global current_time
  try:
    current_time = time.localtime(time.time() + TZ_OFFSET)
    formated_date = "{:02}/{:02}/{:02}".format(current_time[2], current_time[1], current_time[0]%100)
    formatted_time = "{:02}:{:02}".format(current_time[3], current_time[4])
    return str(formated_date) + " "+ str(formatted_time)
  except Exception as e:
    print(f"Time error: {str(e)}")
    return "..:.."
