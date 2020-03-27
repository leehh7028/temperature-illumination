#!/usr/bin/env python
import spidev, time
from pi_sht1x import SHT1x
import RPi.GPIO as GPIO
import pymysql

class sensorToDB():
    def __init__(self):
        #SETTING RASPBERRY PI SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)

        #MYSQP INFO
        self.url = "210.115.227.108"
        self.id = 'cic'
        self.password = '20180903in'
        self.dbName = 'kindergartenbus'

    def analog_read(self, channel):
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((r[1]&3) << 8) + r[2]
        return adc_out

    def i2c_read(self, sensor, type):
        if type is "all":
            t = sensor.read_temperature()
            h = sensor.read_humidity()
            return [t, h]
        elif type is "humi":
            return sensor.read_humidity()
        elif type is "temp":
            return sensor.read_temperature()
        else:
            return "0"


    def data_Transmitting(self):
        illum = self.analog_read(0)
        time.sleep(1)
        try :
            sensor = SHT1x(26, 20, gpio_mode=GPIO.BCM)
            temp, humi = self.i2c_read(sensor, "all")
        finally:
            print("gpio clean up")
            GPIO.cleanup()
        self.db = pymysql.connect(host=self.url, port=3306, user=self.id, passwd=self.password, db=self.dbName,
                                  charset='utf8')
        self.cursor = self.db.cursor()

        sql = "INSERT INTO `sensor_data` (`temp`, `humi`, `illum`, `time`) VALUES ('" + str(temp) + "', '" + str(humi) + "', '" + str(illum) + "', CURRENT_TIMESTAMP);"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()

obj = sensorToDB()
while True:
    obj.data_Transmitting()
    print("transmission success")
    time.sleep(5)

