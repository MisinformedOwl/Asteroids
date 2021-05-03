"""
This is where the fuzzy system is crated.
It creates the memberhsip classes of both distance aswell as the meteor count.
then using both variables comes to a decision and returns a % in danger.
This % is then turned into 1 of 3 variables. low, med and hgih danger
"""
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

def fuzzSetup():
    closeness = ctrl.Antecedent((np.arange(0, 1001, 1)), "Closeness")
    meteorCount = ctrl.Antecedent(np.arange(0,200,1), "Meteors")
    
    danger = ctrl.Consequent(np.arange(0,100,1), "Danger")
    
    meteorCount['lots'] = fuzz.trapmf(meteorCount.universe, [10,20,200, 200])
    meteorCount['many'] = fuzz.trimf(meteorCount.universe, [4,8,14])
    meteorCount['few'] = fuzz.trimf(meteorCount.universe, [0,4,6])
    
    closeness['close'] = fuzz.trimf(closeness.universe, [0,100,200])
    closeness['distant'] = fuzz.trimf(closeness.universe, [100,250,400])
    closeness['far'] = fuzz.trapmf(closeness.universe, [350,500,1001, 1001])
    
    danger['low'] = fuzz.trimf(danger.universe, [0,0,30])
    danger['med'] = fuzz.trimf(danger.universe, [20,50,80])
    danger['high'] = fuzz.trimf(danger.universe, [75,100,100])
    
    rule1 = ctrl.Rule(closeness['close'] & meteorCount['few'], danger['med'])
    rule2 = ctrl.Rule(closeness['close'] & meteorCount['many'], danger['high'])
    rule3 = ctrl.Rule(closeness['close'] & meteorCount['lots'], danger['high'])
    
    rule4 = ctrl.Rule(closeness['distant'] & meteorCount['few'], danger['low'])
    rule5 = ctrl.Rule(closeness['distant'] & meteorCount['many'], danger['med'])
    rule6 = ctrl.Rule(closeness['distant'] & meteorCount['lots'], danger['high'])
    
    rule7 = ctrl.Rule(closeness['far'] & meteorCount['few'], danger['low'])
    rule8 = ctrl.Rule(closeness['far'] & meteorCount['many'], danger['low'])
    rule9 = ctrl.Rule(closeness['far'] & meteorCount['lots'], danger['med'])
    
    dangerControl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9])
    dangerLevel = ctrl.ControlSystemSimulation(dangerControl)
    
    return dangerLevel