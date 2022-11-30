import argparse, sys,os,re,traceback

args=argparse.ArgumentParser(description="generate FST test data from CoNLL-CDLI files, write to stdout")
args.add_argument("files", type=str, nargs="+", help="CoNLL-CDLI files")
args=args.parse_args()

print("# generated with the following command:\n#\t$> python3 "+" ".join(sys.argv))
print()

for file in args.files:
	with open(file,"rt",errors="ignore") as input:
		print(f"# {file}")
		for line in input:
			if not "FORM" in line:
				try:
					line=line.strip().split("\t")
					if len(line)>3:
						orth=line[1]
						segm=line[2]
						morph=line[3]

						lemma=re.sub(r"([^\-]\[[^\-]+\])(\[)?[\-].*",r"\1",segm)
						lemma=re.sub(r".*\-","",lemma)

						pos=morph.split(".")[0]
						template=["",""]
						for x in ["NF.V","V","N","NU"]:
							if "."+x+"." in morph or morph.startswith(x+".") or morph.endswith("."+x) or morph ==x:
								pos=x
								break
						if morph!=pos:
							if morph.startswith(pos+"."):
										template[1]=morph[len(pos)+1:]
							elif morph.endswith("."+pos):
										template[0]=morph[0:-len(pos)-1]
							else:
										template=morph.split("."+pos+".")
							tmp=template
							template=[]
							for part in tmp:
								template.append("".join(["<"+t+">" for t in part.split(".") if len(t)>0]))

						stemplate=["",""]
						s=segm.split("-")

						if len(template[0])>1:
							stemplate[0]="=".join(s[0:len(template[0].split(">"))-1])
						if len(template[1])>1:
							stemplate[1]="=".join(s[1-len(template[1].split(">")):])
						stemplate=["".join(re.sub(r"[\[\]]","\t",st).split()).strip() for st in stemplate ]
						if len(stemplate[0])>0:
							stemplate[0]=stemplate[0]+"="
						if len(stemplate[1])>0:
							stemplate[1]="="+stemplate[1]
						
						# print(template,stemplate)

						if pos.endswith("N"):
							pos="N"

						if not re.match(".+\[.*",lemma):
							sys.stderr.write(f"ERROR: lemma extraction error in \"{segm}\" => \"{lemma}\", skipping\n")
						elif not re.match("^([A-Z]+|NF.V)$",pos):
							sys.stderr.write(f"ERROR: pos extraction error in \"{morph}\" => \"{pos}\", skipping\n")
						else:
							lemma=re.sub(r"[\[\]]","\t",lemma).split()
							translation=lemma[1]
							if re.match("^[0-9]+$",translation.strip()):
								translation=lemma[0]
							lemma=lemma[0]
							
							# template as used in original test.tsv
							template="".join([template[0],translation,template[1]])
							stemplate="".join([stemplate[0],lemma,stemplate[1]])
							
							# # revised template, includes POS tag (after translation)
							# # TODO: please update scripts to this one
							# template="".join([template[0],translation,f"<{pos}>",template[1]])

							# print(segm,morph,orth)
							# print("=>",lemma, pos, translation)
							print(template,stemplate,orth)
							# print()
				except Exception:
					traceback.print_exc()
		print()


# # (1*)
# ruler<ABS> ensi2.k=0 ensi2
# ruler<GEN><ERG> ensi2.k=ak=e ensi2-ka-ke4


# o.3.2   5(disz)-am3     5(disz)[one][-ak]-am    NU.GEN.COP-3-SG _       _       _
# o.3.3   zal-la  zal[pass]-a     NF.V.PT _       _       _
