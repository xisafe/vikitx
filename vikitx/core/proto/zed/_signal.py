#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Signal
  Created: 08/01/17
"""

########################################################################
class SignalBase(object):
    """"""


########################################################################
class Ack(SignalBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, token):
        """Constructor"""
        self._token = token
        
    @property
    def id(self):
        """"""
        return self._token
    
    @property
    def token(self):
        """"""
        return self._token
    
    
########################################################################
class Failed(SignalBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, token):
        """Constructor"""
        self._token = token
        
    @property
    def id(self):
        """"""
        return self._token
    
    @property
    def token(self):
        """"""
        return self._token
        
    
    
        
    
    