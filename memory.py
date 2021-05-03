"""
This section is important for memory. aswell as signing upall of the rules.
"""
import TRule

class workingMemory:
    line1 = 0
    line2 = 0
    line3 = 0
    line4 = 0
    line5 = 0
    line6 = 0
    line7 = 0
    line8 = 0

def Initialize():
    rules = [] # 8³ * 9 = 4608 rules
    
    dangers = ["low", "med", "high"]
    moves = [(1,0,0,0), (0,1,0,0), (0,0,1,0),(0,0,0,1), (0,0,0,0), (1,1,0,0), (1,0,1,0), (0,0,1,1), (0,1,0,1)] # (up, left, right, down)
    
    for first in dangers:
        for second in dangers:
            for third in dangers:
                for fourth in dangers:
                    for fifth in dangers:
                        for sixth in dangers:
                            for seventh in dangers:
                                for eighth in dangers:
                                    for move in moves:
                                        rules.append(TRule.TRule(first,second,third,fourth,fifth,sixth,seventh,eighth,move))
    return rules