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