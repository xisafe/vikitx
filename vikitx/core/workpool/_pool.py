#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Workpool
  Created: 07/17/17
"""

import zmq
import abc
import uuid

from ..channel import context
from . import _tlabor


########################################################################
class PoolBase(object):
    """"""

    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def feed(self):
        """"""
    
    @abc.abstractmethod
    def start(self):
        """"""
    
    @abc.abstractmethod
    def stop(self):
        """"""
        
    

########################################################################
class ThreadPool(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id=None):
        """Constructor"""
        self._id = id if id else str(uuid.uuid1())
        
        
        self.ctx = context
        self.push_sock = ctx.socket(zmq.PUSH)
        self.push_sock.bind()
        self.result_pull = ctx.socket(zmq.PULL)
        
    #----------------------------------------------------------------------
    def feed(self, task_id, target, args=(), keywords={}, callback=None):
        """"""
        
    