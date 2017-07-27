#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Defination
  Created: 07/26/17
"""

import zmq
import threading
import multiprocessing
from multiprocessing import Pipe, Queue
from Queue import Empty
import time

from .. import interfaces
from . import get_new_threadpool

#
# define states
#
state_INIT = 'init'
state_WORKING = 'working'
state_END = 'end'

########################################################################
class FakePipe:
    """"""

    #----------------------------------------------------------------------
    def send(self, *args, **kw):
        """"""
    
    #----------------------------------------------------------------------
    def recv(self):
        """"""
    
    #----------------------------------------------------------------------
    def poll(self):
        """"""
        return False
        
    
    

########################################################################
class _Service(interfaces.ServiceIf, interfaces.ExecuteTaskIf, interfaces.EntityIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, target, task_pipe=None, result_pipe=None):
        """"""
        self._id = id
        self._state = state_INIT
        
        self.task_pipe = task_pipe if task_pipe else FakePipe()
        self.result_pipe = result_pipe if result_pipe else FakePipe()
        
        self._consume_result, self._produce_result = Pipe(False)
        
        #
        # setting target
        #
        assert callable(target)
        self.target = target
        
        #
        # send buffer
        #
        self._task_queue = Queue()
    
    #----------------------------------------------------------------------
    def _init_pool(self):
        """"""
        #
        # set threadpool
        #
        pool = get_new_threadpool("{}-threadpool".format(self._id),
                                       min_threads=1,
                                       max_threads=30,
                                       debug=True)
        #self.pool.regist_global_result_callback(self.result_callback)
        pool.start()
        
        return pool
    
    @property
    def id(self):
        """"""
        return self._id

    @property
    def state(self):
        """"""
        return self._state
    
    @state.setter
    def state(self, value):
        """"""
        self._state = value
        
    #----------------------------------------------------------------------
    def run(self):
        """"""
        #
        # build pool
        #
        pool = self._init_pool()
        
        #
        # set working
        #
        self.state = state_WORKING

        #
        # entry mainloop
        #
        self.__mainloop(pool)    

        
    #----------------------------------------------------------------------
    def __mainloop(self, pool):
        """"""
        while self.state == state_WORKING:

            if self.task_pipe.poll():
                _task = self.task_pipe.recv()
                self.execute(*_task)
            
            self.consume(pool)
    
    #----------------------------------------------------------------------
    def execute(self, task_id, args=(), kwargs={}):
        """"""
        self._task_queue.put((task_id, args, kwargs))
    
    #----------------------------------------------------------------------
    def consume(self, pool):
        """"""
        try:
            #
            # feed
            #
            task_id, args, kwargs = self._task_queue.get()
            pool.feed(self.target, args, kwargs, task_id=task_id,
                      callback=self.__result_callback, 
                      enable_global_result_callback=False)
        except Empty:
            pass
    
        return 
    
    #----------------------------------------------------------------------
    def __result_callback(self, task_id, result):
        """"""
        #
        # system callback
        #
        self.result_callback(task_id, result)
        
        #
        # result send back to servicenode 
        #
        self.result_pipe.send((task_id, result))
    
    #----------------------------------------------------------------------
    def result_callback(self, task_id, result):
        """"""
        #print('default result callback if calling! ' + \
              #'task_id:{} result:{}'.format(task_id, result))
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.state = state_END
        
        
        
        
########################################################################
class ServiceWraperInThread(_Service, threading.Thread):
    """"""

    def __init__(self, id, target, task_pipe=None, result_pipe=None, daemon=True):
        """Constructor"""
        #
        # init service
        #
        _Service.__init__(self, id, target, task_pipe, result_pipe)
        
        #
        # init Thread
        #
        threading.Thread.__init__(self, name=id)
        self.daemon = True

        
        
########################################################################
class ServiceWraperInProcess(_Service, multiprocessing.Process):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, target, task_pipe=None, result_pipe=None, daemon=True):
        """Constructor"""
        #
        # init service
        #
        _Service.__init__(self, id, target, task_pipe, result_pipe)
        
        #
        # init Process
        #
        multiprocessing.Process.__init__(self, name=id)
        self.daemon = True
        
