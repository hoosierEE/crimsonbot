
print("Configuring the Crimsonbot microcontroller...")

PASS = None
while not PASS:
    PASS = input("webREPL password: ")
    if input("Confirm password: ") != PASS:
        print("Password did not match")
        PASS = None

NAME = input("Name your robot: ")

f = open('webrepl_cfg.py', 'w')
f.write("PASS = '{}'\n".format(PASS))
f.write("NAME = '{}'\n".format(NAME))
f.close()
