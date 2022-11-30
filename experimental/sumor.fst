ALPHABET=[a-zA-Z0-9\-\=]

% this is where the magic lies ;)
% map signs to syllables or words
% for final-only syllable renderings, you can use $
% otherwise, characters are always followed by -
$syll2sign$ = \
    {ensik}:{ENSI6$} | \
    {ensi}:{ENSI6\-} | \
    {ke}:{ke\-} | \
    {ka}:{ka\-} | \
    {kak}:{ka$} | \
    {mun}:{mu\-} |\
    {mu}:{mu\-} 

$WRITE$ = \
    $syll2sign$*

% works
% $WRITE$*

$OLD_MORPH$ = \
    (.:. | \
    <ABS>:<> | \
    <DAT>:{\=a} | \
    <GEN>:{\=ak}| \
    <ERG>:{\=e})*

$ROOT$ = [a-z0-9\-]+

% adnominal cases: these are special in that they are likely to be iterated
$NCASE$ = \
    <GEN>:{\=ak}

$CASE$ = \
    $NCASE$ | \
    <ABS>:<> | \
    <DAT>:{\=a} | \
    <ERG>:{\=e}

$NOMINAL$ = $ROOT$ {/N}:<> ($NCASE$? $CASE$)?

%$VERBAL$ = $ROOT$

$MORPH$ = \
    $NOMINAL$ %| $VERBAL$

$JOIN$ = \
    ([a-zA-Z0-9]:[a-zA-Z0-9] | \
    \-:<> | \
    \=:<>)*

% convert MTAAC-style annotations to SFST-style annotations
$PREP$ =\
    ([a-z0-9]:[a-z0-9] | \
    {/N}:{/N} | \
    {\.ABS}:<ABS> | \
    {\.GEN}:<GEN> | \
    {\.ERG}:<ERG> | \
    {\.DAT}:<DAT>)*

% remove final $ and -
$CLEANUP$ = \
    ([a-z0-9A-Z\-]:[a-z0-9A-Z\-])* \
    ([a-z0-9A-Z]:[a-z0-9A-Z]) \
    (\$:<> | \-:<>)?

$PREP$ || $MORPH$ || $JOIN$ || $WRITE$ || $CLEANUP$