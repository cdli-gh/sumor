'''
Uncomment the comments to see the background work happening and
some of the alerts such as of unknown tags for words which will most
probably be for the nouns.
'''


import re
import os,sys
import argparse

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
    ##    out.write(x, end="\t")
    ## out.write("\n")

    if nun.count(w) > 0:
        
        ##out.write(w, '\n')
        if len(a) == 1:
            noun.append(a[0])
            nmean.append(a[0])
            ntag.append(w)
            return
        elif len(a) == 0:
            return
        if not (noun.count(a[0]) > 0 and nmean.count(a[1]) > 0) and len(a[0]) > 1:
            ##out.write(a)
            noun.append(a[0])
            if len(a) >= 2 and w != 'PN':
                nmean.append(a[1])
            else:
                nmean.append(a[0])
            ntag.append(w.replace(' ', ''))

        ## else:
            ## out.write("Duplicate NOUN")
    elif w == 'V' and len(a[0]) > 1:
        if len(a) > 1:
            if not (verb.count(a[0]) > 0 and vmean.count(a[1]) > 0):
                ## out.write("verb added: ", a[0], a[1])
                verb.append(a[0])
                vmean.append(a[1])
            elif len(a) == 1:
                verb.append(a[0])
                verb.append(a[0])
    elif not (tag.count(w) > 0 and end.count(l) > 0) \
        and l.count('_') == 0 and w.count('_') == 0 \
            and len(l) > 0 and len(w) > 0:
        end.append(l); tag.append(w)

if __name__=="__main__":

    out=sys.stderr

    args=argparse.ArgumentParser(description="bootstrap FST grammar from CDLI-CoNLL morphology annotations")
    args.add_argument("--src","-s",type=str,help="directory with source files, defaults to working directory; no recursion",default=".")
    args.add_argument("--tgt","-t",type=str,help="directory with target files, if omitted, just log to stdout", default=None)
    args=args.parse_args()

    for file in os.listdir(args.src):
        if file.endswith('.conll'):
            with open(file) as f:
                for index, line in enumerate(f):
                    l = line.split('\t')
                    if index > 1 and len(l) > 2: 
                        seg = splitS(l[2])
                        xpos = splitX(l[3])

                        if len(seg) == len(xpos):
                            for x in range(len(seg)):
                                ## out.write(seg[x], xpos[x])
                                insertWord(seg[x], xpos[x])
                        ## else:
                            ## out.write('length not equal', seg, xpos)
                         # out.write("line: ", index, " file", file)

    # write proto-FST files in the target directory
    if args.tgt!=None:
        if not os.path.exists(args.tgt):
            os.makedirs(args.tgt)
        output=os.path.join(args.tgt,"dict.tsv")
        if os.path.exists(output):
            raise Exception(f"output file {output} found, remove before running!")
        with open(output,"wt") as output:
            for n,t,m in sorted(set(zip(noun,ntag,nmean))):
                output.write("\t".join([n,t,m])+"\n")
            for v,m in sorted(set(zip(verb,vmean))):
                t="V"
                output.write("\t".join([v,t,m])+"\n")
            # tbc: space or tab as delimiter?

    ## Printing for testing
    if args.tgt==None:
        out=sys.stdout

    '''
    out.write("*****NOUN HERE*****")
    for a in range(0, len(noun)):
        out.write(noun[a], "\t\t", nmean[a])
    out.write("\n*****VERB BELOW*******")
    for b in range(0, len(verb)):
        out.write(verb[b], "\t", vmean[b])
    out.write("\n*****END BELOW*******\n")
    for x in range(len(end)):
        out.write(end[x], "\t", tag[x])
    '''

    ## Print to use in the `dict` file
    out.write("\n*****NOUN DICT*****\n")
    for a in range(0, len(noun)):
        out.write(noun[a]+"\t"+ntag[a]+"\t"+nmean[a]+"\n")
    out.write("\n*****VERB DICT*******\n")
    for b in range(0, len(verb)):
        out.write(verb[b]+"\tV\t"+vmean[b]+"\n")


    ## Print for use in the `flexion` file
    out.write("\n*****END FLEXION*******\n")
    for x in range(len(end)):
        out.write(f"<{tag[x]}>:{{{end[x]}}}\n")

    out.write(f'\nNo. of Nouns: {len(noun)} Verbs: {len(verb)} Ends: {len(end)}\n')
