from machine import Pin
import dht

def dht_sensor_read():
  dht_sensor = dht.DHT22(Pin(25, Pin.IN))
  dht_sensor.measure()
  # print(str(dht_sensor.temperature()) + " & " + str(dht_sensor.humidity()))
  TMP = f"T: {str(dht_sensor.temperature())}`C     "
  HUM = f"H: {str(dht_sensor.humidity())}%       "
  return TMP, HUM