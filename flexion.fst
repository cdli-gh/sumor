% Define the set of valid symbol pairs for the two-level rules.
% The symbol = is used to mark the boundary between the stem and
% the inflectional suffix. It is deleted here.
% \$ is the end symbol
%ALPHABET = [\-A-Za-z0-9é] [\.\=0]:<>

% Read the lexical items from a separate file
$WORDS$ = "lexicon"

% morphophonological rules: generating surface forms
% remove empty morphemes
%$R0$ = {\=0}<=><>

ALPHABET = [\-A-Za-z0-9éú] [\.\=0]:<>
$R0$ = (\=:<>) 0<=><>

ALPHABET = [\=A-Za-z0-9éú] [\.\-0]:<>
$R1$ = (\-:<>) 0<=><>

$SPELLOUT$ = $R0$ || $R1$

% transliteration
% insertion of character separators and sign numbers seems to be *impossible*
% so we work with a representation that strips off all

 ALPHABET = [\-A-Za-z0-9éú]  k:[k<>]
 $k#$ = \
      k <=> k (.:[aeiou])

 ALPHABET = [\-A-Za-z0-9éú]  g:[g<>]
 $g#$ = \
      g <=> g (.:[aeiou])

ALPHABET = [\-A-Za-z0-9éú]  m:[m<>] n:[n<>]
$n$ =   [mn] <=> <> (.:n)

ALPHABET = [\-A-Za-z0-9éú]  m:[m<>] n:[n<>]
$r$ =   [mn] <=> <> (.:r)

ALPHABET = [\-A-Za-z0-9éú]  a:[a<>]
$gen$ = \
     a <=> <> (.:ka)

$TRANSLIT$ = $gen$ || $g#$ || $k#$ || $n$ || $r$

% morphological rules: generating deep morphology

% Define a transducer for case endings
% There can be multiple case endings in Sumerian
$NCASE$ = <GEN>:{ak}? <ABL>:{ta}?
$CASE$ = <ABS>:{0} | <ERG>:{e} | $NCASE$

% rudimentary verbal morphology
% http://oracc.museum.upenn.edu/etcsri/parsing/index.html#VPT
% abbreviations partially changed to match Jagersma
$V1$ = <NEG>:{nu} | <MOD1>:{ha} | <ANT1>:u
$V2$ = <MOD2>:{ga} | <MOD3>:{nan} | <MOD4>:{bara} | <MOD5>:{nusz} | <MOD6>:{szi} \
       <MOD7>:{na} | <FIN>:i |<FIN>:{ii} | <FIN>:a | <FIN>:{aa}
$V3$ = <COOR>:{nga}
$V4$ = <VENT>:m | <VENT>:{mu}   % ETSCRI: <VEN>
$V5$ = <MID>:{ba} | <MID>:b
$V6$ = <2SG>:r | <2SG>:e | <3SGH>:{nn} | <1PL>:{mee} | <3PL>:{nnee}
$V7$ = <DAT>:a
$V8$ = <COM>:{da}
$V9$ = <ABL>:{ta} | <TERM>:{szi} | <TERM>:{sze}
$V10$ = <L1>:{ni} | <L1>:n | <L2>:i | <L2>:e | <L2>:0 | <L3>:i
$V11$ = <2SGA>:e | <3SGH>:n | <1SGA_OB>:n | <3SGNH>:b | <3PLHP>:{nnee}
$V13$ = <PF>:{ed} | <PL>:{en}
$V14$ = <1SG>:{en} | <2SG>:{en} | <3SG>:0 | <3SGA>:e | <3SGS_OB>:e | \
        <1PL>:{enden} | <2PL>:{enzen} | <3PL>:{esz} | <3PLA>:{enee}
$V15$ = <SUB>:a

% Concatenate the lexical forms and the inflectional endings and
% put a morpheme boundary in between which is not printed in the analysis
$GENERATE$ = \
  $WORDS$ <NOUN>:<> | \
  %  $WORDS$ <NOUN>:<> (<>:\= $NCASE$)* <>:\= $CASE$
  % works, but it's safer to limit recursion depth
  $WORDS$ <NOUN>:<> <>:\= $CASE$ | \
  $WORDS$ <NOUN>:<> <>:\= $NCASE$ <>:\= $CASE$  | \
  $WORDS$ <NOUN>:<> <>:\= $NCASE$ <>:\= $NCASE$ <>:\= $CASE$ |\
  $WORDS$ <NOUN>:<> <>:\= $NCASE$ <>:\= $NCASE$ <>:\= $NCASE$ <>:\= $CASE$ | \
  ($V1$ <>:\-)? \
  ($V2$ <>:\-)? \
  ($V3$ <>:\-)? \
  ($V4$ <>:\-)? \
  ($V5$ <>:\-)? \
  ($V6$ <>:\- \
    % as soon as one of the following is used, V6 is obligatory
    ($V7$ <>:\-)? \
    ($V8$ <>:\-)? \
    ($V9$ <>:\-)? \
    ($V10$ <>:\-)? )? \
  ($V11$ <>:\-)? \
  $WORDS$ <VERB>:<> \
  (<>:\- $V13$)? \
  (<>:\- $V14$)? \
  (<>:\- $V15$)?

% Apply the two level rules
% we actually do three levels: transliteration
% The result transducer is stored in the output file
$GENERATE$ || $SPELLOUT$  || $TRANSLIT$

% skip $SPELLOUT$ to generate deep morphology from features
