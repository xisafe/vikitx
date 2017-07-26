#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test ZSRPS
  Created: 07/19/17
"""

import unittest
import time

from vikitx.core.proto import zsrps

########################################################################
class ZSRPSTester(unittest.TestCase):
    """"""
        
    #----------------------------------------------------------------------
    def test_2_start_client(self):
        """"""
        self.clt = zsrps.ZSRPSClient('client', '127.0.0.1')
        self.clt.connect('127.0.0.1', port=7000)
        
        while self.clt.state != 'working':
            pass
    
        time.sleep(10)
        self.clt.stop()
        time.sleep(20)
        

if __name__ == '__main__':
    unittest.main()