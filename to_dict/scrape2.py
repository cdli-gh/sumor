'''
Uncomment the comments to see the background work happening and
some of the alerts such as of unknown tags for words which will most
probably be for the nouns.
'''



import re
import os

NoneType = type(None)

def splitS(list):
    return list.split('-')

def splitX(list):
    return list.split('.')

## Delete endbrackets
def delA(y):
    r = []
    for a in y:
        r.append(delB(a))
    return r

def delB(x):
    r = x

    rex = re.search('\[+$', x)
    if type(rex) == NoneType:
        return r
    else:
        return r[:-1]
    
def delBr(l):
    a = l.replace('[', '')
    return a.replace(']', '')

noun = []; verb = []; end = []
nmean = []; vmean = []
ntag = []
nun = ['N', 'NU', 'PN', 'HN', 'MP', 'MN', 'CNJ', 'RN']

def insertWord(l, w):
    div = re.compile(r'[A-Za-z0-9\(*\w\)]+?(?=\[|\])')
    a = div.findall(l)
    ## Ignoring cases when the length of segmented SEGM and XPOSTAG are different
    if nun.count(w) > 0:
        if not (noun.count(a[0]) > 0 and nmean.count(a[1]) > 0):
            noun.append(a[0].replace(' ', ''))
            nmean.append(a[1].replace(' ', ''))
            ntag.append(w.replace(' ', ''))
        else:
            print("Duplicate NOUN")
    elif w == 'V':
        if not (verb.count(a[0]) > 0 and vmean.count(a[1]) > 0):
            print("verb added: ", a[0], a[1])
            verb.append(a[0].replace(' ', ''))
            vmean.append(a[1].replace(' ', ''))
    else:
        print('Weird thing happened unknown tag', l, w)

end = []; tag = []
def insertEnd(l, t):
    tag.append(t); end.append(delBr(l))

## only for testing
tested = []

for file in os.listdir():
    if file.endswith('.conll'):
        with open(file) as f:
            seg = []; xpos = []
            for index, line in enumerate(f):
                l = line.split('\t')
                if index > 1 and len(l) > 2: 
                    seg.append(delA(splitS(l[2])))
                    xpos.append(delA(splitX(l[3])))
                    ## print("line: ", index, " file", file)
        tested.append(file)


for x in range(0, len(seg)):
    for p in range(0, len(seg[x])):
        print(xpos[x])
        print(seg[x])
        if len(xpos[x]) == len(seg[x]):
            if nun.count(xpos[x][p]) > 0 or xpos[x][p] == 'V':
                print("these are words: ", seg[x][p], xpos[x][p])
                insertWord(seg[x][p], xpos[x][p])
            else:
                print("this is end: ", seg[x][p], xpos[x][p])
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


print(tested)
