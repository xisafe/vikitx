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
from Queue import Queue

from . import context
from . import _tlabor
from . import _excs
from . import _utils

STATE_PREPARED = 'prepared'
STATE_RUNNING = 'running'
STATE_FINISHING = 'finishing'
STATE_END = 'end'

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
    
    @abc.abstractmethod
    def adjust(self):
        """"""
    
    @abc.abstractmethod
    def shrink(self):
        """"""
        
        
    

########################################################################
class ThreadPool(PoolBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id=None, min_threads=3, max_threads=20,
                 debug=False, poll_interval=500):
        """Constructor"""
        self._id = id if id else str(uuid.uuid1())
        
        #
        # sock address
        #
        self._task_queue = Queue()
        self._result_addr = 'inproc://{}-result'.format(self._id)
        self._error_addr = 'inproc://{}-error'.format(self._id)
        
        self._pull_result_sock = context.socket(zmq.PULL)
        self._pull_result_sock.bind(self._result_addr)
        
        self._pull_error_sock = context.socket(zmq.PULL)
        self._pull_error_sock.bind(self._error_addr)
        
        #
        # poller
        #
        self._poller = zmq.Poller()
        self._poller.register(self._pull_error_sock, flags=zmq.POLLIN)
        self._poller.register(self._pull_result_sock, flags=zmq.POLLIN)
        
        #
        # cache threads
        #
        self._threads = []
        
        #
        # threadpool attrs
        #
        self._min = min_threads
        self._max = max_threads
        
        #
        # state flag
        #
        self._state = STATE_PREPARED
        
        #
        # debug
        #
        self.debug = debug
        
        self.poll_interval = poll_interval
        
        #
        # registed callback
        #
        self._registed_callback = {}
        
        #
        # global callback
        #
        self.global_result_calbacks = []
        self.global_error_calbacks = []
        
        self._nogcache_list = []
    
    @property    
    def thread_count(self):
        """"""
        return len(self._threads)
    
    @property
    def state(self):
        """"""
        return self._state
    
    @property
    def buzy(self):
        """"""
        if 0 < len([i for i in self._threads if not i.buzy]):
            return False
        else:
            return True
    
    #----------------------------------------------------------------------
    def feed(self, target, args=(), keywords={}, callback=None,
             task_id=None, new_labor=False, enable_global_result_callback=True):
        """"""
        task_id = str(uuid.uuid1())
        if self.state == STATE_RUNNING:
            if self.thread_count < self._max and self.buzy:
                self.start_new_labor()
            else:
                if new_labor:
                    self.start_new_labor()
            
            self._task_queue.put(self._gen_task(
                target,
                args,
                keywords,
                task_id=task_id,
                callback=callback,
                enable_global_result_callback=enable_global_result_callback
            ))
        else:
            raise _excs.PoolError('may be you should start pool first')
    
    #----------------------------------------------------------------------
    def start(self):
        """Start Threadpool"""
        assert self.state == STATE_PREPARED, 'state error'
        self._state = STATE_RUNNING
        
        _utils.start_thread('thread_pool:{}-mainloop', daemon=True,
                            target=self.main_loop)
    
    #----------------------------------------------------------------------
    def _gen_task(self, target, args=(), keywords={}, callback=None, 
                  task_id=None, new_labor=False, enable_global_result_callback=True):
        """"""
        #
        # regist callback or not
        #
        if callback:
            assert callable(callback)
            if not self._registed_callback.has_key(task_id):
                self._registed_callback[task_id] = {}
            self._registed_callback[task_id]['callback'] = callback
            self._registed_callback[task_id]['enable_global_callback'] = enable_global_result_callback
        else:
            if enable_global_result_callback:
                pass
            else:
                self._nogcache_list.append(task_id)
        
        return (target, args, keywords, task_id)
        
    #----------------------------------------------------------------------
    def main_loop(self):
        """"""
        while self.state == STATE_RUNNING:
            #
            # poll and handle result
            #
            for i in self._poller.poll(self.poll_interval):
                if i[0] is self._pull_error_sock:
                    self.handle_error_for_task(self._pull_error_sock.recv_pyojb())
                elif i[0] is self._pull_result_sock:
                    self.finish_task(self._pull_result_sock.recv_pyobj())
            
            self.shrink()
        
    
    #----------------------------------------------------------------------
    def start_new_labor(self):
        """Start new labor"""
        th = _tlabor.ThreadLabor(self._task_queue, self._result_addr, 
                                 self._error_addr, debug=self.debug)
        th.daemon = True
        th.start()
        
        self._threads.append(th)
        
        return th
    
    #----------------------------------------------------------------------
    def finish_task(self, result):
        """"""
        task_id = result.get('task_id')
        if task_id:
            _r = result.get('result')
            
            _r_callback = self._registed_callback.get(task_id)
            if _r_callback:
                self.feed(_r_callback['callback'], args=(_r,), enable_global_result_callback=False)
                del self._registed_callback[task_id]
                
                if _r_callback['enable_global_callback']:
                    for i in self.global_result_calbacks:
                        i(task_id, _r)
            else:
                if task_id in self._nogcache_list:
                    self._nogcache_list.remove(task_id)
                else:
                    for i in self.global_result_calbacks:
                        i(task_id, _r)                
    
    #----------------------------------------------------------------------
    def handle_error_for_task(self, result):
        """"""
        task_id = result.get('task_id')
        if task_id:
            _e = result.get('result')
            
            if self.global_error_calbacks == []:
                print(_e)
            else:
                for i in self.global_error_calbacks:
                    i(_e)
        
    
    #----------------------------------------------------------------------
    def adjust(self, min_labor=None, max_labor=None):
        """Adjuest the size of threadpool
        
        Params:
        -------
        min_labor: int
          the min size of pool
          
        max_labor: int
          the max size of pool
        
        Returns:
        --------
          None
          
        """
        _min = min_labor if min_labor else self._min
        _max = max_labor if max_labor else self._max
        
        assert int(_min) <= int(_max)
        
        self._max = _max
        self._min = _min
    
    #----------------------------------------------------------------------
    def shrink(self):
        """Shrink idle labor"""
        for _idle_labor in [i for i in self._threads if not i.buzy]:
            _idle_labor.stop()
            self._threads.remove(_idle_labor)
    
    #----------------------------------------------------------------------
    def regist_global_result_callback(self, callback):
        """Regist global result callback
        
        Params:
        --------
        callback: function
          callback should have 2 params at least, the first is task_id:str, 
          the second is the 'result'."""
        
        assert callable(callback)
        
        self.global_result_calbacks.append(callback)
    
    #----------------------------------------------------------------------
    def clear_global_result_callbacks(self):
        """"""
        self.global_result_calbacks = []
        
    #----------------------------------------------------------------------
    def regist_global_error_callback(self, callback):
        """Regist global error callback
        
        Params:
        --------
        callback: function
          callback should have 2 params at least, the first is task_id:str, 
          the second is the 'exception'."""
        
        assert callable(callback)
        
        self.global_result_calbacks.append(callback)
    
    #----------------------------------------------------------------------
    def clear_global_error_callbacks(self):
        """"""
        self.global_error_calbacks = []
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        assert self._state == STATE_RUNNING
        self._state = STATE_FINISHING
            
        def stop_labor(labor):
            labor.stop()
            while labor.alive:
                pass
        
        map(stop_labor, self._threads)
        
        self._threads = []
        
        self._state = STATE_END
            