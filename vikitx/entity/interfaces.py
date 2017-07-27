#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Basic Function Interface For Entity
  Created: 07/26/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

########################################################################
class EntityIf:
    """"""
    
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        """"""
    
        
    
    

########################################################################
class ServiceManageIf(object):
    """Define Interface to Control Service
    
    Methos:
    -------
    start_service(service_id, config):
        start service you can choose start this service \
        in a new process or thread
    
    stop_service(service_id):
        normal stop the service
    
    destory_service(service_id)
        destory the service(For service in process)
    
    sendto(service_id, packet)
        send a message(pkt) to service_id"""
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def start_service(self):
        """"""
    
    @abstractmethod
    def stop_service(self):
        """"""
    
    @abstractmethod
    def destory_service(self):
        """"""
    

########################################################################
class ServiceIf(object):
    """Service Basic Interfaces
    
    Methods:
    --------
    run():
        start the service in process or thread.
        
    stop():
        normal stop current service
        
    recv(): pkt
        recv packet from service node 
    
    """

    #
    # note: main loop
    #
    @abstractmethod
    def run(self):
        """"""
    
    #
    # shutdown: a interface to shutdown (not stop)
    #
    @abstractmethod
    def shutdown(self):
        """"""
        
    @abstractmethod
    def recv(self):
        """"""

########################################################################
class ExecuteTaskIf():
    """"""

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def execute(self):
        """"""
        
        
    @abstractmethod
    def result_callback(self, task_id, result):
        """"""
        
    
        
        