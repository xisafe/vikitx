#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Node Client Tester
  Created: 07/28/17
"""

import unittest

from vikitx.entity.servicenode._client import SNClient

########################################################################
class ServiceNodeClientTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_platform_server(self):
        """"""
        client = SNClient('client', '127.0.0.1')
        client.connect('127.0.0.1', '7000')


if __name__ == '__main__':
    unittest.main()