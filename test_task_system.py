#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test TaskSystem
  Created: 07/21/17
"""

import time
import unittest

from vikitx.core.workpool import threadpool
from vikitx.core.workpool.task import Task, LoopingCall

########################################################################
class TaskSystem(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_task(self):
        """"""
        def test(v1, v3=4):
            print("test", v1, v3)
            
        task = Task(test, 4, 543)
        task.execute()
        task.call_later(4)
    
    #----------------------------------------------------------------------
    def test_2_loopingcall(self):
        """"""
        
        def test1(v1, v2=4):
            print('test1', v1, v2)
        
        lp = LoopingCall(test1, 6, 7)
        lp.start(interval=3)
        time.sleep(9)
    
    #----------------------------------------------------------------------
    def test_z(self):
        """"""
        threadpool.stop()
        

if __name__ == '__main__':
    unittest.main()