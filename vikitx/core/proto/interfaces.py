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
    
    @abstractmethod
    def send_action(self, to, action):
        """"""    

########################################################################
class ClientIf(SendIf, StateIf, IdentifyIf):
    """"""

    __metaclass__ = ABCMeta
    
    @abstractproperty
    def connect(self):
        """"""
        
    
########################################################################
class UserClientIf(object):
    """"""
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_action(self, action):
        """"""
        pass

########################################################################
class UserClientManageIf(object):
    """"""

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_available_clients(self):
        """Return all id(s) in clients"""
    
    @abstractmethod
    def remove_client(self, client_id):
        """"""
    
    @abstractmethod
    def get_client_scope(self, client_id):
        """"""
        
        
        
        
    
    
        
        
    
    
    