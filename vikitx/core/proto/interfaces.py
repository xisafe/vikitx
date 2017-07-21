#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Protocol Interface
  Created: 07/19/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty


########################################################################
class IdentifyIf(object):
    """"""
    
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        """"""
    
    

########################################################################
class SendIf(object):
    """"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self):
        """"""
        
########################################################################
class SendToIf(object):
    """"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def sendto(self):
        """"""
        
########################################################################
class StateIf(object):
    """"""
    
    __metaclass__ = ABCMeta

    @abstractproperty
    def state(self):
        """"""
    

########################################################################
class ServerIf(SendToIf, StateIf, IdentifyIf):
    """"""
    
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def state(self):
        """"""

########################################################################
class ClientIf(SendIf, StateIf, IdentifyIf):
    """"""

    __metaclass__ = ABCMeta
    
    @abstractproperty
    def connect(self):
        """"""
        
    
    
    