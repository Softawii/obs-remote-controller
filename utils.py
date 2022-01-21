def equals(l1, l2):    
    result = all(map(lambda x, y: x == y, l1, l2))
    return result and len(l1) == len(l2)