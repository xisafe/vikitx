#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test ZSRPS
  Created: 07/19/17
"""

import unittest

from vikitx.core.proto import zsrps

########################################################################
class ZSRPSTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_start_server(self):
        """"""
        
        svr = zsrps.ZSRPSServer('server')
        svr.start(port=7000)

if __name__ == '__main__':
    unittest.main()