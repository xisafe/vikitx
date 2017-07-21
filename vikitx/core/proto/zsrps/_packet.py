#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Packet And Signal
  Created: 07/21/17
"""

from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod, abstractproperty
from uuid import uuid1

########################################################################
class ZSRPSPacketIf(object):
    """"""
    
    @property
    def token(self):
        """"""
        if hasattr(self, '_token'):
            pass
        else:
            self._token = str(uuid1())
        
        return self._token
    
    @property
    def id(self):
        """"""
        pass
    
    @id.setter
    def id(self, value):
        """"""
        self._client_id = value
    

########################################################################
class SignalBase(ZSRPSPacketIf):
    """"""

########################################################################
class DataBase(ZSRPSPacketIf):
    """"""


########################################################################
class Negotiation(SignalBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, pub_addr, rep_addr, negtiation_lease):
        """Constructor"""
        self.pub_addr = pub_addr
        self.rep_addr = rep_addr
        self.negtiation_lease = negtiation_lease

########################################################################
class NegotiationResponse(SignalBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

########################################################################
class Established(SignalBase):
    """"""
    pass
        
        
    
    

    
        
        
    
    
    
    
    