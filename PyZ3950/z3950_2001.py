#!/usr/bin/env python
# Auto-generated from ../compiler/tests/z3950-2001.txt at Wed, 02 Jun 2004 15:30:47 +0000
from PyZ3950 import asn1
#module Module None
KnownProximityUnit=asn1.INTEGER_class ([('character',1),('word',2),('sentence',3),('paragraph',4),('section',5),('chapter',6),('document',7),('element',8),('subelement',9),('elementType',10),('byte',11)],None,None)
InternationalString=asn1.GeneralString
Specification=asn1.SEQUENCE ([('schema',None,    asn1.CHOICE ([('oid',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER)),
        ('uri',None,asn1.TYPE(asn1.IMPLICIT(300,cls=asn1.CONTEXT_FLAG),InternationalString))]),1),
    ('elementSpec',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('elementSetName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('externalEspec',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))])),1)], seq_name = 'Specification')
ElementSetName=asn1.TYPE(asn1.IMPLICIT(103,cls=asn1.CONTEXT_FLAG),InternationalString)
Permissions=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('userId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('allowableFunctions',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.INTEGER_class ([('delete',1),('modifyContents',2),('modifyPermissions',3),('present',4),('invoke',5)],None,None))),0)], seq_name = None))
DeleteSetStatus=asn1.TYPE(asn1.IMPLICIT(33,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',0),('resultSetDidNotExist',1),('previouslyDeletedByServer',2),('systemProblemAtServer',3),('accessNotAllowed',4),('resourceControlAtClient',5),('resourceControlAtServer',6),('bulkDeleteNotSupported',7),('notAllRsltSetsDeletedOnBulkDlte',8),('notAllRequestedResultSetsDeleted',9),('resultSetInUse',10)],None,None))
PresentStatus=asn1.TYPE(asn1.IMPLICIT(27,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',0),('partial_1',1),('partial_2',2),('partial_3',3),('partial_4',4),('failure',5)],None,None))
StringOrNumeric=asn1.CHOICE ([('string',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('numeric',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)))])
AttributeSetId=asn1.OBJECT_IDENTIFIER
ProximityOperator=asn1.SEQUENCE ([('exclusion',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('distance',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('ordered',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('relationType',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('lessThan',1),('lessThanOrEqual',2),('equal',3),('greaterThanOrEqual',4),('greaterThan',5),('notEqual',6)],None,None)),0),
    ('proximityUnitCode',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('known',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),KnownProximityUnit)),
        ('private',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)))])),0)], seq_name = 'ProximityOperator')
ResourceReport=asn1.EXTERNAL
Options=asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.BITSTRING_class ([('search',0),('present',1),('delSet',2),('resourceReport',3),('triggerResourceCtrl',4),('resourceCtrl',5),('accessCtrl',6),('scan',7),('sort',8),('unused',9),('extendedServices',10),('level_1Segmentation',11),('level_2Segmentation',12),('concurrentOperations',13),('namedResultSets',14),('encapsulation',15),('resultCountInSort',16),('negotiation',17),('dedup',18),('query104',19),('pQESCorrection',20),('stringSchema',21)],None,None))
Unit=asn1.SEQUENCE ([('unitSystem',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('unitType',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),1),
    ('unit',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),StringOrNumeric),1),
    ('scaleFactor',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'Unit')
CloseReason=asn1.TYPE(asn1.IMPLICIT(211,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('finished',0),('shutdown',1),('systemProblem',2),('costLimit',3),('resources',4),('securityViolation',5),('protocolError',6),('lackOfActivity',7),('responseToPeer',8),('unspecified',9)],None,None))
AttributeElement=asn1.SEQUENCE ([('attributeSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),AttributeSetId),1),
    ('attributeType',None,asn1.TYPE(asn1.IMPLICIT(120,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('attributeValue',None,    asn1.CHOICE ([('numeric',None,asn1.TYPE(asn1.IMPLICIT(121,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('complex',None,asn1.TYPE(asn1.IMPLICIT(224,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('list',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),            asn1.SEQUENCE_OF (StringOrNumeric)),0),
            ('semanticAction',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),            asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),1)], seq_name = None)))]),0)], seq_name = 'AttributeElement')
DefaultDiagFormat=asn1.SEQUENCE ([('diagnosticSetId',None,asn1.OBJECT_IDENTIFIER,0),
    ('condition',None,asn1.INTEGER_class ([],None,None),0),
    ('addinfo',None,    asn1.CHOICE ([('v2Addinfo',None,asn1.VisibleString),
        ('v3Addinfo',None,InternationalString)]),0)], seq_name = 'DefaultDiagFormat')
ResourceReportId=asn1.OBJECT_IDENTIFIER
FragmentSyntax=asn1.CHOICE ([('externallyTagged',None,asn1.EXTERNAL),
    ('notExternallyTagged',None,asn1.OCTSTRING)])
Operator=asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),asn1.CHOICE ([('and',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('or',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('and_not',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('prox',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),ProximityOperator))]))
DiagRec=asn1.CHOICE ([('defaultFormat',None,DefaultDiagFormat),
    ('externallyDefined',None,asn1.EXTERNAL)])
ProtocolVersion=asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BITSTRING_class ([('version_1',0),('version_2',1),('version_3',2)],None,None))
Range=asn1.SEQUENCE ([('startingPosition',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('numberOfRecords',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = 'Range')
ReferenceId=asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)
RetentionCriterion=asn1.CHOICE ([('numberOfEntries',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
    ('percentOfEntries',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
    ('duplicatesOnly',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('discardRsDuplicates',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
DuplicateDetectionCriterion=asn1.CHOICE ([('levelOfMatch',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
    ('caseSensitive',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('punctuationSensitive',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('regularExpression',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('rsDuplicates',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
InfoCategory=asn1.SEQUENCE ([('categoryTypeId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('categoryValue',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = 'InfoCategory')
AttributeList=asn1.TYPE(asn1.IMPLICIT(44,cls=asn1.CONTEXT_FLAG),asn1.SEQUENCE_OF (AttributeElement))
ResultSetId=asn1.TYPE(asn1.IMPLICIT(31,cls=asn1.CONTEXT_FLAG),InternationalString)
DatabaseName=asn1.TYPE(asn1.IMPLICIT(105,cls=asn1.CONTEXT_FLAG),InternationalString)
IdAuthentication=asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.CHOICE ([('open',None,asn1.VisibleString),
    ('idPass',None,    asn1.SEQUENCE ([('groupId',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('userId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('password',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None)),
    ('anonymous',None,asn1.NULL),
    ('other',None,asn1.EXTERNAL)]))
SortCriterion=asn1.CHOICE ([('mostComprehensive',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('leastComprehensive',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('mostRecent',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('oldest',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('leastCost',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('preferredDatabases',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)))])
SortKey=asn1.CHOICE ([('privateSortKey',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('elementSpec',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Specification)),
    ('sortAttributes',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('id',None,AttributeSetId,0),
        ('list',None,AttributeList,0)], seq_name = None)))])
ListStatuses=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('id',None,ResultSetId,0),
    ('status',None,DeleteSetStatus,0)], seq_name = None))
OtherInformation=asn1.TYPE(asn1.IMPLICIT(201,cls=asn1.CONTEXT_FLAG),asn1.SEQUENCE_OF (asn1.SEQUENCE ([('category',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InfoCategory),1),
    ('information',None,    asn1.CHOICE ([('characterInfo',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('binaryInfo',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('externallyDefinedInfo',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
        ('oid',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER))]),0)], seq_name = None)))
ResultSetPlusAttributes=asn1.TYPE(asn1.IMPLICIT(214,cls=asn1.CONTEXT_FLAG),asn1.SEQUENCE ([('resultSet',None,ResultSetId,0),
    ('attributes',None,AttributeList,0)], seq_name = 'ResultSetPlusAttributes'))
InitializeResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('protocolVersion',None,ProtocolVersion,0),
    ('options',None,Options,0),
    ('preferredMessageSize',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('exceptionalRecordSize',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('result',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('implementationId',None,asn1.TYPE(asn1.IMPLICIT(110,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('implementationName',None,asn1.TYPE(asn1.IMPLICIT(111,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('implementationVersion',None,asn1.TYPE(asn1.IMPLICIT(112,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('userInformationField',None,asn1.TYPE(asn1.EXPLICIT(11,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'InitializeResponse')
SortElement=asn1.CHOICE ([('generic',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),SortKey)),
    ('datbaseSpecific',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('databaseName',None,DatabaseName,0),
        ('dbSort',None,SortKey,0)], seq_name = None))))])
IntUnit=asn1.SEQUENCE ([('value',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('unitUsed',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Unit),0)], seq_name = 'IntUnit')
ElementSetNames=asn1.CHOICE ([('genericElementSetName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('databaseSpecific',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('dbName',None,DatabaseName,0),
        ('esn',None,ElementSetName,0)], seq_name = None))))])
SortResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('sortStatus',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',0),('partial_1',1),('failure',2)],None,None)),0),
    ('resultSetStatus',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('empty',1),('interim',2),('unchanged',3),('none',4)],None,None)),1),
    ('diagnostics',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1),
    ('resultCount',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'SortResponse')
Term=asn1.CHOICE ([('general',None,asn1.TYPE(asn1.IMPLICIT(45,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
    ('numeric',None,asn1.TYPE(asn1.IMPLICIT(215,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
    ('characterString',None,asn1.TYPE(asn1.IMPLICIT(216,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('oid',None,asn1.TYPE(asn1.IMPLICIT(217,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER)),
    ('dateTime',None,asn1.TYPE(asn1.IMPLICIT(218,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime)),
    ('external',None,asn1.TYPE(asn1.IMPLICIT(219,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('integerAndUnit',None,asn1.TYPE(asn1.IMPLICIT(220,cls=asn1.CONTEXT_FLAG),IntUnit)),
    ('null',None,asn1.TYPE(asn1.IMPLICIT(221,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
InitializeRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('protocolVersion',None,ProtocolVersion,0),
    ('options',None,Options,0),
    ('preferredMessageSize',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('exceptionalRecordSize',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('idAuthentication',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.ANY),1),
    ('implementationId',None,asn1.TYPE(asn1.IMPLICIT(110,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('implementationName',None,asn1.TYPE(asn1.IMPLICIT(111,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('implementationVersion',None,asn1.TYPE(asn1.IMPLICIT(112,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('userInformationField',None,asn1.TYPE(asn1.EXPLICIT(11,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'InitializeRequest')
ExtendedServicesResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('operationStatus',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('done',1),('accepted',2),('failure',3)],None,None)),0),
    ('diagnostics',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ExtendedServicesResponse')
AccessControlResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('securityChallengeResponse',None,    asn1.CHOICE ([('simpleForm',None,asn1.TYPE(asn1.IMPLICIT(38,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('externallyDefined',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))]),1),
    ('diagnostic',None,asn1.TYPE(asn1.EXPLICIT(223,cls=asn1.CONTEXT_FLAG),DiagRec),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'AccessControlResponse')
TriggerResourceControlRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('requestedAction',None,asn1.TYPE(asn1.IMPLICIT(46,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('resourceReport',1),('resourceControl',2),('cancel',3)],None,None)),0),
    ('prefResourceReportFormat',None,asn1.TYPE(asn1.IMPLICIT(47,cls=asn1.CONTEXT_FLAG),ResourceReportId),1),
    ('resultSetWanted',None,asn1.TYPE(asn1.IMPLICIT(48,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'TriggerResourceControlRequest')
AccessControlRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('securityChallenge',None,    asn1.CHOICE ([('simpleForm',None,asn1.TYPE(asn1.IMPLICIT(37,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('externallyDefined',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))]),0),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'AccessControlRequest')
DeleteResultSetResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('deleteOperationStatus',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),DeleteSetStatus),0),
    ('deleteListStatuses',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ListStatuses),1),
    ('numberNotDeleted',None,asn1.TYPE(asn1.IMPLICIT(34,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('bulkStatuses',None,asn1.TYPE(asn1.IMPLICIT(35,cls=asn1.CONTEXT_FLAG),ListStatuses),1),
    ('deleteMessage',None,asn1.TYPE(asn1.IMPLICIT(36,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'DeleteResultSetResponse')
CompSpec=asn1.SEQUENCE ([('selectAlternativeSyntax',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('generic',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Specification),1),
    ('dbSpecific',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('db',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
        ('spec',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Specification),0)], seq_name = None))),1),
    ('recordSyntax',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1)], seq_name = 'CompSpec')
AttributesPlusTerm=asn1.TYPE(asn1.IMPLICIT(102,cls=asn1.CONTEXT_FLAG),asn1.SEQUENCE ([('attributes',None,AttributeList,0),
    ('term',None,Term,0)], seq_name = 'AttributesPlusTerm'))
NamePlusRecord=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),DatabaseName),1),
    ('record',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('retrievalRecord',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
        ('surrogateDiagnostic',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),DiagRec)),
        ('startingFragment',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),FragmentSyntax)),
        ('intermediateFragment',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),FragmentSyntax)),
        ('finalFragment',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),FragmentSyntax))])),0)], seq_name = 'NamePlusRecord')
ResourceReportResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('resourceReportStatus',None,asn1.TYPE(asn1.IMPLICIT(50,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',0),('partial',1),('failure_1',2),('failure_2',3),('failure_3',4),('failure_4',5),('failure_5',6),('failure_6',7)],None,None)),0),
    ('resourceReport',None,asn1.TYPE(asn1.EXPLICIT(51,cls=asn1.CONTEXT_FLAG),ResourceReport),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ResourceReportResponse')
Operand=asn1.CHOICE ([('attrTerm',None,AttributesPlusTerm),
    ('resultSet',None,ResultSetId),
    ('resultAttr',None,ResultSetPlusAttributes)])
SortKeySpec=asn1.SEQUENCE ([('sortElement',None,SortElement,0),
    ('sortRelation',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('ascending',0),('descending',1),('ascendingByFrequency',3),('descendingByfrequency',4)],None,None)),0),
    ('caseSensitivity',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('caseSensitive',0),('caseInsensitive',1)],None,None)),0),
    ('missingValueAction',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('abort',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('null',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('missingValueData',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING))])),1)], seq_name = 'SortKeySpec')
ResourceControlRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('suspendedFlag',None,asn1.TYPE(asn1.IMPLICIT(39,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('resourceReport',None,asn1.TYPE(asn1.EXPLICIT(40,cls=asn1.CONTEXT_FLAG),ResourceReport),1),
    ('partialResultsAvailable',None,asn1.TYPE(asn1.IMPLICIT(41,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('subset',1),('interim',2),('none',3)],None,None)),1),
    ('responseRequired',None,asn1.TYPE(asn1.IMPLICIT(42,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('triggeredRequestFlag',None,asn1.TYPE(asn1.IMPLICIT(43,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ResourceControlRequest')
DuplicateDetectionRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('inputResultSetIds',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),0),
    ('outputResultSetName',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('applicablePortionOfRecord',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('duplicateDetectionCriteria',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DuplicateDetectionCriterion)),1),
    ('clustering',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('retentionCriteria',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (RetentionCriterion)),0),
    ('sortCriteria',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SortCriterion)),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'DuplicateDetectionRequest')
ResourceControlResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('continueFlag',None,asn1.TYPE(asn1.IMPLICIT(44,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('resultSetWanted',None,asn1.TYPE(asn1.IMPLICIT(45,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ResourceControlResponse')
DuplicateDetectionResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('status',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',0),('failure',1)],None,None)),0),
    ('resultSetCount',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('diagnostics',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'DuplicateDetectionResponse')
PresentRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('resultSetId',None,ResultSetId,0),
    ('resultSetStartPoint',None,asn1.TYPE(asn1.IMPLICIT(30,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('numberOfRecordsRequested',None,asn1.TYPE(asn1.IMPLICIT(29,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('additionalRanges',None,asn1.TYPE(asn1.IMPLICIT(212,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Range)),1),
    ('recordComposition',None,    asn1.CHOICE ([('simple',None,asn1.TYPE(asn1.EXPLICIT(19,cls=asn1.CONTEXT_FLAG),ElementSetNames)),
        ('complex',None,asn1.TYPE(asn1.IMPLICIT(209,cls=asn1.CONTEXT_FLAG),CompSpec))]),1),
    ('preferredRecordSyntax',None,asn1.TYPE(asn1.IMPLICIT(104,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('maxSegmentCount',None,asn1.TYPE(asn1.IMPLICIT(204,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxRecordSize',None,asn1.TYPE(asn1.IMPLICIT(206,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxSegmentSize',None,asn1.TYPE(asn1.IMPLICIT(207,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'PresentRequest')
ResourceReportRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('opId',None,asn1.TYPE(asn1.IMPLICIT(210,cls=asn1.CONTEXT_FLAG),ReferenceId),1),
    ('prefResourceReportFormat',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),ResourceReportId),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ResourceReportRequest')
ExtendedServicesRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('function',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('create',1),('delete',2),('modify',3)],None,None)),0),
    ('packageType',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('packageName',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('userId',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('retentionTime',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('permissions',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),Permissions),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('taskSpecificParameters',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('waitAction',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('wait',1),('waitIfPossible',2),('dontWait',3),('dontReturnPackage',4)],None,None)),0),
    ('elements',None,ElementSetName,1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ExtendedServicesRequest')
Close=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('closeReason',None,CloseReason,0),
    ('diagnosticInformation',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('resourceReportFormat',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),ResourceReportId),1),
    ('resourceReport',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),ResourceReport),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'Close')
DeleteResultSetRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('deleteFunction',None,asn1.TYPE(asn1.IMPLICIT(32,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('list',0),('all',1)],None,None)),0),
    ('resultSetList',None,    asn1.SEQUENCE_OF (ResultSetId),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'DeleteResultSetRequest')
OccurrenceByAttributes=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('attributes',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),AttributeList),0),
    ('occurrences',None,    asn1.CHOICE ([('global',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('byDatabase',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (        asn1.SEQUENCE ([('db',None,DatabaseName,0),
            ('num',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
            ('otherDbInfo',None,OtherInformation,1)], seq_name = None))))]),1),
    ('otherOccurInfo',None,OtherInformation,1)], seq_name = None))
Records=asn1.CHOICE ([('responseRecords',None,asn1.TYPE(asn1.IMPLICIT(28,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (NamePlusRecord))),
    ('nonSurrogateDiagnostic',None,asn1.TYPE(asn1.IMPLICIT(130,cls=asn1.CONTEXT_FLAG),DefaultDiagFormat)),
    ('multipleNonSurDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(205,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)))])
Segment=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('numberOfRecordsReturned',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('segmentRecords',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (NamePlusRecord)),0),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'Segment')
TermInfo=asn1.SEQUENCE ([('term',None,Term,0),
    ('displayTerm',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('suggestedAttributes',None,AttributeList,1),
    ('alternativeTerm',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributesPlusTerm)),1),
    ('globalOccurrences',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('byAttributes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),OccurrenceByAttributes),1),
    ('otherTermInfo',None,OtherInformation,1)], seq_name = 'TermInfo')
SearchResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('resultCount',None,asn1.TYPE(asn1.IMPLICIT(23,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('numberOfRecordsReturned',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('nextResultSetPosition',None,asn1.TYPE(asn1.IMPLICIT(25,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('searchStatus',None,asn1.TYPE(asn1.IMPLICIT(22,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('resultSetStatus',None,asn1.TYPE(asn1.IMPLICIT(26,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('subset',1),('interim',2),('none',3)],None,None)),1),
    ('presentStatus',None,PresentStatus,1),
    ('records',None,Records,1),
    ('additionalSearchInfo',None,asn1.TYPE(asn1.IMPLICIT(203,cls=asn1.CONTEXT_FLAG),OtherInformation),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'SearchResponse')
Entry=asn1.CHOICE ([('termInfo',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),TermInfo)),
    ('surrogateDiagnostic',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),DiagRec))])
RPNStructure=asn1.CHOICE ([('op',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Operand)),
    ('rpnRpnOp',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
ScanRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('databaseNames',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DatabaseName)),0),
    ('attributeSet',None,AttributeSetId,1),
    ('termListAndStartPoint',None,AttributesPlusTerm,0),
    ('stepSize',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('numberOfTermsRequested',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('preferredPositionInResponse',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ScanRequest')
PresentResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('numberOfRecordsReturned',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('nextResultSetPosition',None,asn1.TYPE(asn1.IMPLICIT(25,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('presentStatus',None,PresentStatus,0),
    ('records',None,Records,1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'PresentResponse')
SortRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('inputResultSetNames',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),0),
    ('sortedResultSetName',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('sortSequence',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SortKeySpec)),0),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'SortRequest')
ListEntries=asn1.SEQUENCE ([('entries',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Entry)),1),
    ('nonsurrogateDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1)], seq_name = 'ListEntries')
RPNQuery=asn1.SEQUENCE ([('attributeSet',None,AttributeSetId,0),
    ('rpn',None,RPNStructure,0)], seq_name = 'RPNQuery')
ScanResponse=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('stepSize',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('scanStatus',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',0),('partial_1',1),('partial_2',2),('partial_3',3),('partial_4',4),('partial_5',5),('failure',6)],None,None)),0),
    ('numberOfEntriesReturned',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('positionOfTerm',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('entries',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),ListEntries),1),
    ('attributeSet',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),AttributeSetId),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'ScanResponse')
RpnRpnOp=asn1.SEQUENCE ([('rpn1',None,RPNStructure,0),
    ('rpn2',None,RPNStructure,0),
    ('op',None,Operator,0)], seq_name = 'RpnRpnOp')
Query=asn1.CHOICE ([('type_0',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.ANY)),
    ('type_1',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),RPNQuery)),
    ('type_2',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
    ('type_100',None,asn1.TYPE(asn1.EXPLICIT(100,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
    ('type_101',None,asn1.TYPE(asn1.IMPLICIT(101,cls=asn1.CONTEXT_FLAG),RPNQuery)),
    ('type_102',None,asn1.TYPE(asn1.EXPLICIT(102,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
    ('type_104',None,asn1.TYPE(asn1.IMPLICIT(104,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))])
SearchRequest=asn1.SEQUENCE ([('referenceId',None,ReferenceId,1),
    ('smallSetUpperBound',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('largeSetLowerBound',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('mediumSetPresentNumber',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('replaceIndicator',None,asn1.TYPE(asn1.IMPLICIT(16,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('resultSetName',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('databaseNames',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DatabaseName)),0),
    ('smallSetElementSetNames',None,asn1.TYPE(asn1.EXPLICIT(100,cls=asn1.CONTEXT_FLAG),ElementSetNames),1),
    ('mediumSetElementSetNames',None,asn1.TYPE(asn1.EXPLICIT(101,cls=asn1.CONTEXT_FLAG),ElementSetNames),1),
    ('preferredRecordSyntax',None,asn1.TYPE(asn1.IMPLICIT(104,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('query',None,asn1.TYPE(asn1.EXPLICIT(21,cls=asn1.CONTEXT_FLAG),Query),0),
    ('additionalSearchInfo',None,asn1.TYPE(asn1.IMPLICIT(203,cls=asn1.CONTEXT_FLAG),OtherInformation),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'SearchRequest')
APDU=asn1.CHOICE ([('initRequest',None,asn1.TYPE(asn1.IMPLICIT(20,cls=asn1.CONTEXT_FLAG),InitializeRequest)),
    ('initResponse',None,asn1.TYPE(asn1.IMPLICIT(21,cls=asn1.CONTEXT_FLAG),InitializeResponse)),
    ('searchRequest',None,asn1.TYPE(asn1.IMPLICIT(22,cls=asn1.CONTEXT_FLAG),SearchRequest)),
    ('searchResponse',None,asn1.TYPE(asn1.IMPLICIT(23,cls=asn1.CONTEXT_FLAG),SearchResponse)),
    ('presentRequest',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),PresentRequest)),
    ('presentResponse',None,asn1.TYPE(asn1.IMPLICIT(25,cls=asn1.CONTEXT_FLAG),PresentResponse)),
    ('deleteResultSetRequest',None,asn1.TYPE(asn1.IMPLICIT(26,cls=asn1.CONTEXT_FLAG),DeleteResultSetRequest)),
    ('deleteResultSetResponse',None,asn1.TYPE(asn1.IMPLICIT(27,cls=asn1.CONTEXT_FLAG),DeleteResultSetResponse)),
    ('accessControlRequest',None,asn1.TYPE(asn1.IMPLICIT(28,cls=asn1.CONTEXT_FLAG),AccessControlRequest)),
    ('accessControlResponse',None,asn1.TYPE(asn1.IMPLICIT(29,cls=asn1.CONTEXT_FLAG),AccessControlResponse)),
    ('resourceControlRequest',None,asn1.TYPE(asn1.IMPLICIT(30,cls=asn1.CONTEXT_FLAG),ResourceControlRequest)),
    ('resourceControlResponse',None,asn1.TYPE(asn1.IMPLICIT(31,cls=asn1.CONTEXT_FLAG),ResourceControlResponse)),
    ('triggerResourceControlRequest',None,asn1.TYPE(asn1.IMPLICIT(32,cls=asn1.CONTEXT_FLAG),TriggerResourceControlRequest)),
    ('resourceReportRequest',None,asn1.TYPE(asn1.IMPLICIT(33,cls=asn1.CONTEXT_FLAG),ResourceReportRequest)),
    ('resourceReportResponse',None,asn1.TYPE(asn1.IMPLICIT(34,cls=asn1.CONTEXT_FLAG),ResourceReportResponse)),
    ('scanRequest',None,asn1.TYPE(asn1.IMPLICIT(35,cls=asn1.CONTEXT_FLAG),ScanRequest)),
    ('scanResponse',None,asn1.TYPE(asn1.IMPLICIT(36,cls=asn1.CONTEXT_FLAG),ScanResponse)),
    ('sortRequest',None,asn1.TYPE(asn1.IMPLICIT(43,cls=asn1.CONTEXT_FLAG),SortRequest)),
    ('sortResponse',None,asn1.TYPE(asn1.IMPLICIT(44,cls=asn1.CONTEXT_FLAG),SortResponse)),
    ('segmentRequest',None,asn1.TYPE(asn1.IMPLICIT(45,cls=asn1.CONTEXT_FLAG),Segment)),
    ('extendedServicesRequest',None,asn1.TYPE(asn1.IMPLICIT(46,cls=asn1.CONTEXT_FLAG),ExtendedServicesRequest)),
    ('extendedServicesResponse',None,asn1.TYPE(asn1.IMPLICIT(47,cls=asn1.CONTEXT_FLAG),ExtendedServicesResponse)),
    ('close',None,asn1.TYPE(asn1.IMPLICIT(48,cls=asn1.CONTEXT_FLAG),Close)),
    ('duplicateDetectionRequest',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),ExtendedServicesRequest)),
    ('duplicateDetectionResponse',None,asn1.TYPE(asn1.IMPLICIT(50,cls=asn1.CONTEXT_FLAG),DuplicateDetectionResponse))])
RPNStructure['rpnRpnOp'] =  ('rpnRpnOp', 1, RpnRpnOp)


#module GeneralDiagnosticContainer None
DiagnosticContainer=asn1.SEQUENCE_OF (DiagRec)


#module Explain None
PrimitiveDataType=asn1.INTEGER_class ([('octetString',0),('numeric',1),('date',2),('external',3),('string',4),('trueOrFalse',5),('oid',6),('intUnit',7),('empty',8),('noneOfTheAbove',100)],None,None)
NetworkAddress=asn1.CHOICE ([('internetAddress',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('hostAddress',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('port',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('depricated',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('depricated0',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('depricated1',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('depricated2',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('depricated3',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),0)], seq_name = None))),
    ('other',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('type',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('address',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0)], seq_name = None)))])
AttributeOccurrence=asn1.SEQUENCE ([('attributeSet',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),AttributeSetId),1),
    ('attributeType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('mustBeSupplied',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL),1),
    ('attributeValues',None,    asn1.CHOICE ([('any_or_none',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('specific',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (StringOrNumeric)))]),0)], seq_name = 'AttributeOccurrence')
ValueDescription=asn1.CHOICE ([('integer',None,asn1.INTEGER_class ([],None,None)),
    ('string',None,InternationalString),
    ('octets',None,asn1.OCTSTRING),
    ('oid',None,asn1.OBJECT_IDENTIFIER),
    ('unit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Unit)),
    ('valueAndUnit',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),IntUnit))])
Path=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('tagType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('tagValue',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0)], seq_name = None))
IconObject=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('bodyType',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('ianaType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('z3950type',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('otherType',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString))])),0),
    ('content',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),0)], seq_name = None))
LanguageCode=InternationalString
HumanString=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('language',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),LanguageCode),1),
    ('text',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0)], seq_name = None))
RecordTag=asn1.SEQUENCE ([('qualifier',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),StringOrNumeric),1),
    ('tagValue',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0)], seq_name = 'RecordTag')
AttributeCombination=asn1.SEQUENCE_OF (AttributeOccurrence)
AttributeDescription=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('attributeValue',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
    ('equivalentAttributes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (StringOrNumeric)),1)], seq_name = 'AttributeDescription')
DatabaseList=asn1.SEQUENCE_OF (DatabaseName)
AccessRestrictions=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('accessType',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('any',0),('search',1),('present',2),('specific_elements',3),('extended_services',4),('by_database',5)],None,None)),0),
    ('accessText',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('accessChallenges',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1)], seq_name = None))
SearchKey=asn1.SEQUENCE ([('searchKey',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = 'SearchKey')
ElementDataType=asn1.CHOICE ([('primitive',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),PrimitiveDataType)),
    ('structured',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
AttributeValue=asn1.SEQUENCE ([('value',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('subAttributes',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (StringOrNumeric)),1),
    ('superAttributes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (StringOrNumeric)),1),
    ('partialSupport',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL),1)], seq_name = 'AttributeValue')
ValueRange=asn1.SEQUENCE ([('lower',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ValueDescription),1),
    ('upper',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ValueDescription),1)], seq_name = 'ValueRange')
CommonInfo=asn1.SEQUENCE ([('dateAdded',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('dateChanged',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('expiry',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('humanString_Language',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LanguageCode),1),
    ('otherInfo',None,OtherInformation,1)], seq_name = 'CommonInfo')
ElementInfo=asn1.SEQUENCE ([('elementName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('elementTagPath',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Path),0),
    ('dataType',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),ElementDataType),1),
    ('required',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('repeatable',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = 'ElementInfo')
ExtendedServicesInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('privateType',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('restrictionsApply',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('feeApply',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('available',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('retentionSupported',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('waitAction',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('waitSupported',1),('waitAlways',2),('waitNotSupported',3),('depends',4),('notSaying',5)],None,None)),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('specificExplain',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('esASN',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'ExtendedServicesInfo')
RecordSyntaxInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('recordSyntax',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('transferSyntaxes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('asn1Module',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('abstractStructure',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (ElementInfo)),1)], seq_name = 'RecordSyntaxInfo')
PrivateCapabilities=asn1.SEQUENCE ([('operators',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('operator',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = None))),1),
    ('searchKeys',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SearchKey)),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (HumanString)),1)], seq_name = 'PrivateCapabilities')
Units=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('unit',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0)], seq_name = 'Units')
Charge=asn1.SEQUENCE ([('cost',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),IntUnit),0),
    ('perWhat',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Unit),1),
    ('text',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = 'Charge')
ProcessingInformation=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('processingContext',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('access',0),('search',1),('retrieval',2),('record_presentation',3),('record_handling',4)],None,None)),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('oid',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('instructions',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1)], seq_name = 'ProcessingInformation')
ValueSet=asn1.CHOICE ([('range',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ValueRange)),
    ('enumerated',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (ValueDescription)))])
CategoryInfo=asn1.SEQUENCE ([('category',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('originalCategory',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('asn1Module',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'CategoryInfo')
UnitType=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('unitType',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
    ('units',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Units)),0)], seq_name = 'UnitType')
ProximitySupport=asn1.SEQUENCE ([('anySupport',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('unitsSupported',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.CHOICE ([('known',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('private',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('unit',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
            ('description',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = None)))]))),1)], seq_name = 'ProximitySupport')
AttributeType=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('attributeType',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('attributeValues',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeDescription)),0)], seq_name = 'AttributeType')
VariantValue=asn1.SEQUENCE ([('dataType',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),PrimitiveDataType),0),
    ('values',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ValueSet),1)], seq_name = 'VariantValue')
ContactInfo=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('address',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('email',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('phone',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'ContactInfo')
TagSetInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('tagSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('elements',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('elementname',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('nicknames',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InternationalString)),1),
        ('elementTag',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
        ('description',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),HumanString),1),
        ('dataType',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),PrimitiveDataType),1),
        ('otherTagInfo',None,OtherInformation,1)], seq_name = None))),1)], seq_name = 'TagSetInfo')
SchemaInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('schema',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('tagTypeMapping',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('tagType',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('tagSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
        ('defaultTagType',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL),1)], seq_name = None))),1),
    ('recordStructure',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (ElementInfo)),1)], seq_name = 'SchemaInfo')
AttributeCombinations=asn1.SEQUENCE ([('defaultAttributeSet',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),AttributeSetId),0),
    ('legalCombinations',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeCombination)),0)], seq_name = 'AttributeCombinations')
Iso8777Capabilities=asn1.SEQUENCE ([('searchKeys',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SearchKey)),0),
    ('restrictions',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = 'Iso8777Capabilities')
OmittedAttributeInterpretation=asn1.SEQUENCE ([('defaultValue',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),StringOrNumeric),1),
    ('defaultDescription',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = 'OmittedAttributeInterpretation')
VariantType=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('variantType',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('variantValue',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),VariantValue),1)], seq_name = 'VariantType')
AttributeTypeDetails=asn1.SEQUENCE ([('attributeType',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('defaultIfOmitted',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),OmittedAttributeInterpretation),1),
    ('attributeValues',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeValue)),1)], seq_name = 'AttributeTypeDetails')
Costs=asn1.SEQUENCE ([('connectCharge',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),Charge),1),
    ('connectTime',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Charge),1),
    ('displayCharge',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Charge),1),
    ('searchCharge',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),Charge),1),
    ('subscriptCharge',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),Charge),1),
    ('otherCharges',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('forWhat',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),0),
        ('charge',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Charge),0)], seq_name = None))),1)], seq_name = 'Costs')
AttributeSetInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('attributeSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),AttributeSetId),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('attributes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeType)),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),HumanString),1)], seq_name = 'AttributeSetInfo')
TermListInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('termLists',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('title',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HumanString),1),
        ('searchCost',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('optimized',0),('normal',1),('expensive',2),('filter',3)],None,None)),1),
        ('scanable',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
        ('broader',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InternationalString)),1),
        ('narrower',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InternationalString)),1)], seq_name = None))),0)], seq_name = 'TermListInfo')
CategoryList=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('categories',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (CategoryInfo)),0)], seq_name = 'CategoryList')
RpnCapabilities=asn1.SEQUENCE ([('operators',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.INTEGER_class ([('and',0),('or',1),('and_not',2),('prox',3)],None,None))),1),
    ('resultSetAsOperandSupported',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('restrictionOperandSupported',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('proximity',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),ProximitySupport),1)], seq_name = 'RpnCapabilities')
VariantClass=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('variantClass',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('variantTypes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (VariantType)),0)], seq_name = 'VariantClass')
PerElementDetails=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('recordTag',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),RecordTag),1),
    ('schemaTags',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Path)),1),
    ('maxSize',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('minSize',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('avgSize',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('fixedSize',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('repeatable',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('required',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('contents',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('billingInfo',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('restrictions',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('alternateNames',None,asn1.TYPE(asn1.IMPLICIT(16,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('genericNames',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('searchAccess',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),AttributeCombinations),1)], seq_name = 'PerElementDetails')
VariantSetInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('variantSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('variants',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (VariantClass)),1)], seq_name = 'VariantSetInfo')
AttributeSetDetails=asn1.SEQUENCE ([('attributeSet',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),AttributeSetId),0),
    ('attributesByType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeTypeDetails)),0)], seq_name = 'AttributeSetDetails')
ElementSetDetails=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('elementSetName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),ElementSetName),0),
    ('recordSyntax',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('schema',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('detailsPerElement',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (PerElementDetails)),1)], seq_name = 'ElementSetDetails')
UnitInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('unitSystem',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('units',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (UnitType)),1)], seq_name = 'UnitInfo')
QueryTypeDetails=asn1.CHOICE ([('private',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),PrivateCapabilities)),
    ('rpn',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),RpnCapabilities)),
    ('iso8777',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso8777Capabilities)),
    ('z39_58',None,asn1.TYPE(asn1.IMPLICIT(100,cls=asn1.CONTEXT_FLAG),HumanString)),
    ('erpn',None,asn1.TYPE(asn1.IMPLICIT(101,cls=asn1.CONTEXT_FLAG),RpnCapabilities)),
    ('rankedList',None,asn1.TYPE(asn1.IMPLICIT(102,cls=asn1.CONTEXT_FLAG),HumanString))])
TermListDetails=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('termListName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('attributes',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),AttributeCombinations),1),
    ('scanInfo',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('maxStepSize',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
        ('collatingSequence',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),1),
        ('increasing',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = None)),1),
    ('estNumberTerms',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('sampleTerms',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Term)),1)], seq_name = 'TermListDetails')
SortKeyDetails=asn1.SEQUENCE ([('description',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('elementSpecifications',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Specification)),1),
    ('attributeSpecifications',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),AttributeCombinations),1),
    ('sortType',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('character',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('numeric',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('structured',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HumanString))])),1),
    ('caseSensitivity',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('always',0),('never',1),('default_yes',2),('default_no',3)],None,None)),1)], seq_name = 'SortKeyDetails')
AccessInfo=asn1.SEQUENCE ([('queryTypesSupported',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (QueryTypeDetails)),1),
    ('diagnosticsSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1),
    ('attributeSetIds',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeSetId)),1),
    ('schemas',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1),
    ('recordSyntaxes',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1),
    ('resourceChallenges',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1),
    ('restrictedAccess',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),AccessRestrictions),1),
    ('costInfo',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),Costs),1),
    ('variantSets',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER)),1),
    ('elementSetNames',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (ElementSetName)),1),
    ('unitSystems',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1)], seq_name = 'AccessInfo')
TargetInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('recent_news',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('icon',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),IconObject),1),
    ('namedResultSets',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('multipleDBsearch',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('maxResultSets',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxResultSize',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxTerms',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('timeoutInterval',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('welcomeMessage',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('contactInfo',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),ContactInfo),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('nicknames',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('usage_restrictions',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('paymentAddr',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('hours',None,asn1.TYPE(asn1.IMPLICIT(16,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('dbCombinations',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DatabaseList)),1),
    ('addresses',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (NetworkAddress)),1),
    ('languages',None,asn1.TYPE(asn1.IMPLICIT(101,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('characterSets',None,asn1.TYPE(asn1.IMPLICIT(102,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('commonAccessInfo',None,asn1.TYPE(asn1.IMPLICIT(19,cls=asn1.CONTEXT_FLAG),AccessInfo),1)], seq_name = 'TargetInfo')
AttributeDetails=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('attributesBySet',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (AttributeSetDetails)),1),
    ('attributeCombinations',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),AttributeCombinations),1)], seq_name = 'AttributeDetails')
SortDetails=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('sortKeys',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SortKeyDetails)),1)], seq_name = 'SortDetails')
RetrievalRecordDetails=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('schema',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('recordSyntax',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('detailsPerElement',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (PerElementDetails)),1)], seq_name = 'RetrievalRecordDetails')
DatabaseInfo=asn1.SEQUENCE ([('commonInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),CommonInfo),1),
    ('name',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseName),0),
    ('explainDatabase',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL),1),
    ('nicknames',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DatabaseName)),1),
    ('icon',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),IconObject),1),
    ('user_fee',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('available',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('titleString',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('keywords',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (HumanString)),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('associatedDbs',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),DatabaseList),1),
    ('subDbs',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),DatabaseList),1),
    ('disclaimers',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('news',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('recordCount',None,asn1.TYPE(asn1.EXPLICIT(14,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('actualNumber',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('approxNumber',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)))])),1),
    ('defaultOrder',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('avRecordSize',None,asn1.TYPE(asn1.IMPLICIT(16,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxRecordSize',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('hours',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('bestTime',None,asn1.TYPE(asn1.IMPLICIT(19,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('lastUpdate',None,asn1.TYPE(asn1.IMPLICIT(20,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('updateInterval',None,asn1.TYPE(asn1.IMPLICIT(21,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('coverage',None,asn1.TYPE(asn1.IMPLICIT(22,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('proprietary',None,asn1.TYPE(asn1.IMPLICIT(23,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('copyrightText',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('copyrightNotice',None,asn1.TYPE(asn1.IMPLICIT(25,cls=asn1.CONTEXT_FLAG),HumanString),1),
    ('producerContactInfo',None,asn1.TYPE(asn1.IMPLICIT(26,cls=asn1.CONTEXT_FLAG),ContactInfo),1),
    ('supplierContactInfo',None,asn1.TYPE(asn1.IMPLICIT(27,cls=asn1.CONTEXT_FLAG),ContactInfo),1),
    ('submissionContactInfo',None,asn1.TYPE(asn1.IMPLICIT(28,cls=asn1.CONTEXT_FLAG),ContactInfo),1),
    ('accessInfo',None,asn1.TYPE(asn1.IMPLICIT(29,cls=asn1.CONTEXT_FLAG),AccessInfo),1)], seq_name = 'DatabaseInfo')
Explain_Record=asn1.CHOICE ([('targetInfo',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),TargetInfo)),
    ('databaseInfo',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DatabaseInfo)),
    ('schemaInfo',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),SchemaInfo)),
    ('tagSetInfo',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),TagSetInfo)),
    ('recordSyntaxInfo',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),RecordSyntaxInfo)),
    ('attributeSetInfo',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),AttributeSetInfo)),
    ('termListInfo',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),TermListInfo)),
    ('extendedServicesInfo',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),ExtendedServicesInfo)),
    ('attributeDetails',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),AttributeDetails)),
    ('termListDetails',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),TermListDetails)),
    ('elementSetDetails',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),ElementSetDetails)),
    ('retrievalRecordDetails',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),RetrievalRecordDetails)),
    ('sortDetails',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),SortDetails)),
    ('processing',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),ProcessingInformation)),
    ('variants',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),VariantSetInfo)),
    ('units',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),UnitInfo)),
    ('categoryList',None,asn1.TYPE(asn1.IMPLICIT(100,cls=asn1.CONTEXT_FLAG),CategoryList))])
ElementDataType['structured'] = ('structured', 1, asn1.SEQUENCE_OF(ElementInfo))


#module RecordSyntax_SUTRS None
SutrsRecord=InternationalString


#module RecordSyntax_generic None
Usage=asn1.SEQUENCE ([('type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('redistributable',1),('restricted',2),('licensePointer',3)],None,None)),0),
    ('restriction',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'Usage')
TagPath=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('tagType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('tagValue',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
    ('tagOccurrence',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = None))
ElementData=asn1.CHOICE ([('octets',None,asn1.OCTSTRING),
    ('numeric',None,asn1.INTEGER_class ([],None,None)),
    ('date',None,asn1.GeneralizedTime),
    ('ext',None,asn1.EXTERNAL),
    ('string',None,InternationalString),
    ('trueOrFalse',None,asn1.BOOLEAN),
    ('oid',None,asn1.OBJECT_IDENTIFIER),
    ('intUnit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),IntUnit)),
    ('elementNotThere',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('elementEmpty',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('noDataRequested',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('diagnostic',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('subtree',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.NULL)))])
Variant=asn1.SEQUENCE ([('globalVariantSetId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('triples',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('variantSetId',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
        ('class',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('type',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('value',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),        asn1.CHOICE ([('int',None,asn1.INTEGER_class ([],None,None)),
            ('str',None,InternationalString),
            ('oct',None,asn1.OCTSTRING),
            ('oid',None,asn1.OBJECT_IDENTIFIER),
            ('bool',None,asn1.BOOLEAN),
            ('nul',None,asn1.NULL),
            ('unit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Unit)),
            ('valueAndUnit',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),IntUnit))])),0)], seq_name = None))),0)], seq_name = 'Variant')
Order=asn1.SEQUENCE ([('ascending',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('order',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = 'Order')
HitVector=asn1.SEQUENCE ([('satisfier',None,Term,1),
    ('offsetIntoElement',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('length',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('hitRank',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('serverToken',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1)], seq_name = 'HitVector')
ElementMetaData=asn1.SEQUENCE ([('seriesOrder',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Order),1),
    ('usageRight',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Usage),1),
    ('hits',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (HitVector)),1),
    ('displayName',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('supportedVariants',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Variant)),1),
    ('message',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('elementDescriptor',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1),
    ('surrogateFor',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),TagPath),1),
    ('surrogateElement',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),TagPath),1),
    ('other',None,asn1.TYPE(asn1.IMPLICIT(99,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1)], seq_name = 'ElementMetaData')
TaggedElement=asn1.SEQUENCE ([('tagType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('tagValue',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
    ('tagOccurrence',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('content',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),ElementData),0),
    ('metaData',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),ElementMetaData),1),
    ('appliedVariant',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),Variant),1)], seq_name = 'TaggedElement')
GenericRecord=asn1.SEQUENCE_OF (TaggedElement)
ElementData['subtree'] = ('subtree', asn1.EXPLICIT(6), asn1.SEQUENCE_OF(TaggedElement))


#module RecordSyntax_ESTaskPackage None
TaskPackage=asn1.SEQUENCE ([('packageType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('packageName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('userId',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('retentionTime',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('permissions',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),Permissions),1),
    ('description',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('serverReference',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1),
    ('creationDateTime',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('taskStatus',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('pending',0),('active',1),('complete',2),('aborted',3)],None,None)),0),
    ('packageDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1),
    ('taskSpecificParameters',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),0)], seq_name = 'TaskPackage')


#module ResourceReport_Format_Resource_2 None
Estimate=asn1.SEQUENCE ([('type',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
    ('value',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),IntUnit),0)], seq_name = 'Estimate')
ResourceReport_2=asn1.SEQUENCE ([('estimates',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Estimate)),1),
    ('message',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'ResourceReport_2')


#module AccessControlFormat_prompt_1 None
PromptId=asn1.CHOICE ([('enummeratedPrompt',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('groupId',0),('userId',1),('password',2),('newPassword',3),('copyright',4),('sessionId',5)],None,None)),0),
        ('suggestedString',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None))),
    ('nonEnumeratedPrompt',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString))])
Encryption=asn1.SEQUENCE ([('cryptType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1),
    ('credential',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1),
    ('data',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),0)], seq_name = 'Encryption')
Challenge=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('promptId',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),PromptId),0),
    ('defaultResponse',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('promptInfo',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('character',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('encrypted',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Encryption))])),1),
    ('regExpr',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('responseRequired',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.NULL),1),
    ('allowedValues',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('shouldSave',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.NULL),1),
    ('dataType',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('integer',1),('date',2),('float',3),('alphaNumeric',4),('url_urn',5),('boolean',6)],None,None)),1),
    ('diagnostic',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1)], seq_name = None))
Response=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('promptId',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),PromptId),0),
    ('promptResponse',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('string',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('accept',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN)),
        ('acknowledge',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('diagnostic',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),DiagRec)),
        ('encrypted',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),Encryption))])),0)], seq_name = None))
PromptObject=asn1.CHOICE ([('challenge',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Challenge)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Response))])


#module AccessControlFormat_des_1 None
DRNType=asn1.SEQUENCE ([('userId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1),
    ('salt',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),1),
    ('randomNumber',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),0)], seq_name = 'DRNType')
DES_RN_Object=asn1.CHOICE ([('challenge',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),DRNType)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),DRNType))])


#module AccessControlFormat_krb_1 None
KRBRequest=asn1.SEQUENCE ([('service',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('instance',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('realm',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'KRBRequest')
KRBResponse=asn1.SEQUENCE ([('userid',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('ticket',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),0)], seq_name = 'KRBResponse')
KRBObject=asn1.CHOICE ([('challenge',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),KRBRequest)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),KRBResponse))])


#module ESFormat_PersistentResultSet None
ClientPartNotToKeep_prs=asn1.SEQUENCE ([('clientSuppliedResultSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('replaceOrAppend',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('replace',1),('append',2)],None,None)),1)], seq_name = 'ClientPartNotToKeep_prs')
ServerPart_prs=asn1.SEQUENCE ([('serverSuppliedResultSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('numberOfRecords',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'ServerPart_prs')
PersistentResultSet=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL),0),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ClientPartNotToKeep_prs),1)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL),0),
        ('serverPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ServerPart_prs),1)], seq_name = None)))])


#module ESFormat_PersistentQuery None
ClientPartToKeep_pq=asn1.SEQUENCE ([('dbNames',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('additionalSearchInfo',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),OtherInformation),1)], seq_name = 'ClientPartToKeep_pq')
ServerPart_pq=Query
ClientPartNotToKeep_pq=asn1.CHOICE ([('package',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('query',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Query))])
PersistentQuery=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_pq),1),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ClientPartNotToKeep_pq),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_pq),1),
        ('serverPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ServerPart_pq),0)], seq_name = None)))])


#module ESFormat_ExportSpecification None
Destination=asn1.CHOICE ([('phoneNumber',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('faxNumber',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('x400address',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('emailAddress',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('pagerNumber',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('ftpAddress',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('ftamAddress',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('printerAddress',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),InternationalString)),
    ('other',None,asn1.TYPE(asn1.IMPLICIT(100,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('vehicle',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('destination',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0)], seq_name = None)))])
ClientPartToKeep_es=asn1.SEQUENCE ([('composition',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),CompSpec),0),
    ('exportDestination',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Destination),0)], seq_name = 'ClientPartToKeep_es')
ExportSpecification=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_es),0),
        ('notToKeep',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_es),0),
        ('serverPart',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL),0)], seq_name = None)))])


#module ESFormat_PeriodicQuerySchedule None
Period=asn1.CHOICE ([('unit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),IntUnit)),
    ('businessDaily',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('continuous',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('other',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString))])
ClientPartToKeep_pqs=asn1.SEQUENCE ([('activeFlag',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('databaseNames',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('resultSetDisposition',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('replace',1),('append',2),('createNew',3)],None,None)),1),
    ('alertDestination',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),Destination),1),
    ('exportParameters',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('packageName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('exportPackage',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ExportSpecification))])),1)], seq_name = 'ClientPartToKeep_pqs')
ServerPart_pqs=asn1.SEQUENCE ([('databaseNames',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('actualQuery',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Query),0),
    ('serverStatedPeriod',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Period),0),
    ('expiration',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('resultSetPackage',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('lastQueryTime',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('lastResultNumber',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('numberSinceModify',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('additionalSearchInfo',None,asn1.TYPE(asn1.EXPLICIT(8,cls=asn1.CONTEXT_FLAG),OtherInformation),1)], seq_name = 'ServerPart_pqs')
ClientPartNotToKeep_pqs=asn1.SEQUENCE ([('databaseNames',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('querySpec',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('actualQuery',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Query)),
        ('packageName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString))])),1),
    ('clientSuggestedPeriod',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Period),1),
    ('expiration',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime),1),
    ('resultSetPackage',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('additionalSearchInfo',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),OtherInformation),1)], seq_name = 'ClientPartNotToKeep_pqs')
PeriodicQuerySchedule=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_pqs),0),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ClientPartNotToKeep_pqs),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_pqs),0),
        ('serverPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ServerPart_pqs),0)], seq_name = None)))])


#module ESFormat_ItemOrder None
ClientPartNotToKeep_io=asn1.SEQUENCE ([('resultSetItem',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('resultSetId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('item',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None)),1),
    ('itemRequest',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1)], seq_name = 'ClientPartNotToKeep_io')
ServerPart_io=asn1.SEQUENCE ([('itemRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('statusOrErrorReport',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('auxiliaryStatus',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('notReceived',1),('loanQueue',2),('forwarded',3),('unfilledCopyright',4),('filledCopyright',5)],None,None)),1)], seq_name = 'ServerPart_io')
CreditCardInfo=asn1.SEQUENCE ([('nameOnCard',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('expirationDate',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('cardNumber',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),0)], seq_name = 'CreditCardInfo')
ClientPartToKeep_io=asn1.SEQUENCE ([('supplDescription',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('contact',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('phone',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('email',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None)),1),
    ('addlBilling',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('paymentMethod',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.CHOICE ([('billInvoice',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
            ('prepay',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
            ('depositAccount',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
            ('creditCard',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),CreditCardInfo)),
            ('cardInfoPreviouslySupplied',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
            ('privateKnown',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
            ('privateNotKnown',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))])),0),
        ('customerReference',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('customerPONumber',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None)),1)], seq_name = 'ClientPartToKeep_io')
ItemOrder=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_io),1),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ClientPartNotToKeep_io),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_io),1),
        ('serverPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ServerPart_io),0)], seq_name = None)))])


#module ESFormat_Update None
ClientPartToKeep_upd=asn1.SEQUENCE ([('action',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('recordInsert',1),('recordReplace',2),('recordDelete',3),('elementUpdate',4)],None,None)),0),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('schema',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('elementSetName',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'ClientPartToKeep_upd')
CorrelationInfo=asn1.SEQUENCE ([('note',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('id',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'CorrelationInfo')
SuppliedRecords=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('recordId',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('number',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('string',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('opaque',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING))])),1),
    ('supplementalId',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('timeStamp',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime)),
        ('versionNumber',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('previousVersion',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))])),1),
    ('correlationInfo',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),CorrelationInfo),1),
    ('record',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),0)], seq_name = None))
ClientPartNotToKeep_upd=SuppliedRecords
TaskPackageRecordStructure=asn1.SEQUENCE ([('recordOrSurDiag',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('record',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
        ('diagnostic',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),DiagRec))])),1),
    ('correlationInfo',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),CorrelationInfo),1),
    ('recordStatus',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',1),('queued',2),('inProcess',3),('failure',4)],None,None)),0)], seq_name = 'TaskPackageRecordStructure')
ServerPart_upd=asn1.SEQUENCE ([('updateStatus',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',1),('partial',2),('failure',3)],None,None)),0),
    ('globalDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1),
    ('taskPackageRecords',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (TaskPackageRecordStructure)),0)], seq_name = 'ServerPart_upd')
Update=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_upd),0),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ClientPartNotToKeep_upd),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_upd),0),
        ('serverPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ServerPart_upd),0)], seq_name = None)))])


#module ESFormat_ExportInvocation None
ClientPartToKeep_ei=asn1.SEQUENCE ([('exportSpec',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('packageName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('packageSpec',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ExportSpecification))])),0),
    ('numberOfCopies',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = 'ClientPartToKeep_ei')
ClientPartNotToKeep_ei=asn1.SEQUENCE ([('resultSetId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('records',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('all',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('ranges',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (        asn1.SEQUENCE ([('start',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
            ('count',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = None))))])),0)], seq_name = 'ClientPartNotToKeep_ei')
ServerPart_ei=asn1.SEQUENCE ([('estimatedQuantity',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('quantitySoFar',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('estimatedCost',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('costSoFar',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),IntUnit),1)], seq_name = 'ServerPart_ei')
ExportInvocation=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_ei),0),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ClientPartNotToKeep_ei),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('clientPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ClientPartToKeep_ei),0),
        ('serverPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ServerPart_ei),1)], seq_name = None)))])


#module UserInfoFormat_searchResult_1 None
ResultsByDB=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('databases',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('all',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('list',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (DatabaseName)))])),0),
    ('count',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('resultSetName',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None))
QueryExpression=asn1.CHOICE ([('term',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('queryTerm',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Term),0),
        ('termComment',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None))),
    ('query',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Query))])
SearchInfoReport=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('subqueryId',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('fullQuery',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('subqueryExpression',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),QueryExpression),1),
    ('subqueryInterpretation',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),QueryExpression),1),
    ('subqueryRecommendation',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),QueryExpression),1),
    ('subqueryCount',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('subqueryWeight',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),IntUnit),1),
    ('resultsByDB',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),ResultsByDB),1)], seq_name = None))


#module UserInfoFormat_userInfo_1 None
UserInfo_1=OtherInformation


#module ESpec_2 None
Occurrences=asn1.CHOICE ([('all',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('last',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('values',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('start',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('howMany',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = None)))])
Espec_2_TagPath=asn1.SEQUENCE_OF (asn1.CHOICE ([('specificTag',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('schemaId',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
        ('tagType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
        ('tagValue',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),StringOrNumeric),0),
        ('occurrence',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),Occurrences),1)], seq_name = None))),
    ('wildThing',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Occurrences)),
    ('wildPath',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL))]))
SimpleElement=asn1.SEQUENCE ([('path',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Espec_2_TagPath),0),
    ('variantRequest',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Variant),1)], seq_name = 'SimpleElement')
ElementRequest=asn1.CHOICE ([('simpleElement',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SimpleElement)),
    ('compositeElement',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('elementList',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.CHOICE ([('primitives',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),            asn1.SEQUENCE_OF (InternationalString))),
            ('specs',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),            asn1.SEQUENCE_OF (SimpleElement)))])),0),
        ('deliveryTag',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Espec_2_TagPath),0),
        ('variantRequest',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),Variant),1)], seq_name = None)))])
Espec_2=asn1.SEQUENCE ([('elementSetNames',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (InternationalString)),1),
    ('defaultVariantSetId',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('defaultVariantRequest',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),Variant),1),
    ('defaultTagType',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('elements',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (ElementRequest)),1)], seq_name = 'Espec_2')


#module ESpec_q None
Espec_q_RPNStructure=asn1.CHOICE ([('op',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),AttributesPlusTerm)),
    ('rpnRpnOp',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
Espec_q_RpnRpnOp=asn1.SEQUENCE ([('rpn1',None,Espec_q_RPNStructure,0),
    ('rpn2',None,Espec_q_RPNStructure,0),
    ('op',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('and',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('or',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('and_not',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),0)], seq_name = 'Espec_q_RpnRpnOp')
Espec_q_AttributesPlusTerm=asn1.TYPE(asn1.IMPLICIT(102,cls=asn1.CONTEXT_FLAG),asn1.SEQUENCE ([('attributes',None,AttributeList,0),
    ('term',None,Term,0)], seq_name = 'Espec_q_AttributesPlusTerm'))
ValueRestrictor=asn1.SEQUENCE ([('attributeSetId',None,asn1.OBJECT_IDENTIFIER,0),
    ('nodeSelectionCriteria',None,Espec_q_RPNStructure,0)], seq_name = 'ValueRestrictor')
Espec_q=asn1.SEQUENCE ([('valueRestrictor',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ValueRestrictor),0),
    ('elementSelector',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1)], seq_name = 'Espec_q')
Espec_q_RPNStructure['rpnRpnOp'] =  ('rpnRpnOp', 1, Espec_q_RpnRpnOp)


#!/usr/bin/env python
# Auto-generated from auth_file_info.asn at Wed, 02 Jun 2004 15:30:48 +0000
from PyZ3950 import asn1
#module UserInfoFormat_authorityFileInfo None
AuthorityFileInfo=asn1.SEQUENCE ([('name',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),HumanString),0),
    ('database',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('exclusive',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL),1)], seq_name = 'AuthorityFileInfo')


#!/usr/bin/env python
# Auto-generated from charset_1.asn at Wed, 02 Jun 2004 15:30:48 +0000
from PyZ3950 import asn1
#module UserInfoFormat_charSetandLanguageNegotiation_1 None
Environment=asn1.CHOICE ([('sevenBit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('eightBit',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
Iso10646=asn1.SEQUENCE ([('collections',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('encodingLevel',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0)], seq_name = 'Iso10646')
LeftAndRight=asn1.SEQUENCE ([('gLeft',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('g0',0),('g1',1),('g2',2),('g3',3)],None,None)),0),
    ('gRight',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('g1',1),('g2',2),('g3',3)],None,None)),0)], seq_name = 'LeftAndRight')
LanguageCode1=asn1.GeneralString
PrivateCharacterSet=asn1.CHOICE ([('viaOid',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER))),
    ('externallySpecified',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('previouslyAgreedUpon',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
InitialSet=asn1.SEQUENCE ([('g0',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('g1',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('g2',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('g3',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('c0',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('c1',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = 'InitialSet')
Iso2022=asn1.CHOICE ([('originProposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('proposedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment),1),
        ('proposedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),0),
        ('proposedInitialSets',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InitialSet)),0),
        ('proposedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight),0)], seq_name = None))),
    ('targetResponse',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('selectedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment),0),
        ('selectedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),0),
        ('selectedinitialSet',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InitialSet),0),
        ('selectedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight),0)], seq_name = None)))])
OriginProposal=asn1.SEQUENCE ([('proposedCharSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet))]))),1),
    ('proposedlanguages',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (LanguageCode1)),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'OriginProposal')
TargetResponse=asn1.SEQUENCE ([('selectedCharSets',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet)),
        ('none',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),1),
    ('selectedLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),LanguageCode1),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'TargetResponse')
CharSetandLanguageNegotiation=asn1.CHOICE ([('proposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),OriginProposal)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),TargetResponse))])


#!/usr/bin/env python
# Auto-generated from charset_2.asn at Wed, 02 Jun 2004 15:30:48 +0000
from PyZ3950 import asn1
#module NegotiationRecordDefinition_charSetandLanguageNegotiation_2 None
InitialSet_2=asn1.SEQUENCE ([('g0',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('g1',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('g2',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('g3',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('c0',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('c1',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'InitialSet_2')
LanguageCode2=asn1.GeneralString
LeftAndRight_2=asn1.SEQUENCE ([('gLeft',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('g0',0),('g1',1),('g2',2),('g3',3)],None,None)),0),
    ('gRight',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('g1',1),('g2',2),('g3',3)],None,None)),1)], seq_name = 'LeftAndRight_2')
PrivateCharacterSet2=asn1.CHOICE ([('viaOid',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER))),
    ('externallySpecified',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('previouslyAgreedUpon',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
Iso10646_2=asn1.SEQUENCE ([('collections',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
    ('encodingLevel',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0)], seq_name = 'Iso10646_2')
Environment_2=asn1.CHOICE ([('sevenBit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('eightBit',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
Iso2022_2=asn1.CHOICE ([('originProposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('proposedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment_2),1),
        ('proposedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),0),
        ('proposedInitialSets',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InitialSet_2)),0),
        ('proposedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight_2),0)], seq_name = None))),
    ('targetResponse',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('selectedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment_2),0),
        ('selectedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),0),
        ('selectedinitialSet',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InitialSet_2),0),
        ('selectedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight_2),0)], seq_name = None)))])
TargetResponse2=asn1.SEQUENCE ([('selectedCharSets',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022_2)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646_2)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet2)),
        ('none',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),1),
    ('selectedLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),LanguageCode2),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'TargetResponse2')
OriginProposal2=asn1.SEQUENCE ([('proposedCharSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022_2)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646_2)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet2))]))),1),
    ('proposedlanguages',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (LanguageCode2)),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'OriginProposal2')
CharSetandLanguageNegotiation2=asn1.CHOICE ([('proposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),OriginProposal2)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),TargetResponse2))])


#!/usr/bin/env python
# Auto-generated from charset_3.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module NegotiationRecordDefinition_charSetandLanguageNegotiation_3 None
Environment_3=asn1.CHOICE ([('sevenBit',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('eightBit',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
LeftAndRight_3=asn1.SEQUENCE ([('gLeft',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('g0',0),('g1',1),('g2',2),('g3',3)],None,None)),0),
    ('gRight',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('g1',1),('g2',2),('g3',3)],None,None)),1)], seq_name = 'LeftAndRight_3')
InitialSet_3=asn1.SEQUENCE ([('g0',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('g1',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('g2',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('g3',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('c0',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('c1',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'InitialSet_3')
LanguageCode3=asn1.GeneralString
PrivateCharacterSet_3=asn1.CHOICE ([('viaOid',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (asn1.OBJECT_IDENTIFIER))),
    ('externallySpecified',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('previouslyAgreedUpon',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL))])
Iso2022_3=asn1.CHOICE ([('originProposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('proposedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment_3),1),
        ('proposedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),0),
        ('proposedInitialSets',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InitialSet_3)),0),
        ('proposedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight_3),0)], seq_name = None))),
    ('targetResponse',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('selectedEnvironment',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Environment_3),0),
        ('selectedSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER_class ([],None,None))),0),
        ('selectedinitialSet',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InitialSet_3),0),
        ('selectedLeftAndRight',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),LeftAndRight_3),0)], seq_name = None)))])
Iso10646_3=asn1.SEQUENCE ([('collections',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('encodingLevel',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0)], seq_name = 'Iso10646_3')
TargetResponse_3=asn1.SEQUENCE ([('selectedCharSets',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022_3)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646_3)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet_3)),
        ('none',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),1),
    ('selectedLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),LanguageCode3),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'TargetResponse_3')
OriginProposal_3=asn1.SEQUENCE ([('proposedCharSets',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022_3)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646_3)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet_3))]))),1),
    ('proposedlanguages',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (LanguageCode3)),1),
    ('recordsInSelectedCharSets',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'OriginProposal_3')
CharSetandLanguageNegotiation_3=asn1.CHOICE ([('proposal',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),OriginProposal_3)),
    ('response',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),TargetResponse_3))])


#!/usr/bin/env python
# Auto-generated from edit_replace_qual.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module ERAQ None
EditReplaceActionQualifier=asn1.SEQUENCE ([('persistentResultSetPackageName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('numberOfRecords',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
    ('creationDateTime',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),0),
    ('reviewCode',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('reviewNote',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('changeDataInfo',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('fieldIdentifier',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('oldValue',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('oldValueTruncationAttribute',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('conditionalField',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('conditionalValue',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('conditionalTruncationAttribute',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('newValue',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('editReplaceType',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('fieldInsert',0),('fieldDelete',1),('fieldReplace',2),('subfieldInsert',3),('subfieldDelete',4),('subfieldReplace',5),('subfieldMerge',6),('indicatorChange',7),('dataStringChange',8)],None,None)),0),
        ('case',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = None))),0)], seq_name = 'EditReplaceActionQualifier')


#!/usr/bin/env python
# Auto-generated from frag.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module FragmentSyntax None
Fragment=asn1.SEQUENCE ([('realSyntax',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('remainingOctets',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('fragment',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING),0)], seq_name = 'Fragment')


#!/usr/bin/env python
# Auto-generated from ins_qualifier.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module RIAQ None
RecordInsertActionQualifier=asn1.SEQUENCE ([('idsOrCode',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('nonDupRecordIds',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InternationalString))),
        ('recordReviewCode',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString))])),0),
    ('recordReviewNote',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'RecordInsertActionQualifier')


#!/usr/bin/env python
# Auto-generated from multiple_search_term_1.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module UserInfoFormat_multipleSearchTerms_1 None
MultipleSearchTerms_1=asn1.SEQUENCE_OF (Term)


#!/usr/bin/env python
# Auto-generated from multiple_search_term_2.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module UserInfoFormat_multipleSearchTerms_2 None
MultipleSearchTerms_2=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('term',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Term),0),
    ('flag',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = None))


#!/usr/bin/env python
# Auto-generated from negot_es_size.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module NegotiationRecordDefinition_NegotiateEsSizes None
NegotiateEsSizes=asn1.SEQUENCE ([('maxMsgSize',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxTaskPackageSize',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('maxRecordSize',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'NegotiateEsSizes')


#!/usr/bin/env python
# Auto-generated from oclc.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module UserInfoFormat_OCLC_Info None
DBName=asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.VisibleString)
OCLC_UserInformation=asn1.SEQUENCE ([('motd',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.VisibleString),1),
    ('dblist',None,    asn1.SEQUENCE_OF (DBName),1),
    ('failReason',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('text',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.VisibleString),1)], seq_name = 'OCLC_UserInformation')


#!/usr/bin/env python
# Auto-generated from opac.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module RecordSyntax_opac None
Volume=asn1.SEQUENCE ([('enumeration',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('chronology',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('enumAndChron',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'Volume')
CircRecord=asn1.SEQUENCE ([('availableNow',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('availablityDate',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('availableThru',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('restrictions',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('itemId',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('renewable',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('onHold',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('enumAndChron',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('midspine',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('temporaryLocation',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'CircRecord')
HoldingsAndCircData=asn1.SEQUENCE ([('typeOfRecord',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('encodingLevel',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('format',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('receiptAcqStatus',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('generalRetention',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('completeness',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('dateOfReport',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('nucCode',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('localLocation',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('shelvingLocation',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('callNumber',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('shelvingData',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('copyNumber',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('publicNote',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('reproductionNote',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('termsUseRepro',None,asn1.TYPE(asn1.IMPLICIT(16,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('enumAndChron',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('volumes',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Volume)),1),
    ('circulationData',None,asn1.TYPE(asn1.IMPLICIT(19,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (CircRecord)),1)], seq_name = 'HoldingsAndCircData')
HoldingsRecord=asn1.CHOICE ([('marcHoldingsRecord',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
    ('holdingsAndCirc',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),HoldingsAndCircData))])
OPACRecord=asn1.SEQUENCE ([('bibliographicRecord',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('holdingsData',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (HoldingsRecord)),1)], seq_name = 'OPACRecord')


#!/usr/bin/env python
# Auto-generated from update_es_rev1.asn at Wed, 02 Jun 2004 15:30:49 +0000
from PyZ3950 import asn1
#module ESFormat_Update None
CorrelationInfo_updrev1=asn1.SEQUENCE ([('note',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('id',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = 'CorrelationInfo_updrev1')
OriginPartToKeep_updrev1=asn1.SEQUENCE ([('action',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('recordInsert',1),('recordReplace',2),('recordDelete',3),('elementUpdate',4),('specialUpdate',5)],None,None)),0),
    ('databaseName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('schema',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('elementSetName',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('actionQualifier',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1)], seq_name = 'OriginPartToKeep_updrev1')
TargetPart_updrev1=asn1.SEQUENCE ([('updateStatus',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',1),('partial',2),('failure',3)],None,None)),0),
    ('globalDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1),
    ('taskPackageRecords',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (TaskPackageRecordStructure)),0)], seq_name = 'TargetPart_updrev1')
TaskPackageRecordStructure_updrev1=asn1.SEQUENCE ([('recordOrSurDiag',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('record',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL)),
        ('surrogateDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (DiagRec)))])),1),
    ('correlationInfo',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),CorrelationInfo_updrev1),1),
    ('recordStatus',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('success',1),('queued',2),('inProcess',3),('failure',4)],None,None)),0),
    ('supplementalDiagnostics',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (DiagRec)),1)], seq_name = 'TaskPackageRecordStructure_updrev1')
SuppliedRecords_updrev1=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('recordId',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('number',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('string',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('opaque',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING))])),1),
    ('supplementalId',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('timeStamp',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.GeneralizedTime)),
        ('versionNumber',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('previousVersion',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL))])),1),
    ('correlationInfo',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),CorrelationInfo_updrev1),1),
    ('record',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),0)], seq_name = None))
OriginPartNotToKeep_updrev1=SuppliedRecords_updrev1
Update_updrev1=asn1.CHOICE ([('esRequest',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('toKeep',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),OriginPartToKeep_updrev1),0),
        ('notToKeep',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),OriginPartNotToKeep_updrev1),0)], seq_name = None))),
    ('taskPackage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('originPart',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),OriginPartToKeep_updrev1),0),
        ('targetPart',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),TargetPart_updrev1),0)], seq_name = None)))])


#!/usr/bin/env python
# Auto-generated from zsql.asn at Wed, 02 Jun 2004 15:30:50 +0000
from PyZ3950 import asn1
#module Z39_50_EXTERNALS_SQL_RS None
SQLCharacterSetClause=asn1.SEQUENCE ([('characterSetCatalog',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('characterSetSchema',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('characterSetName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'SQLCharacterSetClause')
SQLUniqueConstraint=asn1.INTEGER_class ([('unique',1),('primaryKey',2)],None,None)
SQLTransformDescriptor=asn1.SEQUENCE ([('groupName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('fromSQLFunctionName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('toSQLFunctionName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'SQLTransformDescriptor')
Z3950CharacterSetLanguageClause=asn1.SEQUENCE ([('characterSet',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('iso2022',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Iso2022)),
        ('iso10646',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Iso10646)),
        ('private',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),PrivateCharacterSet)),
        ('none',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),1),
    ('language',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),LanguageCode),1)], seq_name = 'Z3950CharacterSetLanguageClause')
SQLOrderingDescriptor=asn1.SEQUENCE ([('orderingForm',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('equals',1),('full',2),('none',3)],None,None)),0),
    ('orderingCategory',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('relativeRoutineName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('hashRoutineName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('stateRoutineName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString))])),0)], seq_name = 'SQLOrderingDescriptor')
SQLQuery=asn1.SEQUENCE ([('abstractDatabaseFlag',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('queryExpression',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),0)], seq_name = 'SQLQuery')
SQLException=asn1.SEQUENCE ([('sqlState',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('sqlCode',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
    ('sqlErrorText',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'SQLException')
SQLCollationClause=asn1.SEQUENCE ([('collationCatalog',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('collationSchema',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('collationName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = 'SQLCollationClause')
SQLMethodSpecDescriptor=asn1.SEQUENCE ([('routineName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('parameterList',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('parameterName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('mode',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('in',1),('out',2),('inout',3)],None,None)),1),
        ('type',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL),0)], seq_name = None))),0),
    ('languageName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('parameterStyle',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('sql',1),('general',2)],None,None)),1),
    ('returnsDataDescriptor',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.NULL),1),
    ('methodSpecType',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('originalSelfAsResult',1),('originalSelfAsLocator',2),('overriding',3)],None,None)),1),
    ('methodType',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('instance',1),('static',2)],None,None)),1),
    ('deterministic',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('possibleMethodFunction',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('noSQL',1),('containsSQL',2),('readsSQLData',3),('writesSQLData',4)],None,None)),1),
    ('invokableWhenNull',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)], seq_name = 'SQLMethodSpecDescriptor')
SQLAttributeDescriptor=asn1.SEQUENCE ([('attributeName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('dataDescriptor',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL),1),
    ('collation',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),SQLCollationClause),1)], seq_name = 'SQLAttributeDescriptor')
SQLValue=asn1.SEQUENCE ([('dataItem',None,    asn1.CHOICE ([('characterItem',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('numericItem',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('decimalItem',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('integerItem',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('smallIntItem',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None))),
        ('floatItem',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.REAL)),
        ('realItem',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),asn1.REAL)),
        ('doublePrecisionItem',None,asn1.TYPE(asn1.EXPLICIT(8,cls=asn1.CONTEXT_FLAG),asn1.REAL)),
        ('dateTimeItem',None,asn1.TYPE(asn1.EXPLICIT(9,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('intervalItem',None,asn1.TYPE(asn1.EXPLICIT(10,cls=asn1.CONTEXT_FLAG),InternationalString)),
        ('varcharItem',None,asn1.TYPE(asn1.EXPLICIT(12,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('booleanItem',None,asn1.TYPE(asn1.EXPLICIT(13,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN)),
        ('bitItem',None,asn1.TYPE(asn1.EXPLICIT(14,cls=asn1.CONTEXT_FLAG),asn1.BITSTRING_class ([],None,None))),
        ('bitVarItem',None,asn1.TYPE(asn1.EXPLICIT(15,cls=asn1.CONTEXT_FLAG),asn1.BITSTRING_class ([],None,None))),
        ('udtItem',None,asn1.TYPE(asn1.EXPLICIT(17,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.NULL))),
        ('udtLocator',None,asn1.TYPE(asn1.EXPLICIT(18,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('rowItem',None,asn1.TYPE(asn1.EXPLICIT(19,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.NULL))),
        ('refItem',None,asn1.TYPE(asn1.EXPLICIT(20,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('collectionItem',None,asn1.TYPE(asn1.EXPLICIT(21,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.NULL))),
        ('collectionLocator',None,asn1.TYPE(asn1.EXPLICIT(22,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('bLOBItem',None,asn1.TYPE(asn1.EXPLICIT(30,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('bLOBLocator',None,asn1.TYPE(asn1.EXPLICIT(31,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('cLOBItem',None,asn1.TYPE(asn1.EXPLICIT(40,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('cLOBLocator',None,asn1.TYPE(asn1.EXPLICIT(41,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING)),
        ('resultSetItem',None,asn1.TYPE(asn1.EXPLICIT(50,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.NULL))),
        ('resultSetLocator',None,asn1.TYPE(asn1.EXPLICIT(51,cls=asn1.CONTEXT_FLAG),asn1.OCTSTRING))]),1),
    ('indicator',None,asn1.TYPE(asn1.IMPLICIT(50,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('sqlnull',1),('sqlempty',2),('sqldefault',3)],None,None)),1)], seq_name = 'SQLValue')
SQLDataDescriptor=asn1.CHOICE ([('characterType',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('sqlCharacterSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLCharacterSetClause),1),
        ('zCharacterSetLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Z3950CharacterSetLanguageClause),1),
        ('collation',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),SQLCollationClause),1)], seq_name = None))),
    ('numericType',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('precision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('scale',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('decimalType',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('precision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('scale',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('integerType',None,asn1.TYPE(asn1.EXPLICIT(8,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('precision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
        ('precisionBase',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('binary',0),('decimal',1)],None,None)),0)], seq_name = None))),
    ('smallIntType',None,asn1.TYPE(asn1.EXPLICIT(9,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('precision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
        ('precisionBase',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('binary',0),('decimal',1)],None,None)),0)], seq_name = None))),
    ('floatType',None,asn1.TYPE(asn1.EXPLICIT(10,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('mantissaPrecision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('maxExponent',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('realType',None,asn1.TYPE(asn1.EXPLICIT(11,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('mantissaPrecision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('maxExponent',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('doublePrecisionType',None,asn1.TYPE(asn1.EXPLICIT(12,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('mantissaPrecision',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('maxExponent',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('dateTimeType',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('dateTimeQualifier',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('date',1),('time',2),('timeStamp',3),('timeWithTimeZone',4),('timeStampWithTimeZone',5)],None,None)),0),
        ('fractionalSecondsPrecision',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = None))),
    ('intervalType',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('intervalQualifier',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('year',1),('month',2),('day',3),('hour',4),('minute',5),('second',6),('yearToMonth',7),('dayToHour',8),('dayToMinute',9),('dayToSecond',10),('hourToMinute',11),('hourToSecond',12),('minuteToSecond',13)],None,None)),0),
        ('leadingFieldPrecision',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1),
        ('fractionalSecondsPrecision',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),1)], seq_name = None))),
    ('varcharType',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('characterSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLCharacterSetClause),1),
        ('zCharacterSetLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Z3950CharacterSetLanguageClause),1),
        ('collation',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),SQLCollationClause),1)], seq_name = None))),
    ('booleanType',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
    ('bitType',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('bitVarType',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('sQLUserDefinedType',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('udtName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('ordering',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLOrderingDescriptor),1),
        ('superTypeName',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1),
        ('representation',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),        asn1.CHOICE ([('distinct',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
            ('structured',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),            asn1.SEQUENCE_OF (SQLAttributeDescriptor))),
            ('system_generated',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.NULL))])),0),
        ('instantiable',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
        ('final',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
        ('transformDesc',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (SQLTransformDescriptor)),1)], seq_name = None))),
    ('sQLUserDefinedTypeLocatorType',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('sQLRowType',None,asn1.TYPE(asn1.IMPLICIT(19,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('fieldName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('dataType',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL),0)], seq_name = None)))),
    ('sQLReferenceType',None,asn1.TYPE(asn1.EXPLICIT(20,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('scopeTableName',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None))),
    ('sQLCollectionType',None,asn1.TYPE(asn1.EXPLICIT(21,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('dataType',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.NULL),0),
        ('collectionTypeConstructor',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('size',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
            ('type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('array',1),('set',2)],None,None)),0)], seq_name = None)),0),
        ('sQLCollectionLocatorType',None,asn1.TYPE(asn1.IMPLICIT(22,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None)),0),
        ('bLOBType',None,asn1.TYPE(asn1.IMPLICIT(30,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None)),0),
        ('bLOBLocatorType',None,asn1.TYPE(asn1.IMPLICIT(31,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None)),0),
        ('cLOBType',None,asn1.TYPE(asn1.EXPLICIT(40,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
            ('sqlCharacterSet',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLCharacterSetClause),1),
            ('zCharacterSetLanguage',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Z3950CharacterSetLanguageClause),1),
            ('collation',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),SQLCollationClause),1)], seq_name = None)),0)], seq_name = None))),
    ('cLOBLocatorType',None,asn1.TYPE(asn1.IMPLICIT(41,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None))),
    ('sQLResultSetType',None,asn1.TYPE(asn1.IMPLICIT(50,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('resultSetName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
        ('size',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0),
        ('listOfSQLDataDescriptors',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.NULL),0)], seq_name = None)))),
    ('sQLResultSetLocatorType',None,asn1.TYPE(asn1.IMPLICIT(51,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('length',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([],None,None)),0)], seq_name = None)))])
SQLFieldValue=asn1.SEQUENCE ([('sqlException',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),SQLException),1),
    ('resultValue',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLValue),1)], seq_name = 'SQLFieldValue')
SQLRowValue=asn1.SEQUENCE_OF (SQLFieldValue)
SQLDefaultOption=asn1.CHOICE ([('sqlValue',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),SQLValue)),
    ('other',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER_class ([('user',1),('currentuser',2),('sessionuser',3),('systemuser',4),('currentpath',5),('sqlnull',6),('sqlempty',7)],None,None)))])
SQLColumnDescriptor=asn1.SEQUENCE ([('columnName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),0),
    ('dataType',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL),0),
    ('columnConstraint',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('nullable',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
        ('uniqueConstraint',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLUniqueConstraint),1),
        ('check',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None))),0),
    ('sqlDefault',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),SQLDefaultOption),1)], seq_name = 'SQLColumnDescriptor')
SQLTableDescriptor=asn1.SEQUENCE ([('tableName',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),InternationalString),1),
    ('listOfColumnDescriptors',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SQLColumnDescriptor)),0),
    ('tableConstraint',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (    asn1.SEQUENCE ([('listOfColumnNames',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (InternationalString)),0),
        ('uniqueContraint',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),SQLUniqueConstraint),1),
        ('check',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),InternationalString),1)], seq_name = None))),0)], seq_name = 'SQLTableDescriptor')
SQL_Result=asn1.SEQUENCE ([('tableDescriptor',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),SQLTableDescriptor),1),
    ('listOfResultValues',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (SQLRowValue)),1)], seq_name = 'SQL_Result')
SQLColumnDescriptor['dataType'] = ('dataType', asn1.EXPLICIT(1), SQLDataDescriptor)

SQLDataDescriptor['sQLResultSetType'][0]['listOfSQLDataDescriptors'] = ('listOfSQLDataDescriptors', 3, asn1.SEQUENCE_OF (SQLDataDescriptor))

SQLDataDescriptor ['sQLUserDefinedType']['representation']['distinct'] = ('distinct', 0, SQLDataDescriptor)

SQLDataDescriptor['sQLRowType'][0]['dataType'] = ('dataType', asn1.EXPLICIT(1), SQLDataDescriptor)

SQLAttributeDescriptor['dataDescriptor'] = ('dataDescriptor', 1, SQLDataDescriptor)

SQLValue['dataItem']['udtItem'] = ('udtItem', 17, asn1.SEQUENCE_OF(SQLValue))

SQLValue['dataItem']['rowItem'] = ('rowItem', 19, asn1.SEQUENCE_OF(SQLValue))

SQLValue['dataItem']['collectionItem'] = ('udtItem', 21, asn1.SEQUENCE_OF(SQLValue))

SQLValue['dataItem']['resultSetItem'] = ('udtItem', 50, asn1.SEQUENCE_OF(SQLValue))


