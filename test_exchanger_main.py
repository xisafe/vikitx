#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Exchanger Main test
  Created: 08/08/17
"""

import unittest
import time

from vikitx.core.proto.zed import Exchanger
from vikitx.core.proto.zed import Enxer

########################################################################
class ExchangerMaintest(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1(self):
        """Constructor"""
        
        exchgr = Exchanger('testexchanger')
        exchgr.start()
        exchgr.regist_entry(port=3456)
        exchgr.regist_router('testkey', port=3457)
        
        
        def test_callback(pkt):
            print(pkt)
            
        enxer = Enxer(host='127.0.0.1', ack_backend_port=3424)
        enxer.start()
        
        enxer.connect_entry(port=3456)
        enxer.send('testkey', {'token':'fake token',
                               'message':{'adsfasdfasd':'testmessgae'}})
        enxer.recv_from(key='testkey', port=3457, callback=test_callback, block=False)
        
        time.sleep(3)
        
        enxer.stop()
        exchgr.stop()
        

if __name__ == '__main__':
    unittest.main()