#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: AckPool
  Created: 07/18/17
"""

from uuid import uuid1
import time

from ._task import AckTask
from ..workpool import threadpool
from ..workpool._utils import start_thread


########################################################################
class Ackpool(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._common_callback = None
        self._timeout_callback = None
        
        self._working_flag = True
        
        self._tasks = {}
        
    #----------------------------------------------------------------------
    def _main_loop(self):
        """"""
        self._working_flag = True 
        
        #
        # filter task
        #
        def peek_tasks(task):
            if time.time() <= task.next_time:
                return True
            else:
                return False
        
        while self._working_flag:
            for _task in filter(peek_tasks, self._tasks.values()):
                
                #
                # handle timeout
                #
                if _task.timeout:
                    del self._tasks[_task.id]
                    continue
                
                threadpool.feed(_task.execute, 
                                enable_global_result_callback=False)
        
    #----------------------------------------------------------------------
    def regist_send_callback(self, callback):
        """"""
        assert callable(callback)
    
        self._common_callback = callback
    
    #----------------------------------------------------------------------
    def regist_timeout_callback(self, callback):
        """Set the timeout callback
        
        The callback should have 2 params: 1. the packet;
            2. A tuple contains: start time and timeout timestamp"""
        assert callable(callback)
        
        self._timeout_callback = callback
    
    #----------------------------------------------------------------------
    def add(self, token, packet, interval=5, count=3):
        """"""
        new_task = AckTask(id, self._common_callback, args=(packet, ),
                           loop_interval=interval, count=count)
        
        self._tasks[id] = new_task
    
    #----------------------------------------------------------------------
    def ack(self, token):
        """"""
        while True:
            try:
                del self._tasks[token]
            except:
                pass
            
            if not self._tasks.has_key(token):
                break

    #----------------------------------------------------------------------
    def resend(self, token):
        """"""
        assert self._tasks.has_key(token)
        
        task = self._tasks.get(token)
        if task:
            task.resend()
            
    #----------------------------------------------------------------------
    def reset(self, token):
        """"""
        assert self._tasks.has_key(token)
        
        task = self._tasks.get(token)
        if task:
            task.reset()        
        
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self._working_flag = False
        
    #----------------------------------------------------------------------
    def start(self):
        """"""
        self._working_flag = True
        
        #
        # start main loop
        #
        start_thread('ackpool-{}'.format(str(uuid1())), True,
                     self._main_loop)
    
    