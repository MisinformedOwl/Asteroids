"""
Create a global queue to store lines variables.
"""
class queue:
    
    def __init__(self):
        self.items = []
    
    def add(self, item):
        self.items.insert(0,item)
    
    def nextItem(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)