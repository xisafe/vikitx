#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: clock
  Created: 07/21/17
"""

from collections import defaultdict
import Queue
from time import time
from ._utils import start_thread
from . import threadpool

########################################################################
class Clock(object):
    """"""

    #----------------------------------------------------------------------
    def __new__(self, *args, **kwargs):
        """"""
        if not hasattr(self, '_instance'):
            orig = super(Clock, self)
            self._instance = orig.__new__(self, *args, **kwargs)
        
        return self._instance

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self._working_flag = True
        
        self._tasks = defaultdict(dict)
        
        self._cache_queue = Queue.Queue()
        
        self.now = None
        self.pool = threadpool
        
        self.start()
    
    #----------------------------------------------------------------------
    def __looping(self):
        """"""
        def _peek_task(_id):
            if self._tasks.has_key(_id):
                pass
            else:
                return False
            
            try:
                _ts = self._tasks[_id].get('time')
                _itv = self._tasks[_id].get('interval')
            except KeyError as e:
                return False
            
            _flag = self.now > _ts
            if _flag:
                #
                # looping call
                #
                if _itv is not None:
                    try:
                        self._tasks[_id]['time'] = _ts + _itv
                    except KeyError:
                        return False
            
            return _flag
                
        self._working_flag = True
        while self._working_flag:
            
            #
            # set now
            #
            self.now = time()
            
            #
            # update cache
            #
            while self._cache_queue.qsize() > 0:
                _id, _info = self._cache_queue.get()
                self._tasks[_id] = _info
            
            for _id in filter(_peek_task, self._tasks.keys()):
                ctpl = self._tasks[_id].get('task')
                callback = self._tasks[_id].get('callback')
                if ctpl:
                    cp, v, kw = ctpl
                    
                    self.pool.feed(cp, v, kw,
                                   enable_global_result_callback=False,
                                   callback=callback)
                    
                    if self._tasks[_id].get('time') < self.now:
                        del self._tasks[_id]

    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        start_thread(name='clocking', 
                     daemon=True, 
                     target=self.__looping, args=(), kw={})
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self._working_flag = False
    
    #----------------------------------------------------------------------
    def regist_task(self, id, time, target, v=(), kw={}, interval=None, 
                    callback=None):
        """"""
        #
        # regist task
        #
        _ = {}
        
        _['time'] = time
        _['task'] = (target, v, kw)
        _['interval'] = interval
        _['callback'] = callback
        
        self._cache_queue.put((id, _))
    
    #----------------------------------------------------------------------
    def cancel_task(self, id):
        """"""
        del self._tasks[id]

        

clock = Clock()