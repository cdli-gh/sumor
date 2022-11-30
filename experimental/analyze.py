import sfst
import sys,os,re,traceback,argparse

fst="sumor.a"
dicts=["dict.tsv"]

args=argparse.ArgumentParser(description="""translit.
We read text from stdin, if it is tab-separated, we consider the second column to be the gold data and create * for mismatches""")
args.add_argument("fst", type=str, nargs="?", help="compiles sfst, defaults to "+fst, default=fst)
args=args.parse_args()

sfst.init(args.fst)
sys.stderr.write("generate> ")
sys.stderr.flush()

for line in sys.stdin:
    line=line.strip()
    if len(line)==0:
        break
    if not line.startswith("#"):
        for key in line.split():
            orig_key=key
            forms=sfst.generate(key)
            if len(forms)==0:
                print(key+"\t**"+key)
            else:
                for form in forms:
                    if orig_key in sfst.analyse(form):
                        print(key+"\t*"+form)
                        key=" "*len(key)
                    for ana in sfst.analyse(form):
                        print(key+"\t*"+form+"\t"+ana)
        sys.stderr.write("generate> ")
        sys.stderr.flush()
sys.stderr.write("bye!\n")
