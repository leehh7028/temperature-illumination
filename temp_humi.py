from pi_sht1x import SHT1x
import RPi.GPIO as GPIO

with SHT1x(6, 12, gpio_mode=GPIO.BCM) as sensor:
    temp = sensor.read_temperature()
    humidity = sensor.read_humidity(temp)
    sensor.calculate_dew_point(temp, humidity)
    print(sensor)
