class PriorityQueue:
    # Constructor
    def __init__(self, priority_function):
        self.queue = []
        self.func = priority_function
        
    # Check if PQ is empty
    def is_empty(self):
        return len(self.queue) == 0

    # Add item to PQ
    def enqueue(self, item):
        pos = 0
        found = False

        while(not found and pos < len(self.queue)):
            if(self.func(item, self.queue[pos])):
                found = True
            else:
                pos+=1
        
        self.queue.insert(pos, item)

    # Remove item from PQ
    def dequeue(self):
        return self.queue.pop(0)