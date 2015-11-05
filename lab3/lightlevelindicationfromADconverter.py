import spidev
import time

spi =spidev.SpiDev()

spi.open(0,0)

while True:
    brightness = spi.xfer2([0x1, 0x08, 0x00])
    print "Brightness =", str(brightness[1] & 0x3), str(brightness[2])
    time.sleep(1)

