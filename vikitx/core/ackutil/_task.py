#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ACK Task
  Created: 07/19/17
"""

import time

########################################################################
class AckTask(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, callback, args=(), kw={}, loop_interval=5, count=3):
        """Constructor"""
        
        self.id = id
        
        self._timeout_flag = False
        
        self._interval = loop_interval
        self._count = count
        
        self.reset()
        
        #
        # callback setting
        #
        self._cb = callback
        self._vs = args
        self._kw = kw
        
        #
        # packet
        #
        self.packet = args[0]
    
    #----------------------------------------------------------------------
    def next(self):
        """"""
        
        if self.timeout:
            return 
        
        self._next_ts = self._next_ts + self._interval
        print('now:{} next:{}'.format(time.time(), self.next_time))
        if self._next_ts > self._final_ts:
            self._timeout_flag = True
    
    @property
    def first_time(self):
        """"""
        return self._start_ts
        
    @property
    def next_time(self):
        """"""
        return self._next_ts
    
    @property
    def final_time(self):
        """"""
        return self._final_ts
        
    @property
    def timeout(self):
        """"""
        return self._timeout_flag
    
    #----------------------------------------------------------------------
    def execute(self):
        """"""
        if self.timeout:
            return
        
        self.next()
        
        self.just_execute()
        
        
    
    #----------------------------------------------------------------------
    def just_execute(self):
        """"""
        #
        # do sth
        #
        self._cb(*self._vs, **self._kw)        
    
    #----------------------------------------------------------------------
    def resend(self):
        """"""
        return self.just_execute()
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        self._start_ts = time.time()
        self._next_ts = self._start_ts
        self._final_ts = self._start_ts + self._interval * self._count
        
        self.next()