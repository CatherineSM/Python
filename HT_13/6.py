class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
        
obj_a = Counter()
obj_b = Counter()
obj_c = Counter()

print(obj_a.count)
