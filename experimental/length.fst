% in syllabic scripts, vowels or consonants at sign boundaries can be written redundantly (plene writing)
% on the other hand, plene writing for expressing length is not systematically applied (i.e., it is not clear whether it is actually used for writing length distinctions)

% in this transducer, we 
% - take in a transcription without morpheme boundaries
% - we eliminate repeated "phonemes"
% - we create alternations:
%   CVC => CVVC, VCV => VCCV
% it's a bit hard to control

ALPHABET=[a-z0-9] 


#=C#=qwertzuiopasdfghjklyxcvnbnmſ

$DEDUP$=\
	( {[#=C#] [#=C#]}:{[#=C#]} | . )

$DUP$=\
	( {[#=C#]} : {[#=C#] [#=C#]} | . )

.* || $DEDUP$* || $DUP$* || \
	[a-z0-9]*