#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ThreadPool test
  Created: 07/18/17
"""

import zmq

context = zmq.Context()

from ._pool import ThreadPool as _ThreadPool
from ._tlabor import ThreadLabor as _ThreadLabor

threadpool = _ThreadPool()
threadpool.start()

#----------------------------------------------------------------------
def get_new_threadpool(id=None, min_threads=3, max_threads=20, debug=False, 
                       poll_interval=500):
    """"""
    return _ThreadPool(id, min_threads, max_threads, debug, poll_interval)