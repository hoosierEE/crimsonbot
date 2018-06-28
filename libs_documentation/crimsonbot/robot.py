from crimsonbot import *

d = 1
l = 0
r = 100

def setup():
    pass

def loop():
    global d, l, r
    l += d
    r -= d
    if l == 100:
        d = -1
    if r == 100:
        d = 1
    
    setSpeed(LEFT, l)
    setSpeed(RIGHT, r)
    delay(10)
