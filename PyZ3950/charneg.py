#!/usr/bin/env python

assert (0)
# XXX shouldn't use, absorbed into z3950_2001.py

#from PyZ3950 import asn1
import asn1

InitialSet=asn1.SEQUENCE ([('g0',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1),
    ('g1',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1),
    ('g2',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1),
    ('g3',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1),
    ('c0',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('c1',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1)])

PrivateCharacterSet=asn1.CHOICE ([('viaOid',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER))),
    ('externallySpecified',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('previouslyAgreedUpon',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL))])

LeftAndRight=asn1.SEQUENCE ([('gLeft',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('gRight',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1)])

Iso10646=asn1.SEQUENCE ([('collections',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('encodingLevel',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OID),0)])

LanguageCode=asn1.GeneralString

Environment=asn1.CHOICE ([('sevenBit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('eightBit',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL))])

Iso2022=asn1.CHOICE ([('originProposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('proposedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment),1),
        ('proposedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER)),0),
        ('proposedInitialSets',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InitialSet)),0),
        ('proposedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight),0)]))),
    ('targetResponse',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('selectedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment),0),
        ('selectedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER)),0),
        ('selectedinitialSet',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InitialSet),0),
        ('selectedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight),0)])))])

TargetResponse=asn1.SEQUENCE ([('selectedCharSets',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet)),
        ('none',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),1),
    ('selectedLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),LanguageCode),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)])

OriginProposal=asn1.SEQUENCE ([('proposedCharSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet))]))),1),
    ('proposedlanguages',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (LanguageCode)),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)])
CharSetandLanguageNegotiation=asn1.CHOICE ([('proposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),OriginProposal)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),TargetResponse))])
