#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Action
  Created: 08/03/17
"""

from uuid import uuid1

#----------------------------------------------------------------------
def getuuid1():
    """"""
    return str(uuid1())


########################################################################
class TokenBase(object):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        self._token = getuuid1()
        
    @property
    def token(self):
        """"""
        return self._token


########################################################################
class ActionStartService(TokenBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, mod_type, routing_key=None):
        """Constructor"""
        TokenBase.__init__(self)
        
        self._id = id if id else self.token
        self._mod_type = mod_type
        self._routing_key = routing_key if routing_key else self._mod_type
    
    @property
    def mod_type(self):
        """"""
        return self._mod_type
    
    @property
    def routing_key(self):
        """"""
        return self._routing_key
        
    @property
    def id(self):
        """"""
        return self._id
        
        
    
    

    
    
    