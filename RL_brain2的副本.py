import numpy as np
import pandas as pd
import os

class RL:
    def __init__(self, action_space, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = action_space 
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.terminal = ' Goal '
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.rand() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))   
            action = state_action.idxmax()
        else:
            action = np.random.choice(self.actions)
        return action

    def policy_show(self):
        print('\nState' + '          Best Policy')
        for number in range(len(self.q_table.index)):
            state_action = self.q_table.iloc[number, :]
            best_action = state_action.idxmax()
            print(self.q_table.index[number] + '     ' + best_action)

    def q_learning(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != self.terminal:
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  
        else:
            q_target = r 

        error = q_target - q_predict
        self.q_table.loc[s, a] += self.lr * error  
        os.system('clear')
        print(self.q_table)
        #self.policy_show()

    def Sarsa(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != self.terminal:
            q_target = r + self.gamma * self.q_table.loc[s_, a_] 
        else:
            q_target = r  

        error = q_target - q_predict
        self.q_table.loc[s, a] += self.lr * error  
        os.system('clear')
        print(self.q_table)
        #self.policy_show()



# backward eligibility traces

class SarsaLambda:
    def __init__(self, action_space, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, trace_decay=0.2):
        self.actions = action_space  
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.terminal = ' Hell '
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

        self.lambda_ = trace_decay
        self.eligibility_trace = self.q_table.copy()

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            to_be_append = pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            self.q_table = self.q_table.append(to_be_append)

            self.eligibility_trace = self.eligibility_trace.append(to_be_append)


    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.rand() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.idxmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action


    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != ' Hell' and s_ != ' Goal ':
            q_target = r + self.gamma * self.q_table.loc[s_, a_] 
        else:
            q_target = r  # next state is terminal
        error = q_target - q_predict

        # increase trace amount for visited state-action pair
        self.eligibility_trace.loc[s, :] *= 0
        self.eligibility_trace.loc[s, a] = 1

        self.q_table += self.lr * error * self.eligibility_trace

        if s_ != 'Hell':
            self.eligibility_trace *= self.gamma*self.lambda_

        os.system('clear')
        print(self.q_table)
        print(self.eligibility_trace)

    def learn_advanced(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != ' Hell' and s_ != ' Goal ':
            q_target = r + self.gamma * self.q_table.loc[s_, a_]  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        error = q_target - q_predict

        # response the positive reward with sarsa(lambda) update
        if s_ != 'Hell':
            # increase trace amount for visited state-action pair
            self.eligibility_trace.loc[s, :] *= 0
            self.eligibility_trace.loc[s, a] = 1

            # Q update
            self.q_table += self.lr * error * self.eligibility_trace

            # decay eligibility trace after update
            self.eligibility_trace *= self.gamma*self.lambda_

        # response the negative reward with Q-learning
        else:
            self.q_table.loc[s, a] += self.lr * error 

        os.system('clear')
        print(self.q_table)
        print(self.eligibility_trace)

