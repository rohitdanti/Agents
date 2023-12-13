#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Licensing Information:  
# Please DO NOT DISTRIBUTE OR PUBLISH this project or the solutions for this project.
# We reserve the right to publish and provide access to this code.
# This project is built for the use of CSE 471 Introduction to AI class 
# instructed by Yu Zhang (yzhan442@asu.edu).
# 
# Attribution Information: The Autonomous Driving AI project was developed at Arizona State University Fall 2023
# The core project and autograder was primarily created by Akku Hanni
# (ahanni@asu.edu) and contributed by Kevin Vora (kvora1@asu.edu)

"""

import random
import numpy as np

class Agent:
    """
    An agent must define a get_action method, but may also define
    other methods which will be called if they exist. 
    This is a super class for any agent type.
        
    """

    def __init__(self):
        """
        Description
        -----------
        The list of available actions for all cars are:
        Forward - 'F'
        Left - 'L'
        Right - 'R'
        Wait - 'W'

        """
        self.available_actions = ['F', 'L', 'R', 'W']
    
    def get_action(self, state):
        """
        The Agent will receive a State of the environment (based on the agent type) and
        must return an action from the available actions {Forward - 'F', Left - 'L', Right - 'R' and Wait - 'W'}.
        """
        pass
    
    
class ManualAgent(Agent):
    """
    A manual agent is used to control the Autonomous Agent ('A') manually by the user.

    """
    
    def get_action(self, percept):
        "*** YOUR CODE HERE ***"
        print("Enter Action (Forward - 'F', Left - 'L', Right - 'R', Wait - 'W', Stop - 'S'):\n")
        action = input()
        return action


class RandomAgent(Agent):
    """
    A random agent chooses an action randomly at each choice point from the list of available actions.

    """
    
    def get_action(self, percept):
        "*** YOUR CODE HERE ***"
        action = random.choice(self.available_actions) #should choose an action among the legal actions available
        print(f"Random action chosen: {action}")
        input("Press enter to step through.")
        return action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by following simple rules

    """
    
    def get_action(self, percept):
        """
        Description
        ----------
        This function returns the reflex action given the current percept. 
        The percept is essentially a (3 x 3) grid sized partial view of the road environment, with 'A' at the center i.e. at index (1, 1).
        
        """
        "*** YOUR CODE HERE ***"    
        bottom_left = percept[2][0]
        bottom = percept[2][1]
        bottom_right = percept[2][2]
        left = percept[1][0]
        right = percept[1][2]
        top_left = percept[0][0]
        top = percept[0][1]
        top_right = percept[0][2]
        
        for rows in percept:
            print(rows)
        print('************')
        print()
        
        
        # if(top_left!=-1 or top_right!=-1 or left !=-1 or right!=-1 or bottom_left!=-1 or bottom_right!=-1 or bottom!=-1  ):
        if((top_left ==0 and top == 0 and top_right==0 ) or
        (top_left ==10 and top == 10 and top_right == 10 ) or 
        (top_left ==-1 and top == 0 and top_right== 0  ) or 
        (top_left ==0 and top == 0 and top_right== -1 ) or 
        (top_left ==-1 and top == 0 and top_right== -1 )):
            print('CLEAR F')
            return 'F'
        elif(bottom==0):
            if((left==0) and (right == 0)):
                print('simple wait')
                return 'W'
            elif(left==1 and right==0 and bottom_right!=1):
                print('riksy right--> R')
                return 'R'
            elif(left==0 and right==1 and bottom_left!=1):
                print('risky left--> L')
                return 'L'  
            else:
                print('simple wait')
                # if((left==1 or left==-1 ) and (right==1 or right ==-1)):
                #     if(top==0):
                #         print('risky forward')
                #         return 'F'
                #     else:
                #         return 'W' 
                return 'W'          
        # else:      
        elif((right==0 and bottom_right !=1) or (right==0 and bottom ==1)): #Move Right
            print('taking chance--> Rightttt')
            # if(bottom_right==1):
            #     return 'W'
            return 'R'
        elif((left==0 and bottom_left !=1) or (left==0 and bottom ==1)): #Move Right
            print('Left')
            # if(bottom_left==1):
            #     return 'W'
            return 'L'
        # elif(bottom!=1 and top!=1 and left!=1 and right!= 1 and bottom_left==1 and bottom_right ==1 and top_left ==1 and top_right==1 ):
        #     print('Waiting')
        #     return 'W' 
        # elif(top==0):
        #     print('only F')
        #     return 'F'
        print('default wait')
        return 'W'
        
        
              
class ExpectimaxAgent(Agent):
    """
    An expectimax agent chooses an action at each choice point based on the expectimax algorithm.
    The choice is dependent on the self.evaluationFunction.
    
    All other cars should be modeled as choosing uniformly at random from their legal actions.

    """
    def __init__(self, depth=3):
        self.index = 0 # 'A' is always agent index 0
        self.depth = int(depth)
        super().__init__()
   
    def evaluation_function(self, road_state):
        """
        Description
        ----------
        This function returns a score (float) given a state of the road.
        """
    #     aa_loc = road_state.get_car_position(0)
    #     print('aa_LOC - ',aa_loc)
    #     # Proximity to other vehicles
    #     distances = [manhattan_distance(aa_loc, road_state.get_car_position(i)) for i in range(1, road_state.get_num_cars())]
    #     average_distance = sum(distances) / len(distances) if distances else 0
    #     proximity_score = 1 / (1 + average_distance)

    #     # Goal distance
    #     goal_distance = road_state.get_min_distance_to_goal(aa_loc)
    #     goal_distance_score =  1 / (1 + goal_distance)

    #     # Crashes
    #     crash = 0
    #     if road_state.is_crash():
    #         crash = 0
    #     else:
    #         crash = 1
    #     crash_score = crash
    
        num_cars = road_state.get_num_cars()
        score = 0
        goalDistance = 0
        
        for index in range(num_cars):
            if road_state.is_car_on_road(index):
                agent_Position = road_state.get_car_position(index)
                distance_to_goal = road_state.get_min_distance_to_goal(agent_Position)
                goalDistance = distance_to_goal + goalDistance
        
        if road_state.is_crash():
            score = score - 10000
        elif road_state.is_done():
            score  = score + 10000 

        score = score - goalDistance

        for index in range(num_cars):
            if road_state.is_car_on_road(index):
                agent_position = road_state.get_car_position(index)
                if agent_position == (0, 0):
                    score = score - 5000
                else:
                    score = score + distance_to_goal * 10 
                    
        return score
    
    def get_action(self, road_state):
        """
        Description
        ----------
        This function returns the expectimax action using self.depth and self.evaluationFunction.
        All other cars should be modeled as choosing uniformly at random from their
        legal moves.

        """
        "*** YOUR CODE HERE ***"  
        def expectimax_search(state, depth, agent_index):
            
            # Base case: If depth is 0 or the game is done or there's a crash, return the evaluation of the state.
            if state.is_crash() or depth == 0 or state.is_done():
                return self.evaluation_function(state)

            # Get legal actions for the current agent.
            legal_actions = state.get_legal_actions(agent_index)

            if agent_index != 0: 
                average = 0.0
                num_actions = len(legal_actions) or 1  
                for action in legal_actions:
                    state_successor = state.generate_successor(agent_index, action)
                    value = expectimax_search(state_successor, depth - 1, (agent_index + 1) % state.get_num_cars())
                    average += value / num_actions
                return average
            else:
                max_value = float('-inf')
                # For each legal action, calculate the value and update max_value.
                for action in legal_actions:
                    state_successor = state.generate_successor(agent_index, action)
                    value = expectimax_search(state_successor, depth - 1, 1)
                    max_value = max(max_value, value)
                return max_value
            

        legal_actions = road_state.get_legal_actions(0)
        best_action = None
        new_Max = float('-inf')

        for action in legal_actions:
            successor = road_state.generate_successor(0, action)
            value = expectimax_search(successor, self.depth, 1)
            if value > new_Max:
                new_Max = value
                best_action = action

        return best_action


        
class LearningAgent(Agent):
    """
    A learning agent chooses an action at each choice point based on the Q values approximated.
    In this project your learning agent is essentiually an ApproximateQLearningAgent
    
    """
    
    def __init__(self, num_features=4, custom_weights=False, weights=None, alpha=0.1, gamma=0.99):
        self.alpha = alpha
        self.gamma = gamma
        self.num_features = num_features
        self.decay_rate = 0.99
        self.epsilon = 1
        self.features = None
        if custom_weights:
            self.weights = weights
        else:
            self.weights = np.random.rand(num_features)
            
        super().__init__()
        
    def get_weights(self):
        # print(len(self.weights))
        return self.weights        
            
    def get_features(self, state, action):
        """
        Description
        ----------
        This function returns a vector of features for the given state action pair
        
        Compute: f_1(s, a), f_2(s, a), ... , f_n(s, a)

        """
        "*** YOUR CODE HERE ***"  
        features = []
        for fi in range(self.num_features):
                        
            if fi == 0:
                car_locations = state.get_car_locations()
                if car_locations:
                    closest_distance = 9999
                    for key in car_locations:
                        if key != 0 and car_locations[key]:
                            distance = manhattan_distance(car_locations[key], car_locations[0])
                            if distance < closest_distance:
                                closest_distance = distance
                    features.append(normalize(closest_distance, 1, state.get_height()-1))
            elif fi == 1:
                if not state.is_terminal():
                    next_state, reward, result = state.step(action)
                    # print(next_state.is_terminal(), reward)
                    features.append(1 if next_state.is_terminal() and reward == -100 else 0)
                else:
                    features.append(0)
            elif fi == 2:
                if state.is_terminal() == True:
                    features.append(0)
                else:
                    car_locations = state.get_car_locations()
                    if not car_locations:
                        features.append(0)
                    else:
                        x, y = car_locations[0]
                        features.append(normalize(state.get_height() - x, 0, state.get_height()))
            elif fi ==3:
                #     # next_state, reward, result = state.step(action)
                if state.is_terminal():
                    features.append(0)
                else:
                    car_locations = state.get_car_locations()
                    x, y = car_locations[0]
                    num_cars = 0
                    for car_key in car_locations.keys():
                        if car_key != 0 and car_locations[car_key]:
                            x1,y1 = car_locations[car_key]
                            if manhattan_distance((x,y), (x1,y1)) <= 2:
                                num_cars = num_cars + 1
                    features.append(normalize(num_cars, 0, 12))
        return features

        
    def get_Q_value(self, state, action):
        """
        Description
        ----------
        This function returns the Q value; Q(state,action) = w . featureVector
        where . is the dotProduct operator
        
        Compute: Q(s, a) = w_1 * f_1(s, a) + w_2 * f_2(s, a) + ... + w_n * f_n(s, a)
        
        """
        "*** YOUR CODE HERE ***"
        weights = self.weights
        features = self.get_features(state, action)
        
        Q = sum([weights[i] * features[i] for i in range(len(features))])
        return Q

    def compute_max_Q_value(self, state):
        """
        Description
        ----------
        This function returns the max over all Q(state, action) 
        for all legal/available actions for the given state
        Note that if there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        
        Compute: max_a' Q(s', a')
        
        """
        "*** YOUR CODE HERE ***"
        if state.is_terminal():
            return 0.0
        else:
            all_legal_actions = ['F', 'L', 'R', 'W']
            qvals = []
            for action in all_legal_actions:
                qvals.append(self.get_Q_value(state, action))
            max_qval = max(qvals)
            return max_qval        
    
    def update(self, state, action, next_state, reward):
        """
        Description
        ----------
        This function updates the weights based on the given transition
        
        """
        "*** YOUR CODE HERE ***"
        features = self.get_features(state, action)
        current_Q = self.get_Q_value(state, action)
        new_Q = (1 - self.alpha) * current_Q + self.alpha * (reward + self.gamma * self.compute_max_Q_value(next_state))
        # print(len(self.weights))
        for i in range(len(self.weights)):
            # print((1-self.weights[i]), self.gamma*(new_Q - current_Q)*(1-self.weights[i]))
            self.weights[i] += (1-self.gamma)*(new_Q - current_Q)*features[i]
        # raise Exception("Function not defined")
        self.epsilon = self.epsilon * 0.995

    def get_action(self, state):
        """
        Description
        ----------
        This function returns the best action based on the self.weights it has learned.

        """
        max_qvalue = float('-inf')
        best_action = None
        for action in self.available_actions:
            qvalue = self.get_Q_value(state, action)
            if qvalue > max_qvalue:
                max_qvalue = qvalue  
                best_action = action
        return best_action

    def train(self, state):
        """
        Description
        ----------
        This function learns the weights for your approximate Q learning agent 
        by training for a single episode given the initialization of the road.
        
        """
        
        cum_reward = 0
        done=False
        # self.initialise_features(state)
        # print(state.is_terminal(), state.get_car_locations(), state.get_road_data())
        # exit(0)
        while not (done):            
            # Choose an action epsilon greedily 
            if np.random.rand() < self.epsilon:
                action = np.random.choice(self.available_actions)
            else:
                action = self.get_action(state)
            
            # Take the action and observe the next state and reward
            next_state, reward, done = state.step(action) 
            # if done and reward > 0:
                # print("episode", reward, done)
            # Update weights by approximating Q value
            self.update(state, action, next_state, reward)

            # Move to the next state
            state = next_state
            cum_reward += reward
            
        return cum_reward
    
def normalize(value, min_value, max_value):
    """
    Description
    ----------
    Normalizes a given value between 0-1
    
    """
    return (value - min_value) / (max_value - min_value)

def manhattan_distance(loc1, loc2):
    """
    Description
    ----------
    Returns the Manhattan distance between points loc1 and loc2
    
    """
    return abs( loc1[0] - loc2[0] ) + abs( loc1[1] - loc2[1] )