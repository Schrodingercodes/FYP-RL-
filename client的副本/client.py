#!/usr/bin/env python3
import socket
import time
import sys
import numpy as np
import pandas as pd
import pickle

#EV3's IP
SERVER_IP = "192.168.2.3"
SERVER_PORT = 12345

print("Starting socket: TCP...")
server_addr = (SERVER_IP, SERVER_PORT)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
        socket_tcp.connect(server_addr)
        break
    except Exception:
        print("Can't connect to server,try it later!")
        time.sleep(1)
        continue
while True:
    try:

        a = np.ones((3, 4))
        command = pd.DataFrame(a, index=['1', '2', '3'], columns=['A', 'B', 'C', 'D'])
 #       a = 100
        c_pickled = pickle.dumps(command)
#        print(c_pickled)
        print(pickle.loads(c_pickled))
        print('0')
        socket_tcp.sendall(c_pickled)
        print('1')
        time.sleep(2)
        print('2')
#        data = socket_tcp.recv(1024)
#        if len(data)>0:
#            print("Received: %s" % data)
#            time.sleep(1)
#            continue
#        command = input('Please input >')
#        if not command:
#            break
#        c_pickled = command.to_json()
#        a = 100 
#        c_pickled = json.dumps(dic)
    except Exception:
        socket_tcp.close()
        socket_tcp=None
        sys.exit(1)
