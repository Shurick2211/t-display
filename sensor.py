from machine import Pin, I2C
import dht

import BME280
from ahtx0 import AHT20


def dht_sensor_read():
  dht_sensor = dht.DHT22(Pin(25, Pin.IN))
  dht_sensor.measure()
  # print(str(dht_sensor.temperature()) + " & " + str(dht_sensor.humidity()))
  TMP = f"T: {str(dht_sensor.temperature())}`C     "
  HUM = f"H: {str(dht_sensor.humidity())}%       "
  return TMP, HUM


def move_sensor_read():
  while True:
    m_s = Pin(2, Pin.IN)
    yield m_s.value()


i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=10000)


def bme_read():
  bme = BME280.BME280(i2c=i2c)
  temp = bme.temperature
  pres = bme.pressure2
  print('Temperature: ', temp)
  print('Pressure: ', pres)
  return temp, pres


def aht20_read():
  aht = AHT20(i2c=i2c)
  t = aht.temperature
  h = aht.relative_humidity
  temp = "T={:.02f}'C".format(t)
  hum = "H={:.02f}%".format(h)
  print("\nTemperature: %0.2f C" % t)
  print("Humidity: %0.2f %%" % h)
  return temp, hum
