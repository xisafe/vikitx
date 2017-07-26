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
        return self._id
    
    @id.setter
    def id(self, value):
        """"""
        self._id = value
    

########################################################################
class SignalBase(ZSRPSPacketIf):
    """"""

########################################################################
class DataBase(ZSRPSPacketIf):
    """"""


#
# shake hands
#
########################################################################
class Negotiation(SignalBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, pub_addr, rep_addr, negotiation_lease):
        """Constructor"""
        self.pub_addr = pub_addr
        self.rep_addr = rep_addr
        self.negotiation_lease = negotiation_lease

########################################################################
class NegotiationResponse(SignalBase):
    """"""

#
# heartbeat
#
########################################################################
class Hearbeat(SignalBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, client_id):
        """Constructor"""
        self._id = client_id
        
    @property
    def id(self):
        """"""
        return self._id
        
########################################################################
class LastHeartbeat(Hearbeat):
    """"""
    
    

#
# pair to pair
#
########################################################################
class Established(SignalBase):
    """"""
    pass

########################################################################
class Ack(SignalBase):
    """"""
    

#
# reset or reject
#
########################################################################
class Reset(SignalBase):
    """"""

    pass
    
    
        
        
    
    

    
        
        
    
    
    
    
    