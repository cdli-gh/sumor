all: dict.tsv
		python3 signs2fst.py signs.tsv > orth.fst
		fst-compiler-utf8 length.fst length.a
		fst-compiler-utf8 orth.fst orth.a
		fst-compiler-utf8 sumor.fst sumor.a

dict.tsv:
	python3 conll2dict.py *conll > dict.tsv

test: all
	cat test.tsv | \
	python3 analyze.py