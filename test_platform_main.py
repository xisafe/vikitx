#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform
  Created: 08/02/17
"""

import unittest

from vikitx.entity import Nest, Phoenix

########################################################################
class PlatformMainTester(object):
    """"""

    #----------------------------------------------------------------------
    def test_1_platform_main(self):
        """"""
        plt = Nest('pid', host='127.0.0.1', port=7001)
        plt.set_default_service('test')
        plt.start()
        
    #----------------------------------------------------------------------
    def test_2_servicenode(self):
        """"""
        ph = Phoenix(nest_host='127.0.0.1', port=7001)
        ph.start()
        
    
    

if __name__ == '__main__':
    unittest.main()