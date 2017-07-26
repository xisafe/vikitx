#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test For Workflow
  Created: 07/24/17
"""

import unittest

from vikitx.core.workflow import Workflow

########################################################################
class TestWorkflow(Workflow):
    """"""
    
    state_START = 'start'
    state_END = 'end'
    state_WORKING = 'working'

    _TRANS_TABLE = {
        state_START: [state_WORKING, state_END],
        state_WORKING: [state_END]
    }
    
    @property
    def START_STATE(self):
        """"""
        return self.state_START
    
    @property
    def TRANS_TABLE(self):
        """"""
        return self._TRANS_TABLE
    
    #----------------------------------------------------------------------
    def handle_packet(self, packet):
        """"""
        #
        # if the id is the workflow, the packet will be send to this method
        #
        if self.state == self.state_START:
            self.handle_pkt_when_start(packet)
        elif self.state == self.state_END:
            self.handle_pkt_when_end(packet)
        elif self.state == self.state_WORKING:
            self.handle_pkt_when_working(packet)
    
    #----------------------------------------------------------------------
    def handle_pkt_when_start(self, pkt):
        """"""
        self.state = self.state_WORKING
        print('trans to working state')
    
    #----------------------------------------------------------------------
    def handle_pkt_when_working(self, pkt):
        """"""
        if not hasattr(self, '_count'):
            self._count = 1
        else:
            self._count = self._count + 1
            
        if self._count == 5:
            self.state = self.state_END
            print('working END')
    
    #----------------------------------------------------------------------
    def handle_pkt_when_end(self, pkt):
        """"""
        print('END!')
        
        
        
    
    

########################################################################
class WorkflowTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_workflow(self):
        """"""
        twf = TestWorkflow()
        print(twf.state)
        self.assertEqual(twf.state, 'start')
        twf.handle_packet('test')
        self.assertEqual(twf.state, 'working')
        twf.handle_packet('testtt')
        twf.handle_packet('testtt')
        twf.handle_packet('testtt')
        twf.handle_packet('testtt')
        twf.handle_packet('testtt')
        twf.handle_packet('testtt')
        self.assertEqual(twf.state, 'end')
        
    

if __name__ == '__main__':
    unittest.main()