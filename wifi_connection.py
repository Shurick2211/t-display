
import network
import time
import ntptime



def connect_wifi(wifi_ssid="___", wifi_password="___"):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  time.sleep(1)
  result = wlan.scan()
  print(result)
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


# def create_ap(start_host="192.168.5.1", ssid="ESP32_AP", password="12345678"):
#     ap = network.WLAN(network.AP_IF)
#     ap.active(True)
#     ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
#     ap.ifconfig((start_host, "255.255.255.0", start_host, "8.8.8.8"))
#     return ap
#
#
# def create_wifi(wan_ssid="HSnet", wan_password="ytdktpfqe,mtn"):
#     wlan_in = connect_wifi(wifi_ssid=wan_ssid, wifi_password=wan_password)
#     ap = create_ap()
#  #   _thread.start_new_thread(forward_packets, (wlan_in, ap))
#     return wlan_in, ap

