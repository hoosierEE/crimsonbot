import crimsonbot as cb
from math import pi
from utime import ticks_us, ticks_diff

class Speedo(object):
    """
    Interrupt-driven monitor for wheel speed.

    Assumes:
    - 2 wheels
    - 16-hole optical interruptor on each wheel
    - Single-phase interruptor (not quadrature)

    Usage:
    s = Speedo(left_opto_pin, right_opto_pin)

    # speed
    [left_speed, right_speed] = getWheelSpeed(2.5, 2.5)  # 2.5cm wheel diameter, result will be in cm per second

    """

    def __init__(self, left_pin, right_pin):
        N=16   # must be power of 2, so that we can use (x & N-1) as a ring buffer index

        # init ring buffers for left and right time measurements
        self.tleft = [0 for i in range(N)]
        self.tright = [0 for i in range(N)]
        start_time = ticks_us()
        self.tleft[-1] = start_time
        self.tright[-1] = start_time
        self.ileft = 0
        self.iright = 0

        # pin and interrupt setup
        self.left_pin = left_pin
        self.right_pin = right_pin
        cb.pinMode(self.left_pin, cb.IN)
        cb.pinMode(self.right_pin, cb.IN)
        left_pin.irq(trigger = cb.Pin.IRQ_RISING, handler = cb_left)
        right_pin.irq(trigger = cb.Pin.IRQ_RISING, handler = cb_right)

    # XXX -- should these disable/re-enable interrupts?
    def cb_left():
        self.tleft[self.ileft & 15] = ticks_us()
        self.ileft += 1
    def cb_right():
        self.tright[self.iright & 15] = ticks_us()
        self.iright += 1

    def dt(a, i):
        # difference between last 2 time measurements, or zero (error: time delta too big)
        prev = a[(i-1) & 15]
        curr = a[i & 15]
        diff = ticks_diff(curr, prev)  # this will be negative if TICKS_PERIOD was exceeded
        return 0 if diff < 0 else diff


    # primary function of this library:
    def deltas():
        # time (microseconds) for 1/16 of a revolution
        return [dt(self.tleft, self.ileft), dt(self.tright, self.iright)]


    # some convenience functions...
    def rps():
        # revolutions per second
        return [x*16/1e6 for x in deltas()]

    def getWheelSpeed(wheel_diameter):
        # <length units of wheel_diameter> per second
        return [x*wheel_diameter*pi for x in rps()]


