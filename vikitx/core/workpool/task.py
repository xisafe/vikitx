#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Task
  Created: 07/21/17
"""

import time
import uuid

from . import threadpool
from ._clocks import clock

########################################################################
class Task(object):
    """Basic Task
    
    Attributes
    ----------
    callback: function
        Task core function
    *args: var_args
    **keyword: keyword_args
    
    """

    #----------------------------------------------------------------------
    def __init__(self, callback, *args, **keyword):
        """Constructor"""
        
        
        self._callback = callback
        self._args = args
        self._keyword = keyword
        
        self.pool = threadpool

    #----------------------------------------------------------------------
    def execute(self):
        """"""
        self.pool.feed(self._callback, self._args, self._keyword,
                       enable_global_result_callback=False)
    
    #----------------------------------------------------------------------
    def regist_threadpool(self, pool):
        """"""
        self.pool = pool
    
    #----------------------------------------------------------------------
    def call_later(self, interval):
        """"""
        _time = time.time() + interval
        
        self._id = str(uuid.uuid1())
        clock.regist_task(id=self._id, 
                          time=_time, 
                          target=self._callback,
                          v=self._args,
                          kw=self._keyword)
        
        return
    
    #----------------------------------------------------------------------
    def cancel(self):
        """"""
        clock.cancel_task(self._id)
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.cancel()
        
        
########################################################################
class LoopingCall(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, callback, *args, **keyword):
        """Constructor"""
        
        self._callback = callback
        self._args = args
        self._keyword = keyword
        
        self.pool = threadpool
    
    #----------------------------------------------------------------------
    def regist_threadpool(self, pool):
        """"""
        self.pool = pool
        
    #----------------------------------------------------------------------
    def start(self, interval, first=True):
        """"""
        _time = time.time()
        
        if self.running:
            raise Exception('this task:{} is running!'.format(self._id))
        
        self._id = str(uuid.uuid1())
        clock.regist_task(self._id,
                          _time,
                          self._callback,
                          self._args,
                          self._keyword,
                          interval)
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.cancel()
        
    #----------------------------------------------------------------------
    def cancel(self):
        """"""
        clock.cancel_task(self._id)
        
        del self._id
    
    @property    
    def running(self):
        """"""
        return hasattr(self, '_id')
        
        
    