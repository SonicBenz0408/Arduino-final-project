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


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
        self.raw_data = pandas.read_csv(filepath).values
        self.nd_dict = dict()  # key: index, value: the correspond node
        self.deadend = []
        print(self.raw_data)
        for i in range(np.shape(self.raw_data)[0]):
            self.nd_dict[i+1] = Node(i+1)
            for element in self.raw_data[i][1:5]:
                if not np.isnan(element):
                    #adjacency list
                    for index in np.where(self.raw_data[i][1:5] == element):
                        self.nd_dict[i+1].setSuccessor(int(element), index+1, self.raw_data[i][5:][index])
            #deadend list            
            if len(self.nd_dict[i+1].Successors) == 1:
                self.deadend.append(i+1)
        #except 1
        try:
            self.deadend.remove(1)
        except:
            pass        

        
        """
        self.nd_array = np.array([Node(i+1) for i in range(np.shape(self.raw_data)[0])])
        for i in range(np.shape(self.raw_data)[0]):
            for element in self.raw_data[i][1:5]:
                if not np.isnan(element):
                    for index in np.where(self.raw_data[i][1:5] == element):
                        self.nd_array[i].setSuccessor(int(element), index+1, 2)
        """

    def getStartPoint(self):
        #initialization
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        self.now = 1
        self.now_d = self.nd_dict[1].Successors[0][1].value
        return self.nd_dict[1]

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        """        
        nearest = self.deadend[0]
        min_d = abs(nearest- nd)
        
        for index in self.deadend:
            diff = abs(index - nd)
            if diff < min_d:
                min_d = diff
                nearest = index
        self.deadend.remove(nearest)
        """
        nearest = self.deadend[0]
        min_p = self.BFS_2(nd, nearest)[-1]
        for candidate in self.deadend[1:]:
            distance = self.BFS_2(nd, candidate)[-1]
            if distance < min_p:
                min_p = distance
                nearest = candidate

        self.deadend.remove(nearest)

        return self.BFS_2(nd, nearest)


    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        queue = [nd_from]
        #0:white(isn't searched) 1:gray(searched and in queue) 2:black | 666:searched but not all
        color_dict = dict()
        d_dict = dict()
        pre_dict = dict()
        num_connect_dict = dict()

        #initialization : set all nd is white , distance is infinite, and predecessor is -1 
        for key in self.nd_dict:
            color_dict[key] = 0
            d_dict[key] = 10000000
            pre_dict[key] = -1
            num_connect_dict[key] = len(self.nd_dict[key].Successors)

        d_dict[nd_from] = 0
        color_dict[nd_from] = 1

        while queue != []:
            for succ in self.nd_dict[queue[0]].Successors:
                if color_dict[succ[0]] == 0:
                    if num_connect_dict[succ[0]] == 1:
                        color_dict[succ[0]] = 1
                    else:
                        color_dict[succ[0]] = 666
                        num_connect_dict[succ[0]] -= 1
                    d_dict[succ[0]] = d_dict[queue[0]] + succ[2]
                    pre_dict[succ[0]] = queue[0]
                    queue.append(succ[0])
                elif color_dict[succ[0]] == 666:
                    if num_connect_dict[succ[0]] == 1:
                        color_dict[succ[0]] = 1
                    else:
                        num_connect_dict[succ[0]] -= 1
                    if d_dict[succ[0]] > d_dict[queue[0]] + succ[2]:
                        d_dict[succ[0]] = d_dict[queue[0]] + succ[2]
                        pre_dict[succ[0]] = queue[0]


            color_dict[queue[0]] = 2
            queue.pop(0)

        
        result = [nd_to]
        temp = nd_to
        total_dis = 0

        while result[-1] != nd_from:
            result.append(pre_dict[temp])
            for succ in self.nd_dict[result[-1]].Successors:
                if succ[0] == temp:
                    total_dis += succ[2]
            temp = pre_dict[temp]

        result.pop()
        result.reverse()
        result.append(total_dis)
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
    def strategy(self, nd):
        return self.BFS(nd)[:-1]

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)[:-1]

if __name__ == '__main__':
    start = time.time()
    maze = Maze("data/final_map.csv")
    maze.getStartPoint()
    message_L = []
    direct = []
    sequence = [8, 24, 44, 41, 36]
    while len(sequence) != 0:
        path = maze.strategy_2(maze.now, sequence.pop(0))
        while len(path) != 0:
            direct.append(maze.getAction(maze.now_d, maze.now, path.pop(0)))
            #direct.append(path.pop(0))
    print(direct)
    end = time.time()
    print(end-start)