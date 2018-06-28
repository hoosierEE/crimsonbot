import network

print("Configuring network settings...")

MODE = None
while MODE != "Y" and MODE != "n":
    MODE = input("Use a STATION endpoint? [Y/n]: ")

if MODE == "Y":
    SSID = input("input an SSID to connect to: ")
    p1 = input(" Set the WPA password: ")
    PASS = p1
    MODE = "network.STA_IF"
else:
    MODE = "network.AP_IF"
    SSID = ""
    PASS = ""
    
f = open('net_cfg.py', 'w')
f.write("import network\n")
f.write("MODE = {}\n".format(MODE))
f.write("SSID = '{}'\n".format(SSID))
f.write("PASS = '{}'\n".format(PASS))
f.close()
