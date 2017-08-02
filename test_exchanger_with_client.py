#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Exchanger With Client
  Created: 08/01/17
"""

import unittest
import time

from vikitx.core.proto.zed import Exchanger
from vikitx.core.proto.zed import ZProducer, ZConsumer

########################################################################
class ExchangerWithClients(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_exchanger_with_client(self):
        """"""
        exchanger = Exchanger('exchangerme', backend_port=4567)
        exchanger.regist_entry(1234)
        exchanger.regist_router('test', 2345)
        exchanger.start()
        
        p = ZProducer(host='127.0.0.1', target_port=1234)
        self.assertTrue(p.send({'routing_key':'test',
                                'message':{'token':'adfadfadfsadf',
                                           'testasdfasdf':{1:345}}}))
        
        r = ZConsumer(host='127.0.0.1', router_port=2345, ack_port=4567)
        r.poll(timeout=1000)
        self.assertIsInstance(r.recv(), dict)
        
        time.sleep(4)
        
        exchanger.stop()
        
        
        
    
    

if __name__ == '__main__':
    unittest.main()