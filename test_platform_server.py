#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Tester
  Created: 07/28/17
"""

import unittest

from vikitx.entity.platform._server import PlatformServer

########################################################################
class PlatformServerTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_platform_server(self):
        """"""
        pltfmsvr = PlatformServer('paltforom', 'tcp://127.0.0.1')
        
        pltfmsvr.start()
        
        
        
    
    

if __name__ == '__main__':
    unittest.main()