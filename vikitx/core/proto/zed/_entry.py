#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Entry
  Created: 08/01/17
"""

########################################################################
class Entry(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, port, sock):
        """Constructor"""
        
        self._port = port
        self._sock = sock
    
    @property
    def socket(self):
        """"""
        return self._sock
    
    @property
    def port(self):
        """"""
        return self._port
    
    