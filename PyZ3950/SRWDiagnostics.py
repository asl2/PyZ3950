
# Base Class

class SRWDiagnostic (Exception):
    """ Base Diagnostic Class"""
    code = 0
    uri = "info:srw/diagnostic/1/"
    details = ""
    message = ""

    surrogate = 0
    fatal = 1

    def __str__(self):
        return "%s [%s]: %s" % (self.uri, self.message, self.details)

    # NB 'Need' name for serialization in SRW 
    def __init__(self, name=None):
        if (self.code):
            self.uri = "%s%d" % (self.uri, self.code)
        Exception.__init__(self)

# Diagnostic Types

class GeneralDiagnostic (SRWDiagnostic):
    pass

class CQLDiagnostic (SRWDiagnostic):
    pass

class RecordDiagnostic (SRWDiagnostic):
    pass

class ResultSetDiagnostic (SRWDiagnostic):
    pass

class SortDiagnostic (SRWDiagnostic):
    pass

class StyleDiagnostic (SRWDiagnostic):
    pass

class ScanDiagnostic (SRWDiagnostic):
    pass

class DeprecatedDiagnostic(SRWDiagnostic):
    def __init__(self,  name=None):
        print "WARNING:  Use of deprecated diagnostic %s" % (self)
        SRWDiagnostic.__init__(self)

class ExplainDiagnostic (DeprecatedDiagnostic):
    pass


# Rob's (empty) diagnostic set
class RobDiagnostic (SRWDiagnostic):
    uri = "info:srw/diagnostic/2/"


# Individual Diagnostics

class Diagnostic1 (GeneralDiagnostic):
    code = 1
    message = "General system error"

class Diagnostic2 (GeneralDiagnostic):
    code = 2
    message = "System temporarily unavailable"

class Diagnostic3 (GeneralDiagnostic):
    code = 3
    message = "Authentication error"

class Diagnostic4 (GeneralDiagnostic):
    code = 4
    message = "Unsupported operation"

class Diagnostic5 (GeneralDiagnostic):
    code = 5
    message = "Unsupported version"

class Diagnostic6 (GeneralDiagnostic):
    code = 6
    message = "Unsupported parameter value"

class Diagnostic7 (GeneralDiagnostic):
    code = 7
    message = "Mandatory parameter not supplied"

class Diagnostic8 (GeneralDiagnostic):
    code = 8
    message = "Unknown parameter"



class Diagnostic10 (CQLDiagnostic):
    code = 10
    message = "Malformed query"

class Diagnostic13 (CQLDiagnostic):
    code = 13
    message = "Unsupported use of parentheses"

class Diagnostic14 (CQLDiagnostic):
    code = 14
    message = "Unsupported use of quotes"

class Diagnostic15 (CQLDiagnostic):
    code = 15
    message = "Unsupported context set"

class Diagnostic16 (CQLDiagnostic):
    code = 16
    message = "Unsupported index"

class Diagnostic18 (CQLDiagnostic):
    code = 18
    message = "Unsupported combination of indexes"

class Diagnostic19 (CQLDiagnostic):
    code = 19
    message = "Unsupported relation"

class Diagnostic20 (CQLDiagnostic):
    code = 20
    message = "Unsupported relation modifier"

class Diagnostic21 (CQLDiagnostic):
    code = 21
    message = "Unsupported combination of relation modifiers"

class Diagnostic22 (CQLDiagnostic):
    code = 22
    message = "Unsupported combination of relation and index"

class Diagnostic23 (CQLDiagnostic):
    code = 23
    message = "Too many characters in term"

class Diagnostic24 (CQLDiagnostic):
    code = 24
    message = "Unsupported combination of relation and term"

class Diagnostic26 (CQLDiagnostic):
    code = 26
    message = "Non special character escaped in term"

class Diagnostic27 (CQLDiagnostic):
    code = 27
    message = "Empty term unsupported"

class Diagnostic28 (CQLDiagnostic):
    code = 28
    message = "Masking character not supported"

class Diagnostic29 (CQLDiagnostic):
    code = 29
    message = "Masked words too short"

class Diagnostic30 (CQLDiagnostic):
    code = 30
    message = "Too many masking characters in term"

class Diagnostic31 (CQLDiagnostic):
    code = 31
    message = "Anchoring character not supported"

class Diagnostic32 (CQLDiagnostic):
    code = 32
    message = "Anchoring character in unsupported position."

class Diagnostic33 (CQLDiagnostic):
    code = 33
    message = "Combination of proximity/adjacency and masking characters not supported"

class Diagnostic34 (CQLDiagnostic):
    code = 34
    message = "Combination of proximity/adjacency and anchoring characters not supported"

class Diagnostic35 (CQLDiagnostic):
    code = 35
    message = "Term only stopwords"

class Diagnostic36 (CQLDiagnostic):
    code = 36
    message = "Term in invalid format for index or relation"

class Diagnostic37 (CQLDiagnostic):
    code = 37
    message = "Unsupported boolean operator"

class Diagnostic38 (CQLDiagnostic):
    code = 38
    message = "Too many boolean operators"

class Diagnostic39 (CQLDiagnostic):
    code = 39
    message = "Proximity not supported"

class Diagnostic40 (CQLDiagnostic):
    code = 40
    message = "Unsupported proximity relation"

class Diagnostic41 (CQLDiagnostic):
    code = 41
    message = "Unsupported proximity distance"

class Diagnostic42 (CQLDiagnostic):
    code = 42
    message = "Unsupported proximity unit"

class Diagnostic43 (CQLDiagnostic):
    code = 43
    message = "Unsupported proximity ordering"

class Diagnostic44 (CQLDiagnostic):
    code = 44
    message = "Unsupported combination of proximity modifiers"



class Diagnostic50 (ResultSetDiagnostic):
    code = 50
    message = "Result sets not supported"

class Diagnostic51 (ResultSetDiagnostic):
    code = 51
    message = "Result set does not exist"

class Diagnostic52 (ResultSetDiagnostic):
    code = 52
    message = "Result set temporarily unavailable"

class Diagnostic53 (ResultSetDiagnostic):
    code = 53
    message = "Result sets only supported for retrieval"

class Diagnostic55 (ResultSetDiagnostic):
    code = 55
    message = "Combination of result sets with search terms not supported"

class Diagnostic58 (ResultSetDiagnostic):
    code = 58
    message = "Result set created with unpredictable partial results available"

class Diagnostic59 (ResultSetDiagnostic):
    code = 59
    message = "Result set created with valid partial results available"


class Diagnostic60 (RecordDiagnostic):
    code = 60
    message = "Too many records retrieved"

class Diagnostic61 (RecordDiagnostic):
    code = 61
    message = "First record position out of range"

class Diagnostic64 (RecordDiagnostic):
    code = 64
    message = "Record temporarily unavailable"
    surrogate = 1

class Diagnostic65 (RecordDiagnostic):
    code = 65
    message = "Record does not exist"
    surrogate = 1

class Diagnostic66 (RecordDiagnostic):
    code = 66
    message = "Unknown schema for retrieval"

class Diagnostic67 (RecordDiagnostic):
    code = 67
    message = "Record not available in this schema"
    surrogate = 1

class Diagnostic68 (RecordDiagnostic):
    code = 68
    message = "Not authorised to send record"
    surrogate = 1

class Diagnostic69 (RecordDiagnostic):
    code = 69
    message = "Not authorised to send record in this schema"
    surrogate = 1

class Diagnostic70 (RecordDiagnostic):
    code = 70
    message = "Record too large to send"
    surrogate = 1

class Diagnostic71 (RecordDiagnostic):
    code = 71
    message = "Unsupported record packing"

class Diagnostic72 (RecordDiagnostic):
    code = 72
    message = "XPath retrieval unsupported"

class Diagnostic73 (RecordDiagnostic):
    code = 73
    message = "XPath expression contains unsupported feature"

class Diagnostic74 (RecordDiagnostic):
    code = 74
    message = "Unable to evaluate XPath expression"



class Diagnostic80 (SortDiagnostic):
    code = 80
    message = "Sort not supported"

class Diagnostic82 (SortDiagnostic):
    code = 82
    message = "Unsupported sort sequence"

class Diagnostic83 (SortDiagnostic):
    code = 83
    message = "Too many records to sort"

class Diagnostic84 (SortDiagnostic):
    code = 84
    message = "Too many sort keys"

class Diagnostic86 (SortDiagnostic):
    code = 86
    message = "Incompatible record formats"

class Diagnostic87 (SortDiagnostic):
    code = 87
    message = "Unsupported schema for sort"

class Diagnostic88 (SortDiagnostic):
    code = 88
    message = "Unsupported tag path for sort"

class Diagnostic89 (SortDiagnostic):
    code = 89
    message = "Tag path unsupported for schema"

class Diagnostic90 (SortDiagnostic):
    code = 90
    message = "Unsupported direction value"

class Diagnostic91 (SortDiagnostic):
    code = 91
    message = "Unsupported case value"

class Diagnostic92 (SortDiagnostic):
    code = 92
    message = "Unsupported missing value action"


class Diagnostic110 (StyleDiagnostic):
    code = 110
    message = "Stylesheets not supported"

class Diagnostic111 (StyleDiagnostic):
    code = 111
    message = "Unsupported stylesheet"

class Diagnostic120 (ScanDiagnostic):
    code = 120
    message = "Response position out of range"

class Diagnostic121 (ScanDiagnostic):
    code = 121
    message = "Too many terms requested"

    



# Deprecated diagnostics

class Diagnostic11 (DeprecatedDiagnostic):
    code = 11
    message = "Unsupported query type"

class Diagnostic12 (DeprecatedDiagnostic):
    code = 12
    message = "Too many characters in query"

class Diagnostic17 (DeprecatedDiagnostic):
    code = 17
    message = "Illegal or unsupported combination of index and index set."

class Diagnostic25 (DeprecatedDiagnostic):
    code = 25
    message = "Special characters not quoted in term"

class Diagnostic45 (DeprecatedDiagnostic):
    code = 45
    message = "Index set name (prefix) assigned to multiple identifiers"

class Diagnostic54 (DeprecatedDiagnostic):
    code = 54
    message = "Retrieval may only occur from an existing result set"

class Diagnostic56 (DeprecatedDiagnostic):
    code = 56
    message = "Only combination of single result set with search terms supported"

class Diagnostic57 (DeprecatedDiagnostic):
    code = 57
    message = "Result set created but no records available"

class Diagnostic62 (DeprecatedDiagnostic):
    code = 62
    message = "Negative number of records requested"

class Diagnostic63 (DeprecatedDiagnostic):
    code = 63
    message = "System error in retrieving records"

class Diagnostic81 (DeprecatedDiagnostic):
    code = 81
    message = "Unsupported sort type"

class Diagnostic85 (DeprecatedDiagnostic):
    code = 85
    message = "Duplicate sort keys"

class Diagnostic100 (ExplainDiagnostic):
    code = 100
    message = "Explain not supported"

class Diagnostic101 (ExplainDiagnostic):
    code = 101
    message = "Explain request type not supported"

class Diagnostic102 (ExplainDiagnostic):
    code = 102
    message = "Explain record temporarily unavailable"














    
