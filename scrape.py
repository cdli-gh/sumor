'''
Uncomment the comments to see the background work happening and
some of the alerts such as of unknown tags for words which will most
probably be for the nouns.
'''



import re

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

noun = []; verb = []; end = []
nmean = []; vmean = []
ntag = []
nun = ['N', 'NU', 'PN', 'HN', 'MP', 'MN', 'CNJ', 'RN']

def insertWord(l, w):
    div = re.compile(r'[A-Za-z0-9\(*\w\)]+?(?=\[|\])')
    a = div.findall(l)
    ## Ignoring cases when the length of segmented SEGM and XPOSTAG are different
    if nun.count(w) > 0 and \
        not (noun.count(a[0]) > 0 and nmean.count(a[1]) > 0):

        noun.append(a[0])
        nmean.append(a[1])
        ntag.append(w)
    elif w == 'V' and\
        not (verb.count(a[0]) > 0 and vmean.count(a[1]) > 0):

        verb.append(a[0])
        vmean.append(a[1])
    '''
    else:
        print('Unfounded word annotation: \
        or the word is already in the dict:', l, w)
    '''

end = []; tag = []
def insertEnd(l, t):
    tag.append(t); end.append(l)

with open("P100065.conll") as file:
    seg = []; xpos = []
    for index, line in enumerate(file):
        l = line.split('\t')
        if index > 1: 
            seg.append(delA(splitS(l[2])))
            xpos.append(delA(splitX(l[3])))


for x in range(0, len(seg)):
    for p in range(0, len(seg[x])):
        if len(xpos[x]) == len(seg[x]):
            if nun.count(xpos[x][p]) > 0 or xpos[x][p] == 'V':
                ## print("these are words: ", seg[x][p], xpos[x][p])
                insertWord(seg[x][p], xpos[x][p])
            else:
                ## print("this is end: ", seg[x][p], xpos[x][p])
                if not (end.count(seg[x][p]) > 0 and tag.count(xpos[x][p]) > 0):
                    insertEnd(seg[x][p], xpos[x][p])

## Printing for testing

print("*****NOUN HERE*****")
for a in range(0, len(noun)):
    print(noun[a], "\t\t", nmean[a])
print("\n*****VERB BELOW*******")
for b in range(0, len(verb)):
    print(verb[b], "\t", vmean[b])
print("\n*****END BELOW*******\n")
for x in range(len(end)):
    print(end[x], "\t", tag[x])


## Print to use in the `dict` file
print("\n*****NOUN DICT*****\n")
for a in range(0, len(noun)):
    print(noun[a], "\t", ntag[a], "\t", nmean[a])
print("\n*****VERB DICT*******\n")
for b in range(0, len(verb)):
    print(verb[b], "\tV\t", vmean[b])


## Print for use in the `flexion` file
print("\n*****END FLEXION*******\n")
for x in range(len(end)):
    print(f"<{tag[x]}>:{{{end[x]}}}")
