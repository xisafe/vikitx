#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test for exchanger
  Created: 07/30/17
"""

import unittest

from vikitx.core.proto.zed import Exchanger

########################################################################
class ExchangerTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_exchanger(self):
        """"""
        exchanger = Exchanger(id='exchanger', host='127.0.0.1', backend_port=3424)
        exchanger.regist_entry(addr)
        exchanger.regist_router(router_key, addr)
        
    
    

if __name__ == '__main__':
    unittest.main()