'''extremely brittle line follower'''

# This code ran during LuddyFest demo time on 12 April 2018.
# It demonstrates line following using the bare minimum of facilities:
# 2 reflectance sensors (digital)
# 2 motors
# system timer (delay)

import crimsonbot as cb #pylint:disable=import-error

L = 6
R = 7

cb.pinMode(L, cb.IN)
cb.pinMode(R, cb.IN)

spd = -60  # NOTE -- motors were wired backward; this is a hack
slow = -50
dly = 20

def correct(direction):
    if direction == 0:
        cb.right(slow)
        cb.delay(dly)
    else:
        cb.left(slow)
        cb.delay(dly+10)

def drive():
    while True:
        if cb.read(L) and cb.read(R):  # both sense "line" a.k.a. no reflection (empty space also)
            cb.stop()
        elif cb.read(R): # line on right, go left
            correct(0)
        elif cb.read(L): # line on left, go right
            correct(1)
        else:
            cb.forward(spd)
        cb.delay(dly)
