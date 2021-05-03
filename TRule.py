"""
Thsi creates the basic structure of the rules.
"""

class TRule:
    weight = 0
    
    antecedentA = "none"
    antecedentB = "none"
    antecedentC = "none"
    antecedentD = "none"
    antecedentE = "none"
    antecedentF = "none"
    antecedentG = "none"
    antecedentH = "none"
    move = (0,0,0,0)

    def __init__(self,a,b,c,d,e,f,g,h, move):
        self.antecedentA = a
        self.antecedentB = b
        self.antecedentC = c
        self.antecedentD = d
        self.antecedentE = e
        self.antecedentF = f
        self.antecedentG = g
        self.antecedentH = h
        self.move = move