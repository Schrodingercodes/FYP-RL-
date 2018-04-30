import ev3dev.ev3 as ev3
from time import sleep
from Brick_control import *
from RL_brain2 import *

MAX_EPISODES = 50
speak('Task starts')

def reward_get(state):
    times, sum_c = 0, 0
    for i in range(4):
        times += 1
        sum_c += color_detect(0, 'in3')
    color_sensor = int(sum_c / times)

    if color_sensor < 10:  # black state
        reward = -10
        done = True
        observation = ' Hell '
    elif 10 <= color_sensor < 32:  # goal state
        reward = 10
        done = True
        observation = ' Goal '
    else:
        reward = 0
        done = False
        observation = state

    return reward, done, observation

def observation_get(_state, _action):
    if _action == 'N':
        state = [_state[0] + 0, _state[1] + 1]
    elif _action == 'S':
        state = [_state[0] + 0, _state[1] - 1]
    elif _action == 'E':
        state = [_state[0] + 1, _state[1] + 0]
    elif _action == 'W':
        state = [_state[0] - 1, _state[1] + 0]

    return state

def robot_move(_action, action):
    matrix = np.arange(0, 16).reshape((4, 4))
    matrix[:, :] = [[1, 0, 3, 2], [0, 1, 2, 3], [2, 3, 1, 0], [3, 2, 0, 1]]    # 0(around) 1(straight) 2(left) 3(right)
    transfer_matrix = pd.DataFrame(matrix, index=['N', 'S', 'E', 'W'], columns=['N', 'S', 'E', 'W'])
    move = transfer_matrix.loc[_action, action]
    if move == 1:
        straight_on()
    elif move == 2:
        turn_left()
    elif move == 3:
        turn_right()
    else:
        turn_around()

def loop():
    brain = RL(['N', 'S', 'E', 'W'])
    for episode in range(MAX_EPISODES):
        print('\n Episode' + str(episode) + '\n')
        step = 0
        # initial observation
        observation = [2, 1]
        _action = 'W'

        while True:
            step += 1
            # RL choose action based on observation
            action = brain.choose_action(str(observation))
            robot_move(_action, action)

            print('\naction is ' + str(action))
            observation_ = observation_get(observation, action)

            # RL take action and get next observation and reward
            reward, done, observation_ = reward_get(observation_)

            action_ = brain.choose_action(str(observation_))
            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            brain.q_learning(str(observation), action, reward, str(observation_))

            # swap observation and action
            observation = observation_
            _action = action

            # break loop when end of this episode
            if done:
                speak('Episode Ends')
                print('\n Steps in episode:' + str(step) + '\n')
                sleep(8)
                break


if __name__ == "__main__":
    loop()