#!/usr/bin/env python
import ill
from PyZ3950 import asn1

class Dummy:
    pass

def mk_ill_str (s):
    return ('asn1.GeneralString', s)

def test_req ():
    req = ill.ILL_Request ()
    trans_id = ill.Transaction_Id ()
    trans_id.transaction_group_qualifier = mk_ill_str ('foo')
    trans_id.transaction_qualifier = mk_ill_str ('bar')
    this_serv = Dummy ()
    this_serv.date = '20020906'
    serv_date_time = ill.Service_Date_Time ()
    serv_date_time.date_time_of_this_service = this_serv
    req.protocol_version_num = 1
    req.transaction_id = trans_id
    req.service_date_time = serv_date_time
    req.iLL_service_type = [ill.ILL_Service_Type.loan]
    smit = ill.Supply_Medium_Info_Type ()
    smit.supply_medium_type = ill.Supply_Medium_Type.printed
    req.supply_medium_info_type = [smit]
    ii = ill.Item_Id ()
    ii.title = mk_ill_str ('1066 and all that')
    req.item_id = ii
    rom = ill.Requester_Optional_Messages_Type ()
    rom.can_send_RECEIVED = 1
    rom.can_send_RETURNED = 0
    rom.requester_SHIPPED = 1 # XXX should be enum
    rom.requester_CHECKED_IN = 1 # ditto
    req.requester_optional_messages = rom
    req =  ('ILL_Request', req)
    print(req)
    ber = asn1.encode (ill.ILL_APDU,req)
    print(ber)
    req_1 = asn1.decode (ill.ILL_APDU, ber)
    print(req_1)
    assert (req_1 == req)
    
if __name__ == '__main__':
    test_req ()
