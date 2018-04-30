#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
from Brick_control import *
from RL_brain import *
import matplotlib  

matplotlib.use('Agg')  

import matplotlib.pyplot as plt 

MAX_EPISODES = 20
speak('Task starts')

def reward_get(s):
    if s == 'White_White':
        reward = -10
        done = True
    else:
        reward = 0
        done = False

    return reward, done

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
    brain = RL(['Straight', 'Right', 'Left'])
    info_store = []
    for episode in range(MAX_EPISODES):
        print('\nEpisode' + str(episode)+' starts\n')
        step = 0
        # initial observation
        observation = observation_get()
        action = brain.choose_action(str(observation))

        while True:
            step += 1
            # RL choose action based on observation
            robot_move(action)
            observation_ = observation_get()

            # RL take action and get next observation and reward
            reward, done = reward_get(observation_)

            action_ = brain.choose_action(str(observation_))
            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            brain.Sarsa(str(observation), action, reward, str(observation_), action_)

            # swap observation and action
            observation = observation_
            action = action_
            print(step)

            # break while loop when end of this episode
            if done:
                speak('Episode Ends')
                print('\nSteps in episode:' + str(step) + '\n')
                info_store.append(step)
                sleep(4)
                break
            
        if step > 120:
            x = np.arange(episode + 1)
            y = info_store
            print(x)
            print('Episode-steps info: ' + str(y))
            plt.figure()
            plt.xlabel('episode number')  
            plt.ylabel('step(s)') 
            plt.plot(x, y, color='b', linewidth=1.5)
            plt.plot(x, y, 'ro')
            plt.grid()
            plt.savefig('figure_T1_s.png')
            break


if __name__ == "__main__":
    loop()


