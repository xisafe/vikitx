#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Ackpool
  Created: 08/01/17
"""

import warnings

from .. import Ackpool as _Ackpool

########################################################################
class Ackpool(object):
    """The ackpool need 3 params
    
    Attributes:
    -----------
    ack_timeout: int
        the ack interval
    
    cout: int
        max count for calling a single ack task
    
    timeout_callback: function
        the timeout_callback has 2 parameters: 1st, the token for packet; 
        2nd, the packet object
    
    """

    #----------------------------------------------------------------------
    def __init__(self, ack_timeout=10, count=3, timeout_callback=None):
        """Constructor"""
        
        self._ack_timeout = ack_timeout
        self._count = count
        
        self.pool = _Ackpool()
        self.pool.start()
        
        self._timeout_callback = timeout_callback if timeout_callback \
            else self.timeout_callback
    
    @property    
    def ack_timeout(self):
        """"""
        return self._ack_timeout
    
    @property
    def count(self):
        """"""
        return self._count
    
    #----------------------------------------------------------------------
    def add(self, token, callback, args=tuple(), kw={}):
        """"""
        self.pool.add(token, packet=args[0], 
                      interval=self.ack_timeout, count=self.count, 
                      send_callback=callback)
    
    #----------------------------------------------------------------------
    def ack(self, token):
        """"""
        self.pool.ack(token)
    
    #----------------------------------------------------------------------
    def timeout_callback(self, pkt):
        """"""
        if self._timeout_callback:
            self._timeout_callback(pkt.token, pkt)
        else:
            warnings.warn('the packet is timeout, but no timeout_callback called!')
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.pool.stop()