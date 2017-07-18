#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Vikitx
  Created: 07/16/17
"""

import unittest
import time

from vikitx.core.session import Session, SessionManager
from vikitx.core.workpool import threadpool

########################################################################
class VikitxBasicTest(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_session_control(self):
        """"""
        #
        # scope test
        #
        _session = Session('testsessionid')
        _session.add(key='key1', value='value1')
        self.assertEqual(_session.scope['key1'], 'value1')
        
        #
        # test session
        #
        manager = SessionManager()
        manager.add(_session)
        self.assertIsInstance(manager.get('testsessionid'), Session)
        
    #----------------------------------------------------------------------
    def test_2_workpool(self):
        """"""
        def test(i):
            print('execute onece: {}'.format(i))
            return i
            
        def cb(re):
            print(re)
            
        def gcb(t, re):
            print('g:{}:{}'.format(t, re))
            
        threadpool.regist_global_result_callback(gcb)
        
        for i in range(100):
            threadpool.feed(test, args=(i,), enable_global_result_callback=True)
            
        for i in range(100):
            threadpool.feed(test, args=(i,), callback=cb, enable_global_result_callback=False)  
        
        
        time.sleep(2)
        threadpool.stop()
    

if __name__ == '__main__':
    unittest.main()