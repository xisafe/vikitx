#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Vikitx
  Created: 07/16/17
"""

import unittest

from vikitx.core.session import Session, SessionManager
#from vikitx.core.workflow import Workflow
from vikitx.core.channel import TCPChannelREQ, TCPChannelREP

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
    def test_2_channel(self):
        """"""
        channel2 = TCPChannelREP(port='4443', id='B')
        channel1 = TCPChannelREQ(addr='tcp://127.0.0.1:4443', id='A')
        channel1.send(to='B', msg='testmessage')
        self.assertEqual(channel2.recv()[0], 'B')

        
        channel3 = TCPChannelREQ(addr='tcp://127.0.0.1:4443', id='C')
        channel3.send(to='B', msg='testest')
    
        
        channel2.send('dsfsdf')
        channel2.send('dsfsdf')
        
        print(channel1.recv())
        print(channel3.recv())    
    

if __name__ == '__main__':
    unittest.main()