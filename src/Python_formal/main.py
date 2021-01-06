from node import *
import maze as mz
import score
import interface
import time
#import threading

import numpy as np
import pandas
import time
import sys
import os


def main():
    maze = mz.Maze("data/final_map.csv")
    interf = interface.interface()
    if (sys.argv[1] == '1'):
        sequence = [8, 24, 44, 41, 36]
    point = score.Scoreboard("data/UID.csv", "Mingto's English Corner", sys.argv[1])
    
    # TODO : Initialize necessary variables

    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting with rule 1")
        # TODO : for treasure-hunting with rule 1, which encourages you to hunt as many scores as possible
        maze.getStartPoint()
        message_L = []
        direct_L = []
        maze.deadend.remove(4)
        maze.deadend.remove(13)
        while len(maze.deadend) != 0:
            path = maze.strategy(maze.now)
            while len(path) != 0:
                direct_L.append(maze.getAction(maze.now_d, maze.now, path.pop(0)))
            
        while len(direct_L) != 0:
            message_L.append(interf.save_action(direct_L.pop(0)))
        
        message_L.pop(0)
        #send all paths    
        message = ''.join(message_L)
        interf.send_action(message)
        
        #score
        while True:
            UID = interf.get_UID()
            if UID != 0:
                point.add_UID(UID)
                now_score = point.getCurrentScore()
                print("score:", now_score)

    elif (sys.argv[1] == '1'):
        print("Mode 1: for treasure-hunting with rule 2")
        # TODO : for treasure-hunting with rule 2, which requires you to hunt as many specified treasures as possible
        maze.getStartPoint()
        message_L = []
        direct_L = []
        while len(sequence) != 0:
            path = maze.strategy_2(maze.now, sequence.pop(0))
            while len(path) != 0:
                direct_L.append(maze.getAction(maze.now_d, maze.now, path.pop(0)))
        while len(direct_L) != 0:
            message_L.append(interf.save_action(direct_L.pop(0)))
        
        message_L.pop(0)
        #send all paths
        message = ''.join(message_L)
        interf.send_action(message)   

        #score
        while True:
            UID = interf.get_UID()
            if UID != 0:
                point.add_UID(UID)
                now_score = point.getCurrentScore()
                #print("score:", now_score)

#TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    elif (sys.argv[1] == '2'):
        while True:

            print(point.getCurrentScore())                                              #
#TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       

if __name__ == '__main__':
    main()
