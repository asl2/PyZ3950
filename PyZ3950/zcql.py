
# Build configuration for Z39.50 <-> CQL

from PyZ3950 import asn1, oids
asn1.register_oid (oids.Z3950_QUERY_CQL, asn1.GeneralString)

class ZCQLConfig:

    DC = {'title' : 4,
          'subject' : 21,
          'creator' : 1003,
          'author' : 1003,
          'editor' : 1020,
          'publisher' : 1018,
          'description' : 62,
          'date' : 30,
          'resourceType' : 1031,
          'format' : 1034,
          'resourceIdentifier' : 12,
          'source' : 1019,
          'language' : 54
          }

    CQL = {'anywhere' : 1016,
           'serverChoice' : 1016}

    # The common bib1 points
    BIB1 = {"personal_name" : 1,
            "corporate_name" : 2,
            "conference_name" : 3,
            "title" : 4,
            "title_series" : 5,
            "title_uniform" : 6,
            "isbn" : 7,
            "issn" : 8,
            "lccn" : 9,
            "local_number" : 12,
            "dewey_number" : 13,
            "lccn" : 16,
            "local_classification" : 20,
            "subject" : 21,
            "subject_lc" : 27,
            "subject_local" : 29,
            "date" : 30,
            "date_publication" : 31,
            "date_acquisition" : 32,
            "local_call_number" : 53,
            "abstract" : 62,
            "note" : 63,
            "record_type" : 1001,
            "name" : 1002,
            "author" : 1003,
            "author_personal" : 1004,
            "identifier" : 1007,
            "text_body" : 1010,
            "date_modified" : 1012,
            "date_added" : 1011,
            "concept_text" : 1014,
            "any" : 1016,
            "default" : 1017,
            "publisher" : 1018,
            "record_source" : 1019,
            "editor" : 1020,
            "docid" : 1032,
            "anywhere" : 1035,
            "sici" : 1037
            }
    
  
    XD1 = {"title" : 1,
          "subject" : 2,
          "name" : 3,
          "description" : 4,
          "date" : 5,
          "type" : 6,
          "format" : 7,
          "identifier" : 8,
          "source" : 9,
          "langauge" : 10,
          "relation" : 11,
          "coverage" : 12,
          "rights" : 13}

    UTIL = {"record_date" : 1,
            "record_agent" : 2,
            "record_language" : 3,
            "control_number" : 4,
            "cost" : 5,
            "record_syntax" : 6,
            "database_schema" : 7,
            "score" : 8,
            "rank" : 9,
            "result_set_position" : 10,
            "all" : 11,
            "anywhere" : 12,
            "server_choice" : 13,
            "wildcard" : 14,
            "wildpath" : 15}
    
          
