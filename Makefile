all:
		cut -d " " -f 1 dict.tsv > lexicon
		fst-compiler flexion.fst flexion.a

test_cdli:
	# update to YOUR CDLI files:
	cut -d " " -f 1 dict.tsv > lexicon
	fst-compiler flexion.fst flexion.a
	st-generate flexion.a
	at lexicon | perl -pe 's/\s+/ /g;'
	cho;
	st-mor flexion.a
	
	#  test on CDLI files
	cut -f " " -f 1,3 test.cdli.tsv | python3 analyze.py flexion.a -d test.dict.tsv
	## use -f 1,2 to evaluate morphological forms, but then lexicon, etc., must be adapted

test: all
#		fst-generate flexion.a
#		cat lexicon | perl -pe 's/\s+/ /g;'
#		echo;
#		fst-mor flexion.a
	cut -d ' ' -f 1,3 test.cdli.tsv | python3 analyze.py
