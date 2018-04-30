#!/usr/bin/env python3
#import necessary package
import numpy as np
import pandas as pd
import socket
import time
import os
import pickle

def con_connect():
    #define host ip: Rpi's IP
    HOST_IP = "192.168.2.3"
    HOST_PORT = 12345
    print("Starting socket: TCP...")
    #create socket object:socket=socket.socket(family,type)
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
    host_addr = (HOST_IP, HOST_PORT)
    #bind socket to addr:socket.bind(address)
    socket_tcp.bind(host_addr)
    #listen connection request:socket.listen(backlog)
    socket_tcp.listen(1)
    #waite for client:connection,address=socket.accept()
    socket_con, (client_ip, client_port) = socket_tcp.accept()
    print("Connection accepted from %s." %client_ip)
    #handle
    print("Receiving package...")
    while True:
        start = socket_con.recv(1024).decode()
        if start == 'Ready':
            print('PC is ready')
            break
    return socket_con

def data_send(socket_con, data):
    bytes_out = pickle.dumps(data)
    socket_con.sendall(bytes_out)
    time.sleep(2)

def data_recv(socket_con):
    bytes_in = b''
    bytes_in = socket_con.recv(1024)
    time.sleep(1)
    if len(bytes_in) > 0:
        data = pickle.loads(bytes_in)
        print(data)
        return data
    else:
        print('No data obtained')
        return False
'''    
while True:
    a = np.ones((3, 4))
    a_pickled = pickle.dumps(a)
    socket_con.sendall(a_pickled)
    print('here0')
    bytes_pc = b''
    bytes_pc = socket_con.recv(1024)
    if len(bytes_pc) > 0:
        data_ev3 = pickle.loads(bytes_pc)
        print(data_ev3)
        print('here1')
        time.sleep(2)
    else:
        print('No data obtained')
'''
def loop():
    socket_con = con_connect()
    while True:
        a = np.ones((3, 4))
        data_send(socket_con, a)
        data = data_recv(socket_con)


if __name__ == "__main__":
    loop()

        
 

