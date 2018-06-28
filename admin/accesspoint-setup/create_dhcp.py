
header = '''
subnet 10.0.1.0 netmask 255.255.255.0 {
  option subnet-mask 255.255.255.0;
  option domain-name-servers 10.0.1.2;
  option routers 10.0.1.2;
  range 10.0.1.100 10.0.1.254;
'''

inv = {}
with open('inv.dat') as f:
    for l in f:
        esp = l.split()
        inv[esp[0]] = esp[1]

with open('dhcpd.conf', 'w') as f:
    f.write(header)
    
    for i, (k, v) in enumerate(inv.items()):
        f.write('  host r{} {{\n'.format(i))
        f.write('      hardware ethernet {};\n'.format(k))
        f.write('      fixed-address {};\n'.format(v))
        f.write('  }\n')
    f.write('}\n')
