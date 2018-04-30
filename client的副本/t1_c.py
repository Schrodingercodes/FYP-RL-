#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from Brick_control import *
import socket
from time import sleep
import os
import pickle

MAX_EPISODES = 20

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
    sleep(0.5)

def data_recv(socket_con):
    bytes_in = b''
    bytes_in = socket_con.recv(1024)
    sleep(0.5)
    if len(bytes_in) > 0:
        data = pickle.loads(bytes_in)
        #print(data)
        return data
    else:
        print('No data obtained')
        return False


def observation_get():
    times, sum_l, sum_r = 0, 0, 0
    for i in range(10):
        times += 1
        sum_l += color_detect(0, 'in3')
        sum_r += color_detect(0, 'in4')
    color_sensor_l = int(sum_l / times)
    color_sensor_r = int(sum_r / times)

    if color_sensor_l < 18 and color_sensor_r < 18:
        state = 'Black_Black'
    elif color_sensor_l < 18 and color_sensor_r > 17:
        state = 'Black_White'
    elif color_sensor_l > 17 and color_sensor_r < 18:
        state = 'White_Black'
    else:
        state = 'White_White'
    return state


def robot_move(action):
    if action == 'Straight':
        go_straight(450, 150)
    elif action == 'Right':
        go_right(400, 150)
    else:
        go_left(400, 150)


def loop():
    speak('Task starts')
    socket_con = con_connect()
    for episode in range(MAX_EPISODES):
        observation = observation_get()
        data_send(socket_con, observation)
        while True:
            action = data_recv(socket_con)
            robot_move(action)
            observation_ = observation_get()
            data_send(socket_con, observation_)

            done = data_recv(socket_con)
            if done:
                speak('Episode Ends')
                sleep(4)
                break


if __name__ == "__main__":
    loop()

        
 

