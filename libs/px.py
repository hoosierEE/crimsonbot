'''LPD8806 - Micropython library for LED driver chip'''
from machine import Pin, SPI #pylint:disable=import-error

class Px(object):
    '''init with n pixels, set color'''
    def __init__(self, count=16, clk=14, data=13): # 14:D5, 13:D7
        self.spi = None
        # NOTE miso not used but still required by SPI(), so watch out when using D6 a.k.a. Pin(12)
        self.spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(clk), mosi=Pin(data), miso=Pin(12))
        self.spi.init()
        self.count = count  # number of LEDs per strip
        self.pixels = [[128, 128, 128]]*count # list of GRB-lists
        self.latch = (count+31) // 32 # LPD8806 quirk; requires extra latch 0 for every 32 LEDs
        self.show()

    def one(self, n, r, g, b):  # Nth led: red, green, and blue 7-bit values (0-127)
        if n >= self.count:
            return
        clr = [128, 128, 128]
        # GRB
        clr[0] |= g & 0xff
        clr[1] |= r & 0xff
        clr[2] |= b & 0xff
        self.pixels[n] = clr
        self.show()

    def all(self, r, g, b):
        self.pixels = [[128|(g&0xff), 128|(r&0xff), 128|(b&0xff)]]*self.count
        self.show()

    def clear(self):
        self.pixels = [[128, 128, 128]]*self.count
        self.show()

    def show(self):  # draw entire strip
        flat = sum(self.pixels, [])
        for _ in range(0, self.latch):
            flat.append(0)
        bts = bytes(flat)
        self.spi.write(bts)  # flatten -> convert to bytes -> write SPI
