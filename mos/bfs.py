from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math
import time

class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Map:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
        self.raw_data = pandas.read_csv(filepath).values
        self.nd_dict = dict()  # key: index, value: the correspond node
        self.deadend = []
        for i in range(np.shape(self.raw_data)[0]):
            self.nd_dict[i+1] = Node(i+1)
            for element in self.raw_data[i][1:5]:
                if not np.isnan(element):
                    #adjacency list
                    for index in np.where(self.raw_data[i][1:5] == element):
                        self.nd_dict[i+1].setSuccessor(int(element), index+1)

        self.now = 6
        self.now_d = self.nd_dict[6].Successors[0][1].value

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd_from, nd_to):
        # TODO : similar to BFS but fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        
        queue = [nd_from]
        #0:white(isn't searched) 1:gray(searched and in queue) 2:black
        color_dict = dict()
        d_dict = dict()
        pre_dict = dict()

        #initialization : set all nd is white , distance is infinite, and predecessor is -1 
        for key in self.nd_dict:
            color_dict[key] = 0
            d_dict[key] = 10000000
            pre_dict[key] = -1

        d_dict[nd_from] = 0
        color_dict[nd_from] = 1

        while queue != []:
            for succ in self.nd_dict[queue[0]].Successors:
                if color_dict[succ[0]] == 0:
                    d_dict[succ[0]] = d_dict[queue[0]] + 1
                    pre_dict[succ[0]] = queue[0]
                    queue.append(succ[0])
                    color_dict[succ[0]] += 1


            color_dict[queue[0]] += 1
            queue.pop(0)

        
        result = [nd_to]
        temp = nd_to
        total_dis = 0

        while result[-1] != nd_from:
            result.append(pre_dict[temp])
            temp = pre_dict[temp]

        result.pop()
        result.reverse()
        return result

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car
        destination_dir = ''
        for succ in self.nd_dict[nd_from].Successors:
            if succ[0] == nd_to:
                destination_dir = self.nd_dict[nd_from].getDirection(nd_to)
                break
        self.now_d = destination_dir
        self.now = nd_to
        if car_dir == 1:
            if destination_dir == 1:
                return Action.ADVANCE.value
            elif destination_dir == 2:
                return Action.U_TURN.value
            elif destination_dir == 3:
                return Action.TURN_LEFT.value
            elif destination_dir == 4:
                return Action.TURN_RIGHT.value
#            else:
#                return Action.HALT.value
        
        elif car_dir == 2:
            if destination_dir == 2:
                return Action.ADVANCE.value
            elif destination_dir == 1:
                return Action.U_TURN.value
            elif destination_dir == 4:
                return Action.TURN_LEFT.value
            elif destination_dir == 3:
                return Action.TURN_RIGHT.value
#            else:
#                return Action.HALT.value

        elif car_dir == 3:
            if destination_dir == 3:
                return Action.ADVANCE.value
            elif destination_dir == 4:
                return Action.U_TURN.value
            elif destination_dir == 2:
                return Action.TURN_LEFT.value
            elif destination_dir == 1:
                return Action.TURN_RIGHT.value
#            else: 
#               return Action.HALT.value
        
        elif car_dir == 4:
            if destination_dir == 4:
                return Action.ADVANCE.value
            elif destination_dir == 3:
                return Action.U_TURN.value
            elif destination_dir == 1:
                return Action.TURN_LEFT.value
            elif destination_dir == 2:
                return Action.TURN_RIGHT.value
#            else: 
#                return Action.HALT.value
        else:
            return Action.HALT.value

    def save_action(self,dirc):
        # TODO : save the action to car
        if dirc == 1:
            message = 'a' #advance
        elif dirc == 2:
            message = 'u' #U turn
        elif dirc == 3:
            message = 'r' #turn right
        elif dirc == 4:
            message = 'l' #turn left
        elif dirc == 5:
            message = 'h' #halt
            
        return message

    def strategy(self, nd_from, nd_to):
        direct_L = []
        message_L = []
        path = self.BFS(nd_from, nd_to)
        while len(path) != 0:
            direct_L.append(self.getAction(self.now_d, self.now, path.pop(0)))
        while len(direct_L) != 0:
            message_L.append(self.save_action(direct_L.pop(0)))

        message = ''.join(message_L)
        return message

if __name__ == '__main__':
    start = time.time()
    test = Map("map/map.csv")
    test.getStartPoint()
    message_L = []
    path_L = []
    direct = []
    sequence = [5, 2, 3, 4]

    while len(sequence) != 0:
        path = test.strategy(test.now, sequence.pop(0))
        path_L = path_L + path
        while len(path) != 0:
             direct.append(test.getAction(test.now_d, test.now, path.pop(0)))

    print(path_L)
    end = time.time()
    print(end-start)