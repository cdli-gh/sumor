# experimental revision

with this mini-prototype, the problem of syllable segmentation is solved, still to be integrated with sumor proper

`analyze.py` is not an API, but a demo to illustrate both generation and analysis
- reads English gloss, optionally followed by Sumerian case flags, e.g., `scribe<GEN><ERG>`
- looks up Sumerian translation
- generates deep morphology
- maps to cuneiform characters
- generates deep morphology from these
- looks up English translation
- restores original input

build with

	`make`

test with

	`make test`

## Building the sign list

Key to this enterprise is to extend `signs.tsv`.

In order to do that, process one or more CDLI-CoNLL files and return transcriptions that cannot be reproduced. Then, extend `signs.tsv` manually.

To evaluate against `P100065.conll`, as an example:

- build transducers

		make

- write log to `transcript.log`:

		python3 P100065.conll > transcript.log

Check manually.

Note that not all errors returned are to be addressed in `signs.tsv`. As a rule of thumb, if entire syllables are left implicit in the writing, do not try to fix that. Frequenly, the morpheme `=ak` (for genitive case) isn't written, but put into annotation. 