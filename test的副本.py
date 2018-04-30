#!/usr/bin/env python3
# so that script can be run from Brickman
#import numpy as np
#import pandas as pd
from Brick_control import *
from time import sleep
#from t1_q import *
#from t2_sarsa import *

#matrix = np.arange(0, 16).reshape((4, 4))
#matrix[:, :] = [[1, 0, 3, 2], [0, 1, 2, 3], [2, 3, 1, 0], [3, 2, 0, 1]]  # 0(around) 1(straight) 2(left) 3(right)
#transfer_matrix = pd.DataFrame(matrix, index=['N', 'S', 'E', 'W'], columns=['N', 'S', 'E', 'W'])
#print(transfer_matrix)

#for i in range(100):
 #   reward, done = reward_get()
#    print(reward)
#    sleep(0.2)
#a = [1, 2]
#b = [a[0] + 1, a[1] + 2]
#print(b)
'''
def observation_get():
    times, sum_l, sum_r = 0, 0, 0
    for i in range(10):
        times += 1
        sum_l += color_detect(0, 'in3')
        sum_r += color_detect(0, 'in4')
    color_sensor_l = int(sum_l / times)
    color_sensor_r = int(sum_r / times)
    return color_sensor_l, color_sensor_r

for i in range(100):
    col = observation_get()
    print(col)
    sleep(0.5)

'''
#for i in range(50):
#  a = observation_get()
#    print(a)
#turn_right()
#turn_left()
#straight_on()
#straight_on()
#turn_right()
#turn_left()
#turn_around()
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 11, 10)
y1 = np.random.normal(5, 4, 10)
y2 = x**2

plt.figure()
#plt.plot(x, y1)


#plt.figure(num=3, figsize=(8, 5),)
#plt.plot(x, y2)
# plot the second curve in this figure with certain parameters
plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--')
plt.show()
plt.save('figure.png')