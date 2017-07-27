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
from multiprocessing import Queue
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
class _Service(interfaces.ServiceIf, interfaces.ExecuteTaskIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, target, comm_addr=None):
        """"""
        self._id = id
        self._state = state_INIT
        
        self.ch_addr = comm_addr
        if self.ch_addr:
            self.context = zmq.Context()
            self.ch = self.context.socket(zmq.PAIR)
        else:
            self.ch = None
        
        #
        # setting target
        #
        assert callable(target)
        self.target = target
        
        #
        # send buffer
        #
        self._buffer_queue = Queue()
        self._task_queue = Queue()
        
        #
        # set threadpool
        #
        self.pool = get_new_threadpool("{}-threadpool".format(self._id),
                                       min_threads=1,
                                       max_threads=30)
        self.pool.regist_global_result_callback(self.result_callback)
        self.pool.start()
    
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
        self.state = state_WORKING
        #
        # if self.ch 
        #   execute with no chennal
        #
        print('Prepared to entry main loop')
        if self.ch:
            self.__channel_mainloop()
        else:
            self.__no_channal_mainloop()
        
        if self.ch:
            del self.ch
            
        print('Failed in mainloop')
        
    #----------------------------------------------------------------------
    def __channel_mainloop(self):
        """"""
        while self.state == state_WORKING:
            #
            # pick task up
            #
            flags = self.ch.poll(0, flags=zmq.POLLIN)
            if flags & zmq.POLLIN:
                execute_params = self.ch.recv_pyobj()
                self.execute(*execute_params)
            
            if flags & zmq.POLLOUT:
                while self._buffer_queue.qsize():
                    self.ch.send_pyobj(self._buffer_queue.get())
            
            self.consume()
            
    
    #----------------------------------------------------------------------
    def __no_channal_mainloop(self):
        """"""
        while self.state == state_WORKING:
            self.consume()
    
    #----------------------------------------------------------------------
    def execute(self, task_id, args=(), kwargs={}):
        """"""
        self._task_queue.put((task_id, args, kwargs))
    
    #----------------------------------------------------------------------
    def consume(self):
        """"""
        try:
            #
            # feed
            #
            task_id, args, kwargs = self._task_queue.get()
            self.pool.feed(self.target, args, kwargs, task_id=task_id,
                           enable_global_result_callback=True)
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
        # result send back to _buffer_queue (if self.ch)
        #
        if self.ch: 
            self._buffer_queue.put((task_id, result))
    
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

    #----------------------------------------------------------------------
    def __init__(self, id, target, comm_addr=None, daemon=True):
        """Constructor"""
        #
        # init service
        #
        _Service.__init__(self, id, target, comm_addr)
        #
        # init Thread
        #
        threading.Thread.__init__(self, name=id)
        self.daemon = True

        
        
########################################################################
class ServiceWraperInProcess(_Service, multiprocessing.Process):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, target, comm_addr=None, daemon=True):
        """Constructor"""
        #
        # init service
        #
        _Service.__init__(self, id, target, comm_addr)
        
        #
        # init Process
        #
        multiprocessing.Process.__init__(self, name=id)
        self.daemon = True
        
