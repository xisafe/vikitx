#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Enxer
  Created: 08/08/17
"""

from .. import thread_utils
from . import ZConsumer, ZProducer

########################################################################
class Enxer(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, host, ack_backend_port=3424):
        """Constructor"""
        
        self._host = host
        self._ack_backend_port = ack_backend_port
        
        self._working_flag = False
        
    
    #----------------------------------------------------------------------
    def _mainloop(self):
        """"""
        self._working_flag = True
        while self._working_flag:
            for sock, flag in self.poller.poll(timeout=0):
                
    
    