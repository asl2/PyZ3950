#!/usr/bin/env python
from PyZ3950 import asn1
#None
#ILL_APDU depends on ['Overdue', 'Expired', 'Status_Or_Error_Report', 'Conditional_Reply', 'Cancel', 'Message', 'Returned', 'Shipped', 'Cancel_Reply', 'ILL_Request', 'Forward_Notification', 'Renew', 'Recall', 'Renew_Answer', 'Lost', 'Checked_In', 'Status_Query', 'Damaged', 'Received', 'ILL_Answer']
#ILL_Request depends on ['Transaction_Id', 'Delivery_Service', 'ILL_Service_Type', 'Client_Id', 'Service_Date_Time', 'System_Id', 'Requester_Optional_Messages_Type', 'Third_Party_Info_Type', 'Search_Type', 'Transaction_Type', 'Item_Id', 'Supplemental_Item_Description', 'Cost_Info_Type', 'Extension', 'ILL_String', 'Place_On_Hold_Type', 'Delivery_Address', 'Supply_Medium_Info_Type']
#Forward_Notification depends on ['Transaction_Id', 'ILL_String', 'Extension', 'Service_Date_Time', 'System_Id', 'System_Address']
#Shipped depends on ['Transaction_Id', 'Supply_Details', 'System_Address', 'Client_Id', 'Service_Date_Time', 'System_Id', 'Transaction_Type', 'Responder_Optional_Messages_Type', 'Extension', 'Postal_Address', 'ILL_String', 'Supplemental_Item_Description', 'Shipped_Service_Type']
#ILL_Answer depends on ['Transaction_Id', 'Send_To_List_Type', 'Already_Tried_List_Type', 'System_Id', 'Service_Date_Time', 'Transaction_Results', 'Hold_Placed_Results', 'Estimate_Results', 'Responder_Optional_Messages_Type', 'Unfilled_Results', 'Conditional_Results', 'Extension', 'ILL_String', 'Locations_Results', 'Supplemental_Item_Description', 'Will_Supply_Results', 'Retry_Results']
#Conditional_Reply depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Cancel depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Cancel_Reply depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Received depends on ['Transaction_Id', 'ILL_String', 'Extension', 'ISO_Date', 'Service_Date_Time', 'System_Id', 'Supplemental_Item_Description', 'Shipped_Service_Type']
#Recall depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Returned depends on ['Transaction_Id', 'Amount', 'Extension', 'ILL_String', 'Transportation_Mode', 'ISO_Date', 'Service_Date_Time', 'System_Id', 'Supplemental_Item_Description']
#Checked_In depends on ['Transaction_Id', 'ILL_String', 'Extension', 'ISO_Date', 'Service_Date_Time', 'System_Id']
#Overdue depends on ['Transaction_Id', 'ILL_String', 'Extension', 'Service_Date_Time', 'System_Id', 'Date_Due']
#Renew depends on ['Transaction_Id', 'ILL_String', 'Extension', 'ISO_Date', 'Service_Date_Time', 'System_Id']
#Renew_Answer depends on ['Transaction_Id', 'ILL_String', 'Extension', 'Service_Date_Time', 'System_Id', 'Date_Due']
#Lost depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Damaged depends on ['Transaction_Id', 'Damaged_Details', 'ILL_String', 'Extension', 'Service_Date_Time', 'System_Id']
#Message depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Status_Query depends on ['Extension', 'Transaction_Id', 'Service_Date_Time', 'System_Id', 'ILL_String']
#Status_Or_Error_Report depends on ['Reason_No_Report', 'Transaction_Id', 'Error_Report', 'Status_Report', 'ILL_String', 'Extension', 'Service_Date_Time', 'System_Id']
#Expired depends on ['Transaction_Id', 'Service_Date_Time', 'System_Id', 'Extension']
#Account_Number depends on ['ILL_String']
#Already_Forwarded depends on ['System_Address', 'System_Id']
#Already_Tried_List_Type depends on ['System_Id']
#Amount depends on ['AmountString']
#AmountString depends on []
#Client_Id depends on ['ILL_String']
#Conditional_Results depends on ['ISO_Date', 'Delivery_Service', 'Location_Info']
#Cost_Info_Type depends on ['Amount', 'Account_Number']
#Current_State depends on []
#Damaged_Details depends on []
#Date_Due depends on ['ISO_Date']
#Delivery_Address depends on ['Postal_Address', 'System_Address']
#Delivery_Service depends on ['Transportation_Mode', 'Electronic_Delivery_Service']
#Electronic_Delivery_Service depends on ['ILL_String', 'System_Id', 'ISO_Time', 'System_Address']
#Error_Report depends on ['ILL_String', 'Provider_Error_Report', 'Report_Source', 'User_Error_Report']
#Estimate_Results depends on ['Location_Info', 'ILL_String']
#Extension depends on []
#General_Problem depends on []
#History_Report depends on ['ISO_Date', 'ILL_String', 'System_Id', 'Transaction_Results', 'Shipped_Service_Type']
#Hold_Placed_Results depends on ['ISO_Date', 'Medium_Type', 'Location_Info']
#ILL_APDU_Type depends on []
#ILL_Service_Type depends on []
#ILL_String depends on ['EDIFACTString']
#Intermediary_Problem depends on []
#ISO_Date depends on []
#ISO_Time depends on []
#Item_Id depends on ['Medium_Type', 'ILL_String']
#Location_Info depends on ['ILL_String', 'System_Id', 'System_Address']
#Locations_Results depends on ['Location_Info', 'Reason_Locs_Provided']
#Medium_Type depends on []
#Name_Of_Person_Or_Institution depends on ['ILL_String']
#Person_Or_Institution_Symbol depends on ['ILL_String']
#Place_On_Hold_Type depends on []
#Postal_Address depends on ['Name_Of_Person_Or_Institution', 'ILL_String']
#Provider_Error_Report depends on ['State_Transition_Prohibited', 'General_Problem', 'Transaction_Id_Problem']
#Reason_Locs_Provided depends on []
#Reason_No_Report depends on []
#Reason_Unfilled depends on []
#Report_Source depends on []
#Requester_Optional_Messages_Type depends on []
#Responder_Optional_Messages_Type depends on []
#Retry_Results depends on ['ISO_Date', 'Location_Info']
#Search_Type depends on ['ISO_Date', 'ILL_String']
#Security_Problem depends on ['ILL_String']
#Send_To_List_Type depends on ['Account_Number', 'System_Id', 'System_Address']
#Service_Date_Time depends on ['ISO_Date', 'ISO_Time']
#Shipped_Service_Type depends on ['ILL_Service_Type']
#State_Transition_Prohibited depends on ['Current_State', 'ILL_APDU_Type']
#Status_Report depends on ['History_Report', 'Current_State']
#Supplemental_Item_Description depends on []
#Supply_Details depends on ['Units_Per_Medium_Type', 'Electronic_Delivery_Service', 'Transportation_Mode', 'ISO_Date', 'Date_Due', 'Amount']
#Supply_Medium_Info_Type depends on ['Supply_Medium_Type', 'ILL_String']
#Supply_Medium_Type depends on []
#System_Address depends on ['ILL_String']
#System_Id depends on ['Name_Of_Person_Or_Institution', 'Person_Or_Institution_Symbol']
#Third_Party_Info_Type depends on ['Send_To_List_Type', 'Already_Tried_List_Type', 'System_Address']
#Transaction_Id depends on ['ILL_String', 'System_Id']
#Transaction_Id_Problem depends on []
#Transaction_Results depends on []
#Transaction_Type depends on []
#Transportation_Mode depends on ['ILL_String']
#Unable_To_Perform depends on []
#Unfilled_Results depends on ['Location_Info', 'Reason_Unfilled']
#Units_Per_Medium_Type depends on ['Supply_Medium_Type']
#User_Error_Report depends on ['Security_Problem', 'Intermediary_Problem', 'Already_Forwarded', 'Unable_To_Perform']
#Will_Supply_Results depends on ['ISO_Date', 'Electronic_Delivery_Service', 'Location_Info', 'Postal_Address']
#EDIFACTString depends on []
General_Problem=asn1.ENUM
Transaction_Id_Problem=asn1.ENUM
Reason_Unfilled=asn1.ENUM
Medium_Type=asn1.ENUM
Damaged_Details=asn1.SEQUENCE ([('document_type_id',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),1),
    ('damaged_portion',None,    asn1.CHOICE ([('complete_document',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.NULL)),
        ('specific_units',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),        asn1.SEQUENCE_OF (asn1.INTEGER)))]),0)])
Extension=asn1.SEQUENCE ([('identifier',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('critical',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('item',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.ANY_constr(def_by="identifier")),0)])
Reason_No_Report=asn1.ENUM
ISO_Date=asn1.VisibleString
AmountString=asn1.PrintableString
ILL_APDU_Type=asn1.ENUM
ISO_Time=asn1.VisibleString
Supplemental_Item_Description=asn1.SEQUENCE_OF (asn1.EXTERNAL)
Requester_Optional_Messages_Type=asn1.SEQUENCE ([('can_send_RECEIVED',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('can_send_RETURNED',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('requester_SHIPPED',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0),
    ('requester_CHECKED_IN',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0)])
Transaction_Type=asn1.ENUM
Report_Source=asn1.ENUM
Service_Date_Time=asn1.SEQUENCE ([('date_time_of_this_service',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('date',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
        ('time',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ISO_Time),1)])),0),
    ('date_time_of_original_service',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('date',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
        ('time',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ISO_Time),1)])),1)])
EDIFACTString=asn1.VisibleString
Responder_Optional_Messages_Type=asn1.SEQUENCE ([('can_send_SHIPPED',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('can_send_CHECKED_IN',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('responder_RECEIVED',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0),
    ('responder_RETURNED',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0)])
Current_State=asn1.ENUM
State_Transition_Prohibited=asn1.SEQUENCE ([('aPDU_type',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_APDU_Type),0),
    ('current_state',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Current_State),0)])
ILL_Service_Type=asn1.ENUM
Intermediary_Problem=asn1.ENUM
Reason_Locs_Provided=asn1.ENUM
Amount=asn1.SEQUENCE ([('currency_code',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.PrintableString),1),
    ('monetary_value',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),AmountString),0)])
ILL_String=asn1.CHOICE ([('asn1.GeneralString',None,asn1.GeneralString),
    ('EDIFACTString',None,EDIFACTString)])
Shipped_Service_Type=ILL_Service_Type
Supply_Medium_Type=asn1.ENUM
Transaction_Results=asn1.ENUM
Place_On_Hold_Type=asn1.ENUM
Client_Id=asn1.SEQUENCE ([('client_name',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('client_status',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('client_identifier',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Provider_Error_Report=asn1.CHOICE ([('general_problem',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),General_Problem)),
    ('transaction_id_problem',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id_Problem)),
    ('state_transition_prohibited',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),State_Transition_Prohibited))])
Date_Due=asn1.SEQUENCE ([('date_due_field',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('renewable',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)])
Unable_To_Perform=asn1.ENUM
Supply_Medium_Info_Type=asn1.SEQUENCE ([('supply_medium_type',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),Supply_Medium_Type),0),
    ('medium_characteristics',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Transportation_Mode=ILL_String
Account_Number=ILL_String
Search_Type=asn1.SEQUENCE ([('level_of_service',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('need_before_date',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('expiry_flag',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.ENUM),1),
    ('expiry_date',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),ISO_Date),1)])
Units_Per_Medium_Type=asn1.SEQUENCE ([('medium',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Supply_Medium_Type),0),
    ('no_of_units',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0)])
Cost_Info_Type=asn1.SEQUENCE ([('account_number',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Account_Number),1),
    ('maximum_cost',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Amount),1),
    ('reciprocal_agreement',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('will_pay_fee',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('payment_provided',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1)])
Item_Id=asn1.SEQUENCE ([('item_type',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.ENUM),1),
    ('held_medium_type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Medium_Type),1),
    ('call_number',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('author',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('title',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('sub_title',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('sponsoring_body',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('place_of_publication',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('publisher',None,asn1.TYPE(asn1.EXPLICIT(8,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('series_title_number',None,asn1.TYPE(asn1.EXPLICIT(9,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('volume_issue',None,asn1.TYPE(asn1.EXPLICIT(10,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('edition',None,asn1.TYPE(asn1.EXPLICIT(11,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('publication_date',None,asn1.TYPE(asn1.EXPLICIT(12,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('publication_date_of_component',None,asn1.TYPE(asn1.EXPLICIT(13,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('author_of_article',None,asn1.TYPE(asn1.EXPLICIT(14,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('title_of_article',None,asn1.TYPE(asn1.EXPLICIT(15,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('pagination',None,asn1.TYPE(asn1.EXPLICIT(16,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('national_bibliography_no',None,asn1.TYPE(asn1.EXPLICIT(17,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('iSBN',None,asn1.TYPE(asn1.EXPLICIT(18,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('iSSN',None,asn1.TYPE(asn1.EXPLICIT(19,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('system_no',None,asn1.TYPE(asn1.EXPLICIT(20,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('additional_no_letters',None,asn1.TYPE(asn1.EXPLICIT(21,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('verification_reference_source',None,asn1.TYPE(asn1.EXPLICIT(22,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Name_Of_Person_Or_Institution=asn1.CHOICE ([('name_of_person',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String)),
    ('name_of_institution',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String))])
System_Address=asn1.SEQUENCE ([('telecom_service_identifier',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('telecom_service_address',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Person_Or_Institution_Symbol=asn1.CHOICE ([('person_symbol',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String)),
    ('institution_symbol',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String))])
Security_Problem=ILL_String
Postal_Address=asn1.SEQUENCE ([('name_of_person_or_institution',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Name_Of_Person_Or_Institution),1),
    ('extended_postal_delivery_address',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('street_and_number',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('post_office_box',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('city',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('region',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('country',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('postal_code',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Delivery_Address=asn1.SEQUENCE ([('postal_address',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),Postal_Address),1),
    ('electronic_address',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),System_Address),1)])
System_Id=asn1.SEQUENCE ([('person_or_institution_symbol',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),Person_Or_Institution_Symbol),1),
    ('name_of_person_or_institution',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Name_Of_Person_Or_Institution),1)])
Electronic_Delivery_Service=asn1.SEQUENCE ([('e_delivery_service',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('e_delivery_mode',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
        ('e_delivery_parameters',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.ANY_constr(def_by="e_delivery_mode")),0)])),1),
    ('document_type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE ([('document_type_id',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.OBJECT_IDENTIFIER),0),
        ('document_type_parameters',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.ANY_constr(def_by="document_type_id")),0)])),1),
    ('e_delivery_description',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('e_delivery_details',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('e_delivery_address',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),System_Address)),
        ('e_delivery_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),System_Id))])),0),
    ('name_or_code',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('delivery_time',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),ISO_Time),1)])
Send_To_List_Type=asn1.SEQUENCE_OF (asn1.SEQUENCE ([('system_id',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),System_Id),0),
    ('account_number',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Account_Number),1),
    ('system_address',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),System_Address),1)]))
Already_Tried_List_Type=asn1.SEQUENCE_OF (System_Id)
Supply_Details=asn1.SEQUENCE ([('date_shipped',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('date_due',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Date_Due),1),
    ('chargeable_units',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),1),
    ('cost',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),Amount),1),
    ('shipped_conditions',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),asn1.ENUM),1),
    ('shipped_via',None,    asn1.CHOICE ([('physical_delivery',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),Transportation_Mode)),
        ('electronic_delivery',None,asn1.TYPE(asn1.IMPLICIT(50,cls=asn1.CONTEXT_FLAG),Electronic_Delivery_Service))]),1),
    ('insured_for',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),Amount),1),
    ('return_insurance_require',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),Amount),1),
    ('no_of_units_per_medium',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Units_Per_Medium_Type)),1)])
Location_Info=asn1.SEQUENCE ([('location_id',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),System_Id),0),
    ('location_address',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),System_Address),1),
    ('location_note',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Already_Forwarded=asn1.SEQUENCE ([('responder_id',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),System_Id),0),
    ('responder_address',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),System_Address),1)])
Transaction_Id=asn1.SEQUENCE ([('initial_requester_id',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('transaction_group_qualifier',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String),0),
    ('transaction_qualifier',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ILL_String),0),
    ('sub_transaction_qualifier',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
Expired=asn1.TYPE(asn1.EXPLICIT(20,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('expired_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Forward_Notification=asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),0),
    ('responder_address',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),System_Address),1),
    ('intermediary_id',None,asn1.TYPE(asn1.IMPLICIT(25,cls=asn1.CONTEXT_FLAG),System_Id),0),
    ('notification_note',None,asn1.TYPE(asn1.EXPLICIT(48,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('forward_notification_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Returned=asn1.TYPE(asn1.EXPLICIT(10,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('supplemental_item_description',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),Supplemental_Item_Description),1),
    ('date_returned',None,asn1.TYPE(asn1.IMPLICIT(37,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('returned_via',None,asn1.TYPE(asn1.EXPLICIT(38,cls=asn1.CONTEXT_FLAG),Transportation_Mode),1),
    ('insured_for',None,asn1.TYPE(asn1.IMPLICIT(39,cls=asn1.CONTEXT_FLAG),Amount),1),
    ('requester_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('returned_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Cancel_Reply=asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('answer',None,asn1.TYPE(asn1.IMPLICIT(35,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('cancel_reply_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Lost=asn1.TYPE(asn1.EXPLICIT(15,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('lost_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Checked_In=asn1.TYPE(asn1.EXPLICIT(11,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('date_checked_in',None,asn1.TYPE(asn1.IMPLICIT(40,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('checked_in_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Damaged=asn1.TYPE(asn1.EXPLICIT(16,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('damaged_details',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),Damaged_Details),1),
    ('note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('damaged_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Retry_Results=asn1.SEQUENCE ([('reason_not_available',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.ENUM),1),
    ('retry_date',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),1)])
Delivery_Service=asn1.CHOICE ([('physical_delivery',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),Transportation_Mode)),
    ('electronic_delivery',None,asn1.TYPE(asn1.IMPLICIT(50,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Electronic_Delivery_Service)))])
Cancel=asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('requester_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('cancel_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
History_Report=asn1.SEQUENCE ([('date_requested',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('author',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('title',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('author_of_article',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('title_of_article',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('date_of_last_transition',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('most_recent_service',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0),
    ('date_of_most_recent_service',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('initiator_of_most_recent_service',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),System_Id),0),
    ('shipped_service_type',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),Shipped_Service_Type),1),
    ('transaction_results',None,asn1.TYPE(asn1.IMPLICIT(10,cls=asn1.CONTEXT_FLAG),Transaction_Results),1),
    ('most_recent_service_note',None,asn1.TYPE(asn1.EXPLICIT(11,cls=asn1.CONTEXT_FLAG),ILL_String),1)])
User_Error_Report=asn1.CHOICE ([('already_forwarded',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),Already_Forwarded)),
    ('intermediary_problem',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Intermediary_Problem)),
    ('security_problem',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Security_Problem)),
    ('unable_to_perform',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),Unable_To_Perform))])
Hold_Placed_Results=asn1.SEQUENCE ([('estimated_date_available',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('hold_placed_medium_type',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Medium_Type),1),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),1)])
Unfilled_Results=asn1.SEQUENCE ([('reason_unfilled',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),Reason_Unfilled),0),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),1)])
Shipped=asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_address',None,asn1.TYPE(asn1.IMPLICIT(24,cls=asn1.CONTEXT_FLAG),System_Address),1),
    ('intermediary_id',None,asn1.TYPE(asn1.IMPLICIT(25,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('supplier_id',None,asn1.TYPE(asn1.IMPLICIT(26,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('client_id',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),Client_Id),1),
    ('transaction_type',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),Transaction_Type),1),
    ('supplemental_item_description',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),Supplemental_Item_Description),1),
    ('shipped_service_type',None,asn1.TYPE(asn1.IMPLICIT(27,cls=asn1.CONTEXT_FLAG),Shipped_Service_Type),0),
    ('responder_optional_messages',None,asn1.TYPE(asn1.IMPLICIT(28,cls=asn1.CONTEXT_FLAG),Responder_Optional_Messages_Type),1),
    ('supply_details',None,asn1.TYPE(asn1.IMPLICIT(29,cls=asn1.CONTEXT_FLAG),Supply_Details),0),
    ('return_to_address',None,asn1.TYPE(asn1.IMPLICIT(30,cls=asn1.CONTEXT_FLAG),Postal_Address),1),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('shipped_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Received=asn1.TYPE(asn1.EXPLICIT(8,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('supplier_id',None,asn1.TYPE(asn1.IMPLICIT(26,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('supplemental_item_description',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),Supplemental_Item_Description),1),
    ('date_received',None,asn1.TYPE(asn1.IMPLICIT(36,cls=asn1.CONTEXT_FLAG),ISO_Date),0),
    ('shipped_service_type',None,asn1.TYPE(asn1.IMPLICIT(27,cls=asn1.CONTEXT_FLAG),Shipped_Service_Type),0),
    ('requester_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('received_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Third_Party_Info_Type=asn1.SEQUENCE ([('permission_to_forward',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('permission_to_chain',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('permission_to_partition',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('permission_to_change_send_to_list',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('initial_requester_address',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Address),1),
    ('preference',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),asn1.ENUM),1),
    ('send_to_list',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),Send_To_List_Type),1),
    ('already_tried_list',None,asn1.TYPE(asn1.IMPLICIT(7,cls=asn1.CONTEXT_FLAG),Already_Tried_List_Type),1)])
Estimate_Results=asn1.SEQUENCE ([('cost_estimate',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String),0),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),1)])
ILL_Request=asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('transaction_type',None,asn1.TYPE(asn1.IMPLICIT(5,cls=asn1.CONTEXT_FLAG),Transaction_Type),1),
    ('delivery_address',None,asn1.TYPE(asn1.IMPLICIT(6,cls=asn1.CONTEXT_FLAG),Delivery_Address),1),
    ('delivery_service',None,Delivery_Service,1),
    ('billing_address',None,asn1.TYPE(asn1.IMPLICIT(8,cls=asn1.CONTEXT_FLAG),Delivery_Address),1),
    ('iLL_service_type',None,asn1.TYPE(asn1.IMPLICIT(9,cls=asn1.CONTEXT_FLAG),ILL_Service_Type),0),
    ('responder_specific_service',None,asn1.TYPE(asn1.EXPLICIT(10,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('requester_optional_messages',None,asn1.TYPE(asn1.IMPLICIT(11,cls=asn1.CONTEXT_FLAG),Requester_Optional_Messages_Type),0),
    ('search_type',None,asn1.TYPE(asn1.IMPLICIT(12,cls=asn1.CONTEXT_FLAG),Search_Type),1),
    ('supply_medium_info_type',None,asn1.TYPE(asn1.IMPLICIT(13,cls=asn1.CONTEXT_FLAG),Supply_Medium_Info_Type),1),
    ('place_on_hold',None,asn1.TYPE(asn1.IMPLICIT(14,cls=asn1.CONTEXT_FLAG),Place_On_Hold_Type),1),
    ('client_id',None,asn1.TYPE(asn1.IMPLICIT(15,cls=asn1.CONTEXT_FLAG),Client_Id),1),
    ('item_id',None,asn1.TYPE(asn1.IMPLICIT(16,cls=asn1.CONTEXT_FLAG),Item_Id),0),
    ('supplemental_item_description',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),Supplemental_Item_Description),1),
    ('cost_info_type',None,asn1.TYPE(asn1.IMPLICIT(18,cls=asn1.CONTEXT_FLAG),Cost_Info_Type),1),
    ('copyright_compliance',None,asn1.TYPE(asn1.EXPLICIT(19,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('third_party_info_type',None,asn1.TYPE(asn1.IMPLICIT(20,cls=asn1.CONTEXT_FLAG),Third_Party_Info_Type),1),
    ('retry_flag',None,asn1.TYPE(asn1.IMPLICIT(21,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('forward_flag',None,asn1.TYPE(asn1.IMPLICIT(22,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),1),
    ('requester_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('forward_note',None,asn1.TYPE(asn1.EXPLICIT(47,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('iLL_request_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Status_Query=asn1.TYPE(asn1.EXPLICIT(18,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('status_query_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Will_Supply_Results=asn1.SEQUENCE ([('reason_will_supply',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0),
    ('supply_date',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('return_to_address',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Postal_Address),1),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),1),
    ('electronic_delivery_service',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),Electronic_Delivery_Service),1)])
Locations_Results=asn1.SEQUENCE ([('reason_locs_provided',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),Reason_Locs_Provided),1),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),0)])
Message=asn1.TYPE(asn1.EXPLICIT(17,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),0),
    ('message_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Renew_Answer=asn1.TYPE(asn1.EXPLICIT(14,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('answer',None,asn1.TYPE(asn1.IMPLICIT(35,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('date_due',None,asn1.TYPE(asn1.IMPLICIT(41,cls=asn1.CONTEXT_FLAG),Date_Due),1),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('renew_answer_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Overdue=asn1.TYPE(asn1.EXPLICIT(12,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('date_due',None,asn1.TYPE(asn1.IMPLICIT(41,cls=asn1.CONTEXT_FLAG),Date_Due),0),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('overdue_extensions',None,asn1.TYPE(asn1.EXPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Status_Report=asn1.SEQUENCE ([('user_status_report',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),History_Report),0),
    ('provider_status_report',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Current_State),0)])
Conditional_Reply=asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('answer',None,asn1.TYPE(asn1.IMPLICIT(35,cls=asn1.CONTEXT_FLAG),asn1.BOOLEAN),0),
    ('requester_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('conditional_reply_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Renew=asn1.TYPE(asn1.EXPLICIT(13,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('desired_due_date',None,asn1.TYPE(asn1.IMPLICIT(42,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('requester_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('renew_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Recall=asn1.TYPE(asn1.EXPLICIT(9,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('recall_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Error_Report=asn1.SEQUENCE ([('correlation_information',None,asn1.TYPE(asn1.EXPLICIT(0,cls=asn1.CONTEXT_FLAG),ILL_String),0),
    ('report_source',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Report_Source),0),
    ('user_error_report',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),User_Error_Report),1),
    ('provider_error_report',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),Provider_Error_Report),1)])
Conditional_Results=asn1.SEQUENCE ([('conditions',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.ENUM),0),
    ('date_for_reply',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),ISO_Date),1),
    ('locations',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Location_Info)),1),
    ('proposed_delivery_service',None,Delivery_Service,1)])
ILL_Answer=asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('transaction_results',None,asn1.TYPE(asn1.IMPLICIT(31,cls=asn1.CONTEXT_FLAG),Transaction_Results),0),
    ('results_explanation',None,asn1.TYPE(asn1.EXPLICIT(32,cls=asn1.CONTEXT_FLAG),    asn1.CHOICE ([('conditional_results',None,asn1.TYPE(asn1.EXPLICIT(1,cls=asn1.CONTEXT_FLAG),Conditional_Results)),
        ('retry_results',None,asn1.TYPE(asn1.EXPLICIT(2,cls=asn1.CONTEXT_FLAG),Retry_Results)),
        ('unfilled_results',None,asn1.TYPE(asn1.EXPLICIT(3,cls=asn1.CONTEXT_FLAG),Unfilled_Results)),
        ('locations_results',None,asn1.TYPE(asn1.EXPLICIT(4,cls=asn1.CONTEXT_FLAG),Locations_Results)),
        ('will_supply_results',None,asn1.TYPE(asn1.EXPLICIT(5,cls=asn1.CONTEXT_FLAG),Will_Supply_Results)),
        ('hold_placed_results',None,asn1.TYPE(asn1.EXPLICIT(6,cls=asn1.CONTEXT_FLAG),Hold_Placed_Results)),
        ('estimate_results',None,asn1.TYPE(asn1.EXPLICIT(7,cls=asn1.CONTEXT_FLAG),Estimate_Results))])),1),
    ('responder_specific_results',None,asn1.TYPE(asn1.EXPLICIT(33,cls=asn1.CONTEXT_FLAG),asn1.EXTERNAL),1),
    ('supplemental_item_description',None,asn1.TYPE(asn1.IMPLICIT(17,cls=asn1.CONTEXT_FLAG),Supplemental_Item_Description),1),
    ('send_to_list',None,asn1.TYPE(asn1.IMPLICIT(23,cls=asn1.CONTEXT_FLAG),Send_To_List_Type),1),
    ('already_tried_list',None,asn1.TYPE(asn1.IMPLICIT(34,cls=asn1.CONTEXT_FLAG),Already_Tried_List_Type),1),
    ('responder_optional_messages',None,asn1.TYPE(asn1.IMPLICIT(28,cls=asn1.CONTEXT_FLAG),Responder_Optional_Messages_Type),1),
    ('responder_note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('ill_answer_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
Status_Or_Error_Report=asn1.TYPE(asn1.EXPLICIT(19,cls=asn1.APPLICATION_FLAG),asn1.SEQUENCE ([('protocol_version_num',None,asn1.TYPE(asn1.IMPLICIT(0,cls=asn1.CONTEXT_FLAG),asn1.INTEGER),0),
    ('transaction_id',None,asn1.TYPE(asn1.IMPLICIT(1,cls=asn1.CONTEXT_FLAG),Transaction_Id),0),
    ('service_date_time',None,asn1.TYPE(asn1.IMPLICIT(2,cls=asn1.CONTEXT_FLAG),Service_Date_Time),0),
    ('requester_id',None,asn1.TYPE(asn1.IMPLICIT(3,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('responder_id',None,asn1.TYPE(asn1.IMPLICIT(4,cls=asn1.CONTEXT_FLAG),System_Id),1),
    ('reason_no_report',None,asn1.TYPE(asn1.IMPLICIT(43,cls=asn1.CONTEXT_FLAG),Reason_No_Report),1),
    ('status_report',None,asn1.TYPE(asn1.IMPLICIT(44,cls=asn1.CONTEXT_FLAG),Status_Report),1),
    ('error_report',None,asn1.TYPE(asn1.IMPLICIT(45,cls=asn1.CONTEXT_FLAG),Error_Report),1),
    ('note',None,asn1.TYPE(asn1.EXPLICIT(46,cls=asn1.CONTEXT_FLAG),ILL_String),1),
    ('status_or_error_report_extensions',None,asn1.TYPE(asn1.IMPLICIT(49,cls=asn1.CONTEXT_FLAG),    asn1.SEQUENCE_OF (Extension)),1)]))
ILL_APDU=asn1.CHOICE ([('ILL_Request',None,ILL_Request),
    ('Forward_Notification',None,Forward_Notification),
    ('Shipped',None,Shipped),
    ('ILL_Answer',None,ILL_Answer),
    ('Conditional_Reply',None,Conditional_Reply),
    ('Cancel',None,Cancel),
    ('Cancel_Reply',None,Cancel_Reply),
    ('Received',None,Received),
    ('Recall',None,Recall),
    ('Returned',None,Returned),
    ('Checked_In',None,Checked_In),
    ('Overdue',None,Overdue),
    ('Renew',None,Renew),
    ('Renew_Answer',None,Renew_Answer),
    ('Lost',None,Lost),
    ('Damaged',None,Damaged),
    ('Message',None,Message),
    ('Status_Query',None,Status_Query),
    ('Status_Or_Error_Report',None,Status_Or_Error_Report),
    ('Expired',None,Expired)])
