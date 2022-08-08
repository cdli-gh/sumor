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

end = []; tag = []
noun = []; verb = []; end = []
nmean = []; vmean = []
ntag = []
nun = ['N', 'NU', 'PN', 'HN', 'MP', 'MN', 'CNJ', 'RN', 'FN', 'DN', 'SN', \
    'AN', 'TN', 'GN', 'ON', 'WN', 'EN']

def insertWord(p, r):
    ## Ignoring cases when the length of segmented SEGM and XPOSTAG are different
    l = delBr(p)
    w = r.replace('\n', '')

    div = re.compile(r"[A-Za-z0-9\(\)_ø'\/]+")
    a = div.findall(p)
    ## for x in a:
    ##    print(x, end="\t")
    ## print("\n")

    if nun.count(w) > 0:
        
        ##print(w, '\n')
        if len(a) == 1:
            noun.append(a[0])
            nmean.append(a[0])
            ntag.append(w)
            return
        elif len(a) == 0:
            return
        if not (noun.count(a[0]) > 0 and nmean.count(a[1]) > 0) and len(a[0]) > 1:
            ##print(a)
            noun.append(a[0])
            if len(a) >= 2 and w != 'PN':
                nmean.append(a[1])
            else:
                nmean.append(a[0])
            ntag.append(w.replace(' ', ''))

        ## else:
            ## print("Duplicate NOUN")
    elif w == 'V' and len(a[0]) > 1:
        if len(a) > 1:
            if not (verb.count(a[0]) > 0 and vmean.count(a[1]) > 0):
                ## print("verb added: ", a[0], a[1])
                verb.append(a[0])
                vmean.append(a[1])
            elif len(a) == 1:
                verb.append(a[0])
                verb.append(a[0])
    elif not (tag.count(w) > 0 and end.count(l) > 0) \
        and l.count('_') == 0 and w.count('_') == 0 \
            and len(l) > 0 and len(w) > 0:
        end.append(l); tag.append(w)

for file in os.listdir():
    if file.endswith('.conll'):
        with open(file) as f:
            for index, line in enumerate(f):
                l = line.split('\t')
                if index > 1 and len(l) > 2: 
                    seg = splitS(l[2])
                    xpos = splitX(l[3])

                    if len(seg) == len(xpos):
                        for x in range(len(seg)):
                            ## print(seg[x], xpos[x])
                            insertWord(seg[x], xpos[x])
                    ## else:
                        ## print('length not equal', seg, xpos)
                     # print("line: ", index, " file", file)

## Printing for testing
'''
print("*****NOUN HERE*****")
for a in range(0, len(noun)):
    print(noun[a], "\t\t", nmean[a])
print("\n*****VERB BELOW*******")
for b in range(0, len(verb)):
    print(verb[b], "\t", vmean[b])
print("\n*****END BELOW*******\n")
for x in range(len(end)):
    print(end[x], "\t", tag[x])
'''
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

print(f'\nNo. of Nouns: {len(noun)} Verbs: {len(verb)} Ends: {len(end)}')
