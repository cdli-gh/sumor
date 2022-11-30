# SuMor -- Sumerian SFST grammar

Toy grammar based on Jagersma, Chap.5, built with SFST. Note that this follows some Jagersma conventions that you won't find in ETCSRI or CDLI. In particular, morphological segmentation is marked by either `=` (nouns) or `-` (verbs).

## Quickstart

Run

    $> make

to compile the fst grammar.

Under Python, then

    import sfst
    sfst.init(flexion.a)

    input=["ensike", "é"]

    for form in input:
        for analysis in sfst.analyse(form):
            print(form,"=>",analysis)

Note that we do not support transcripts as input yet, but require transliterations. The library will be considered operational if it is able to process `input=["ensi2-ke4", "e2"]`, instead.

## Description

On Ubuntu, this requires the [`sfst` package](https://launchpad.net/ubuntu/xenial/+package/sfst) to be installed.
For other systems, see [the Apertium wiki](https://wiki.apertium.org/wiki/SFST). General documentation on [Helmut Schmid's SFST page](https://www.cis.uni-muenchen.de/~schmid/tools/SFST/). Sources on [GitHub](https://github.com/santhoshtr/sfst).

In addition to that, we use the [SFST Python module](https://pypi.org/project/sfst/]).

Build and test using

    $> make test

The system consists of two main components, a [toy lexicon](dict.tsv) of Sumerian roots and English glosses and a
small SFST morphology. Given an English word plus required morphological features, say `ruler<GEN><ERG>`, we perform a lookup in the dictionary, retrieve the Sumerian root(s) (`ensi2.k`) and part(s) of speech (`NOUN`), and construct the *input* to SFST generation (`ensi2.k<NOUN><GEN><ERG>`).

The [SFST grammar](flexion.fst) applies three main finite state automata:
- `$GENERATE$` produces the deep morphology (it directly implements slot information according to ETCSRI). For the input `ensi2.k<NOUN><GEN><ERG>`, this currently produces `ensi2.k=ak=e`.
- `$SPELLOUT$` uses the output of `$GENERATE$` to produce a surface string. It eliminates morpheme boundaries and zero morphemes (for the example, this currently produces `ensi2kake`).
- `$TRANSLIT$` uses the output of `$SPELLOUT$` to produce an orthographic representation (at the moment, this filters out certain allophones and eliminates the "silent" *k* in roots like `ensi2.k` where it is final)

Ideally, `$TRANSLIT$` would actually predict cuneiform characters. Currently, it does not, as we found no way to insert character boundaries. Likewise, not all unwritten characters (`mu*n*-rú`) are eliminated.

The main call in the transducer is

    $GENERATE$ || $SPELLOUT$ || $TRANSLIT$

If you comment out, say, the second step, you can inspect intermediate representations:

    $GENERATE$ % || $SPELLOUT$ || $TRANSLIT$

As long as we cannot generate a CDLI-compliant string representation, the suggested workflow should
take a CDLI string, drop character boundaries and indices and use that as input. However, then,
the lexicon needs to be adjusted, and subscripts (indices) must be dropped there, as well.

Interactive demo of generation (from English gloss + grammatical features) and analysis (of the generated forms):

    $> python3 analyze.py

If you enter a word with features (say, `ruler<ABS>`), it will construct all "surface forms" and then provide all analyses of these surface forms. Analyses that are not identical with the input are marked by `*` (this does not say that these are incorrect). For the target analysis, we consult the bidictionary to predict the gloss.

For evaluation, you can optionally provide a "gold" surface form. Only if the predicted surface is a loose match (modulo subscripts and character boundaries), an analysis is performed, so you can use that to test both generation and analysis. Surface forms that do not match are marked with `*`.

## Known issues

- At the moment, only the bidictionary defines the part of speech. This means that `$GENERATE$` will always
attempt to return both verbal and nominal analyses.
- `$GENERATE$` does not do full nominal slots, but only (selected) cases
- `$TRANSLIT$` does not do character segmentation/mapping to characters
- `$SPELLOUT$` uses impossible allomorphs (`mnrú` [ > `rú`] instead of `munrú` [ > `mu-rú`])
- `$TRANSLIT$` lets some impossible forms (`*mrú`) slip through
- We have a coverage of one IGT gloss and three roots ;)

## History

- 2021-11-21 created: basic setup, 3 roots [CC]

## Contributors

CC - Christian Chiarcos, GU Frankfurt
