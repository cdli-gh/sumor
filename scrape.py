def splitS(list):
    return list.split('-')

def splitX(list):
    return list.split('.')

def delA(y):
    r = []
    for a in y:
        r.append(delB(delB(a)))
    return r

def delB(x):
    r = x
    if x[-1] == '[' and x[-2] == ']' or x.count(']') + x.count('[') == 1:
        r = r[:-1]
    return r

with open("P100065.conll") as file:
    for index, line in enumerate(file):
        l = line.split('\t')
        if index > 1: 
            print("\n", index-1)
            print(delA(splitS(l[2])))
            print(delA(splitX(l[3])))
