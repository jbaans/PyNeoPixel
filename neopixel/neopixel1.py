#!/usr/bin/python
import struct
import serial
import time

class NeoPixel(object):
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, 115200, timeout=60)
        self.command_count = 0

    def setPixelColor(self, pixel, red, green, blue):
        message = struct.pack('>BBBHBBB', ord(':'), self.command_count, ord('c'), pixel, red, green, blue)
        self.command_count += 1
        if self.command_count >=255:
            self.command_count = 0
        self.ser.write(message)
        response = self.ser.readline()

    def show(self):
        message = struct.pack('BBB', ord(':'), self.command_count, ord('s'))
        self.command_count += 1
        self.ser.write(message)
        response = self.ser.readline()


if __name__ == "__main__":
    import sys

    strand = NeoPixel(sys.argv[1])
    numpixels = 64
    numrows = 8
    numcolumns = numpixels / numrows
    
    # rotate through all pixels twice
    for i in range(2*numpixels):
        w = i % numpixels
        x = (i + 1) % numpixels
        y = (i + 2) % numpixels
        z = (i + 3) % numpixels
        strand.setPixelColor(w, 0, 0, 0)
        strand.setPixelColor(x, 255, 0, 0)
        strand.setPixelColor(y, 0, 255, 0)
        strand.setPixelColor(z, 0, 0, 255)
        strand.show()
        time.sleep(0.01)

    strand.setPixelColor(0, 0, 0, 0)
    strand.setPixelColor(1, 0, 0, 0)
    strand.setPixelColor(2, 0, 0, 0)
    strand.show()

    # switch rows on and off one by one
    for row in range(numrows):
        # row on
        for column in range(numcolumns):
            i = row * numcolumns + column
            strand.setPixelColor(i, 255, 0, 0)
        strand.show()
        time.sleep(0.5)
        # row off
        for column in range(8):
            i = row * numcolumns + column
            strand.setPixelColor(i, 0, 0, 0)
        strand.show()
