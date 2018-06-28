import subprocess

# Read Mac here
out = subprocess.check_output(['esptool.py', '-p', '/dev/ttyUSB0', 'read_mac'])
out = out.split('\n')
for l in out:
    v = l.split(":", 1)
    if len(v) != 1:
        mac = v[1].strip()

flen = 0
with open('inv.dat') as f:
    for l in f:
        pair = l.split()
        if pair[0] == mac:
            print("Mac already in inventory:")
            print(l)
            exit()
        flen += 1

ip = "10.0.1.{}".format(flen + 4)
mac = "{} {}\n".format(mac, ip)
with open('inv.dat', 'a') as f:
    f.write(mac)
print(ip)
