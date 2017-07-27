#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ThreadLabor
  Created: 07/18/17
"""
from Queue import Empty, Queue
import traceback
from uuid import uuid1
from threading import Thread

import zmq

from . import context

########################################################################
class ThreadLabor(Thread):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, result_sock_addr, error_sock_addr,
                 poll_interval=500, task_table={},
                 debug=False, task_queue=None):
        """Constructor"""
        self._name = 'Thread_labor-{}'.format(str(uuid1()))
        self._working_flag = True
        self._poll_interval = poll_interval
        self.debug = debug
        self._alive_flag = False
        self._buzy_flag = False
        
        Thread.__init__(self, name=self._name)
        
        #
        # set task queue
        #
        self.task_queue = Queue(1) if not task_queue else task_queue
        
        #
        # set result socket
        #
        self._push_result_sock = context.socket(zmq.PUSH)
        self._push_result_sock.connect(result_sock_addr)
        
        #
        # set error socket
        #
        self._push_error_sock = context.socket(zmq.PUSH)
        self._push_error_sock.connect(error_sock_addr)
        
    #----------------------------------------------------------------------
    def run(self):
        """"""
        #
        # set alive 
        #
        self._alive_flag = True
        
        #
        # main loop
        #
        while self._working_flag:
            try:
                _result = self.task_queue.get(block=False)
            except:
                self._buzy_flag = False
                continue                
            
            self._buzy_flag = True
            #
            # recv task
            #
            target, args, kw, task_id = _result
            
            result = {'task_id':task_id}
            
            try:
                _r = target(*args, **kw)
            except:
                _r = traceback.format_exc()
                if self.debug:
                    result['result'] = _r
                    #
                    # send exc info from error sock
                    #
                    self._push_error_sock.send_pyobj(result)
            
            result['result'] = _r
            #
            # send result back
            #
            self._push_result_sock.send_pyobj(result)
            
            #
            # finished task set it not buzy
            #
            self._buzy_flag = False
        
        self._buzy_flag = False
        self._alive_flag = False
            
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self._working_flag = False
    
    @property
    def alive(self):
        """"""
        return self._alive_flag
    
    @property
    def buzy(self):
        """"""
        return self._buzy_flag or (self.task_queue.qsize() == 1)
    
    #----------------------------------------------------------------------
    def feed(self, task):
        """"""
        self.task_queue.put(task)
        