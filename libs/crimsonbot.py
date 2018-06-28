'''crimsonbot motor library'''
import sys
import gc
from utime import sleep_ms as delay  # pylint: disable=import-error
from machine import Pin, PWM  # pylint: disable=import-error
############
VERSION = "1.3.0"
############

IN = 0
OUT = 1
OPEN_DRAIN = 2
PULL_UP = 3

LEFT = 0
RIGHT = 1
_pins = {}
_motors = []

def pinMode(p, mode):
    _pins[p] = Pin([16, 5, 4, 0, 2, 14, 12, 13, 15][p],
                   [Pin.IN, Pin.OUT, Pin.OPEN_DRAIN, Pin.PULL_UP][mode])

def _enable_motors(f):
    def _f(*args, **kwargs):
        global _motors
        if not _motors:
            _lmotor = (PWM(Pin(5), freq=50), Pin(0, Pin.OUT))
            _rmotor = (PWM(Pin(4), freq=50), Pin(2, Pin.OUT))
            _motors = [_lmotor, _rmotor]
        return f(*args, **kwargs)
    return _f

def read(p):
    return _pins[p].value()
def write(p, v):
    _pins[p].value(v)
def analogWrite(p, v):
    if not isinstance(_pins[p], PWM):
        _pins[p] = PWM(_pins[p], freq=50)
    _pins[p].duty(v)

def forward(speed):
    setSpeed(LEFT, speed)
    setSpeed(RIGHT, speed)

def left(speed):
    setSpeed(RIGHT, speed)
    setSpeed(LEFT, 0)

def right(speed):
    setSpeed(RIGHT, 0)
    setSpeed(LEFT, speed)

def pivotLeft(speed):
    setSpeed(RIGHT, speed)
    setSpeed(LEFT, 0 - speed)

def pivotRight(speed):
    setSpeed(RIGHT, 0 - speed)
    setSpeed(LEFT, speed)

def stop():
    forward(0)

@_enable_motors
def setSpeed(side, speed):
    if speed < 0:
        _motors[side][1].off()
    else:
        _motors[side][1].on()
    speed = (1023 * abs(speed)) // 100
    _motors[side][0].duty(speed)

def reset_modules():
    keep = ['crimsonbot', 'webrepl', 'webrepl_cfg', 'flashdev', 'websocket_helper', 'net_cfg']
    for module in sys.modules:
        if module not in keep:
            del sys.modules[module]

def run(wait=1):
    import robot  # pylint: disable=import-error
    try:
        robot.setup()
        while True:
            delay(wait)
            robot.loop()
    except:
        raise
    finally:
        stop()
        gc.collect()
        del sys.modules['robot']
