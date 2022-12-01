import sfst
import sys,os,re,traceback,argparse

fst="sumor.a"
dicts=["dict.tsv"]

args=argparse.ArgumentParser(description="""parse and generate Sumerian toy grammar.
We read text from stdin, if it is tab-separated, we consider the second column to be the gold data and create * for mismatches""")
args.add_argument("fst", type=str, nargs="?", help="compiles sfst, defaults to "+fst, default=fst)
args.add_argument("-d","--dicts", type=str, nargs="*", action="extend",
    help="dictionaries in TSV format, cols: LEMMA<TAB>POS<TAB>GLOSS[<TAB>...], defaults to "+str(dicts))
args=args.parse_args()

if args.dicts==None or len(args.dicts)==0:
    args.dicts=dicts

en2sums={}
sum2en={}

for file in args.dicts:
    # print(file)
    with open(file,"r") as input:
        for line in input:
            line=re.sub(r"\s+"," ",line.strip())
            fields=line.split()
            # print(fields)
            if not line.startswith("#") and len(fields)>2:
                sum=fields[0]+"/"+fields[1]
                en=fields[2]
                if not en in en2sums:
                    en2sums[en] = [sum]
                elif not sum in en2sums[en]:
                    en2sums[en].append(sum)
                if not sum in sum2en:
                    sum2en[sum]= en

print(list(en2sums.items())[0])
print(list(sum2en.items())[0])

sfst.init(args.fst)
sys.stderr.write("generate> ")
sys.stderr.flush()

correct = 0
total = 0
for line in sys.stdin:
    line=line.strip()
    if len(line)==0:
        break
    if not line.startswith("#"):
        gold=None
        if len(line.split())>1:
            gold=line.split()[1]
            line=line.split()[0]
            total += 1
        gloss=re.sub(r"<[^>]*>","",line)
        if gloss in en2sums:
            for sum in en2sums[gloss]:
                print(sum)
                key=line[0:line.index(gloss)]+sum+line[line.index(gloss)+len(gloss):]
                print(key)
                for form in sfst.generate(key):
                    if gold!=None and form!=gold and re.sub(r"[^a-z]","",form)!=re.sub(r"[^a-z]","",gold):
                        print("\t*"+form+" ("+gold+")")
                    else:
                        for analysis in sfst.analyse(form):
                            amatch=" "
                            result=""
                            if analysis!=key:
                                amatch="*"
                            else:
                                for lemma in sum2en:
                                    if lemma in analysis:
                                        result=analysis[0:analysis.index(lemma)]+sum2en[lemma]+analysis[analysis.index(lemma)+len(lemma):]
                                        break
                            if amatch != "*":
                                correct += 1
                            print("\t "+form+"\t"+str(gold)+"\t"+amatch+analysis+"\t"+result)
        if gold!=None:
            sys.stdout.write("\n")
        sys.stderr.write("generate> ")
        sys.stderr.flush()
sys.stderr.write(f'Total analysis: {total}, Correct analysis: {correct}\n')