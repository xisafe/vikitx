#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Message 
  Created: 07/31/17
"""

########################################################################
class _Msg(object):
    """Message only in exchanger
    
    Attributes:
    -----------
    id: str
        the id of msg
    
    routing_key: str
        the routing key for the current msg
    
    message: packet
        Message content"""
    
    def __init__(self, id, routing_key, message):
        """"""
        self._id = id
        self._rkey = routing_key
        self._message = message
        self._retry_count = 0


    @property
    def id(self):
        return self._id

    @property
    def token(self):
        """"""
        return self._id
    
    @property
    def routing_key(self):
        return self._rkey
    
    @property
    def message(self):
        return self._message
    
    @property
    def retry_count(self):
        """"""
        return self._retry_count
    
    
    #----------------------------------------------------------------------
    def retry(self):
        """"""
        self._retry_count = self._retry_count + 1
        
    
    def ack(self):
        self.finished()