import spidev, time

spi = spidev.SpiDev()
spi.open(0,0)

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    print(r)
    adc_out = ((r[1]&3) << 8) + r[2]
    print(adc_out)
    return adc_out


while True:
    reading1 = analog_read(0)
    voltage1 = reading1 * 3.3 / 1024
    print("(0)Reading=%d\tVoltage=%f" % (reading1, voltage1))
    time.sleep(1)

    reading2 = analog_read(1)
    voltage2 = reading2 * 3.3 / 1024
    print("(1)Reading=%d\tVoltage=%f" % (reading2, voltage2))
    time.sleep(1)
