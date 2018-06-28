'''library for interacting with the HCSR04 ultrasonic rangefinder'''
#pylint:disable=superfluous-parens, import-error
from machine import Pin, time_pulse_us
from utime import sleep_us, ticks_ms, ticks_diff

class HCSR04(object):
    ''' usage:
        from HCSR04 import HCSR04
        my_sensor = HCSR04()
        dist = my_sensor.cm() '''
    def __init__(self, trig=2, echo=5):
        ''' machine.Pin(2) == D4 on the ESP12E Motor Shield.
            machine.Pin(5) == D1 on the ESP12E Motor Shield. '''
        self.trigPin = Pin(trig, Pin.OUT)
        self.trigPin(0)
        self.echoPin = Pin(echo, Pin.IN)
        self.measured = 0
        self.previous = ticks_ms()

    def trigger_start(self):
        '''LOW for 2us, HIGH for 10us, LOW'''
        self.trigPin(1)
        self.trigPin(0)
        sleep_us(2)
        self.trigPin(1)
        sleep_us(10)
        self.trigPin(0)

    def cm(self):
        '''Distance to reflected object, in cm.
        Error codes:
        -1 out of range
        -2 sensor error
        '''
        # busy-wait until at least 60ms since last reading
        now = ticks_ms()
        while ticks_diff(self.previous, now) < 60:
            now = ticks_ms()
        self.previous = now

        self.trigger_start()

        # Reads the echoPin, `time` gets set to the sound wave travel time in microseconds.
        echo_us = time_pulse_us(self.echoPin, 1, 29000)
        if echo_us < 0:
            return -2
        dist_in_cm = echo_us / 58.0 # ((time / 2.0) / 29)
        if dist_in_cm < 2 or dist_in_cm > 400:
            return -1
        return dist_in_cm

    def test(self):
        '''For testing. Calls `cm` until force-quit. (Ctrl-C)'''
        while True:
            sense = self.cm()
            print("Distance: ", sense, "cm")
            ms = 100# every 100ms
            sleep_us(ms*1e3)
