#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: 
  Created: 08/01/17
"""

########################################################################
class Router(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, routing_key, port, sock):
        """Constructor"""
        self._rk = routing_key
        self._port = port
        self._sock = sock
    
    @property
    def routing_key(self):
        """"""
        return self.routing_key
    
    @property
    def port(self):
        """"""
        return self._port
    
    @property
    def socket(self):
        """"""
        return self._sock
        
        
    
    