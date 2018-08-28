import crimsonbot as cb
from machine import Pin

rsens = Pin(14, Pin.IN)
lsens = Pin(12, Pin.IN)
DARK = 1
LITE = 0
spd = 100
dly = 20

def rdar():
    return rsens.value() == DARK

def ldar():
    return lsens.value() == DARK

def line():
    while True:
        ld = ldar()
        rd = rdar()
        if ld and rd:
            cb.forward(-spd)
            cb.delay(20)
            while ldar() and rdar():
                cb.stop()
        else:
            if ld:
                cb.left(spd // 2)
            elif rd:
                cb.right(spd // 2)
            else:
                cb.forward(spd)

        cb.delay(dly)

# line()
def powerstop(t):
    cb.forward(-spd)
    cb.delay(t)
    cb.stop()

def test():
    cb.forward(spd)
    while True:
        ld = ldar()
        rd = rdar()
        if ld or rd:
            powerstop(100)
            return

        cb.delay(0)

test()

