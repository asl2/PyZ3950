#!/usr/bin/env python

from __future__ import print_function
import random
import time

from PyZ3950 import zoom

from threading import Thread, currentThread
from Queue import Queue

thread_count = 10
parse_only = 1


class TestThread (Thread):
    def __init__ (self, terminate_queue, *args, **kw):
        Thread.__init__ (self, *args, **kw)
        self.terminate_queue = terminate_queue
        self.count = 0
        self.queries = [
            'any = wive and any = wealthily',
            'any = mandrake',]
#            'ti = Necronomicon',
#            'au = Bourbaki']
    def consume (self, record):
        pass
            
    def run (self):
        if not parse_only:
            self.conn = zoom.Connection ('localhost', 2100)
            self.conn.preferredRecordSyntax = 'SUTRS'
        while 1:
            self.count += 1
#            if not (self.count % 100):
#                print "Thread", currentThread (), "Count", self.count
            query_str = random.choice (self.queries)
            try:
                q = zoom.Query ('CCL', query_str)
                if not parse_only:
                    r = self.conn.search (q)
                    for rec in r:
                        self.consume (rec)
            except zoom.Bib1Err as err:
                pass
            except zoom.QuerySyntaxError as e:
                print("e", e, "q", query_str)

            if self.count > 500:
                if not parse_only:
                    self.conn.close ()
                # should randomly do clean vs. not clean exit
                self.terminate_queue.put (self, 1)
                break

if __name__ == '__main__':
    start_t = time.time()
    thread_list = []
    terminate_queue = Queue ()
    for i in range (thread_count):
        t = TestThread (terminate_queue)
        t.start ()
        thread_list.append (t)
    total_count = 0

    while len (thread_list) > 0:
        t = terminate_queue.get (1)
        t.join ()
        total_count += t.count
        thread_list.remove (t)
    
    end_t = time.time ()
    elapsed = end_t - start_t
    print("total", total_count, "elapsed", elapsed)
    print("rate", total_count * 1.0 / elapsed)
    
        
        
        
