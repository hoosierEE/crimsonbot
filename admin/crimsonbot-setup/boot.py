import gc
import webrepl
import network

try:
    from net_cfg import MODE, SSID, PASS
except:
    MODE = network.AP_IF
    SSID = 'crimsonbots'
    PASS = 'ise-e101'


sta = network.WLAN(network.STA_IF)
ap  = network.WLAN(network.AP_IF)

if MODE == network.STA_IF:
    ap.active(False)
    sta.active(True)
    net = None
    for t in sta.scan():
        if str(t[0], 'utf8') == SSID:
            net = t
            break
    sta.connect(str(net[0], 'utf8'), PASS)
else:
    sta.active(False)
    ap.active(True)

try:
    webrepl.start()
except OSError as exp:
    print("OSError: ", exp)

try:
    import crimsonbot as cb
    ver = cb.VERSION
    pad =  " " * (64 - len(ver))
    print("###################################################################")
    print("#  ___  ____  ____  __  __  ___  _____  _  _    ____  _____  ____ #")
    print("# / __)(  _ \(_  _)(  \/  )/ __)(  _  )( \( )  (  _ \(  _  )(_  _)#")
    print("#( (__  )   / _)(_  )    ( \__ \ )(_)(  )  (    ) _ < )(_)(   )(  #")
    print("# \___)(_)\_)(____)(_/\/\_)(___/(_____)(_)\_)  (____/(_____) (__) #")
    print("#{}v{}{}#".format(pad[int(len(pad)/2):], ver, pad[:int(len(pad)/2)]))
    print("###################################################################")
except:
    print("ImportError: Could not import crimsonbot")

gc.collect()
