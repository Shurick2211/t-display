
import network
import time
import ntptime
import ujson

networks = None

def connect_wifi(wifi_ssid="___", wifi_password="____"):
  global networks
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  time.sleep(1)
  networks = wlan.scan()
  print(networks)
  print("Try to connect to Wi-Fi...")
  try:
    wlan.connect(wifi_ssid, wifi_password)
    for _ in range(10):
      time.sleep(1)
      if wlan.isconnected():
        break
    if wlan.isconnected():
      ssid = wlan.config('essid')
      print(f"Connected to: {ssid}")
      print(f"Connected! IP: {wlan.ifconfig()[0]}")
      ntptime.settime()
      return wlan
    else:
      print("Don`t connect to Wi-Fi! " + wlan.status())
      wlan.disconnect()
      return None
  except Exception as e:
    print(f"Error connection: {e}")
    return None


def create_ap(start_host="192.168.5.1", get_way = "192.168.5.1",ssid="ESP32_AP", password="12345678"):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
    ap.ifconfig((start_host, "255.255.255.0", get_way, "8.8.8.8"))
    return ap


def rssi_to_signal_level(rssi):
  if rssi >= -50:
    return '|||||'
  elif rssi >= -60:
    return '||||'
  elif rssi >= -70:
    return '|||'
  elif rssi >= -80:
    return '||'
  else:
    return '|'

def scan_wifi():
  global networks
  result = {
    "message": [
      {
        "ssid": net[0].decode(),  # SSID (Network Name)
        "signal": rssi_to_signal_level(net[3]),  # Signal strength
      }
      for net in networks
    ]
  }

  return ujson.dumps(result)