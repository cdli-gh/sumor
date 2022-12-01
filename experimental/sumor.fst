ALPHABET=[a-zA-Z0-9_]

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
$OLD_PREP$ =\
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

$MORPH$ || [a-zA-Z0-9=]+ || $JOIN$ || "<orth.a>"
