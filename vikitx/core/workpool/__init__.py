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