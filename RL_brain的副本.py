import numpy as np
import pandas as pd
import os

class RL:
    def __init__(self, action_space, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = action_space  
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.terminal = 'White_White'
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
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
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
        self.policy_show()

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
        self.policy_show()





class SarsaLambdaTable(RL):
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, trace_decay=0.9):
        super(SarsaLambdaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

       
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

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, a_]  
        else:
            q_target = r  
        error = q_target - q_predict

        self.eligibility_trace.loc[s, :] *= 0
        self.eligibility_trace.loc[s, a] = 1

        self.q_table += self.lr * error * self.eligibility_trace

        self.eligibility_trace *= self.gamma*self.lambda_
