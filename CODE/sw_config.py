#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import pickle
import time
host_list = ['128.194.6.178', '128.194.6.141', '128.194.6.170']
Switch1 = 0xb273c1911047
Switch2 = 0x9a5c5639b84a
Switch3 = 0xe6324fba604f
Switch4 = 0xf2e51686d74c
Switch5 = 0x02bb72767e4b

s = socket.socket()         # Create a socket object
time.sleep(1)
host = host_list[2] # Get local machine name
port = 13999                # Reserve a port for your service.
dpid = Switch1
s.connect((host, port))
s.send(pickle.dumps(dpid))
print s.recv(1024)
s.close                     # Close the socket when done

s = socket.socket()         # Create a socket object
time.sleep(1)
host = host_list[1] # Get local machine name
port = 13999                # Reserve a port for your service.
dpid = Switch1
s.connect((host, port))
s.send(pickle.dumps(dpid))
print s.recv(1024)
s.close                     # Close the socket when done

s = socket.socket()         # Create a socket object
time.sleep(1)
host = host_list[0] # Get local machine name
port = 13999                # Reserve a port for your service.
dpid = Switch1
s.connect((host, port))
s.send(pickle.dumps(dpid))
print s.recv(1024)
s.close                     # Close the socket when done

