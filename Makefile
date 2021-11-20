all:
		cut -d " " -f 1 dict.tsv > lexicon
		fst-compiler flexion.fst flexion.a

test: all
#		fst-generate flexion.a
#		cat lexicon | perl -pe 's/\s+/ /g;'
#		echo;
#		fst-mor flexion.a
	cut -d ' ' -f 1,3 test.tsv | python3 analyze.py
