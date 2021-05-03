"""
Saves the model and loads the model using pickle. Simple stuff not much explaination needed.
"""
import pickle

def saveModel(rules):
    file = open("model.pickle", "wb")
    pickle.dump(rules, file)
    file.close()

def loadModel():
    file = open("model.pickle", "rb")
    rules = pickle.load(file)
    file.close()
    return rules