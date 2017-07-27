#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test Service
  Created: 07/26/17
"""

import unittest
import time

from vikitx.entity import Service, ServiceWraperInThread
from vikitx.entity import ServiceNode

#----------------------------------------------------------------------
def test(args, v1=4):
    """"""
    time.sleep(2)
    print('args', args)
    return 'result for this test target function'
    

########################################################################
class ServiceTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_single_service_in_process(self):
        """Constructor"""
        ser = Service(id='serviceid', target=test)
        ser.start()
        for i in range(6):
            ser.execute(task_id="id:{}".format(i) ,args=(i,), kwargs={})
        
        time.sleep(3)
        
        ser.stop()
    
    #----------------------------------------------------------------------
    def test_2_service_in_thread(self):
        """"""
        ser = ServiceWraperInThread(id='serviceidprocess', target=test)
        ser.start()
        for i in range(6):
            ser.execute(task_id="id:{}".format(i) ,args=(i,), kwargs={})
        
        time.sleep(3)
        
        ser.stop()
    
    #----------------------------------------------------------------------
    def test_2_servicenode_with_service_in_process(self):
        """"""
        ser = ServiceNode(id='servicenodeid')
        if ser.start_service(id, target=test)
        
    

if __name__ == '__main__':
    unittest.main()