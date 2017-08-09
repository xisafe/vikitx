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
from vikitx.core.workpool import task

########################################################################
class ZSRPSTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_start_server(self):
        """"""
        def print_result(_, result):
            print(result)
        
        svr = zsrps.ZSRPSServer('server')
        _t = task.Task(svr.send_action, 'client', 'asdfasdfsadfasdf')
        _t.call_later(5, print_result)
        svr.start(port=7000)
        
        time.sleep(3)
        #client = svr.get_available_client()[0]
        #scope = svr.get_scope(client)
        #assert isinstance(scope, dict)
        #svr.send_action(client_id='client', content='tetsetststs')
        #svr.join()
        

if __name__ == '__main__':
    unittest.main()