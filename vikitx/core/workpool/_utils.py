#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ThreadUtils
  Created: 07/18/17
"""

from threading import Thread

#----------------------------------------------------------------------
def start_thread(name, daemon, target, args=(), kw={}):
    """"""
    assert callable(target)
    
    _r = Thread(name=name, target=target, args=args, kwargs=kw)
    _r.daemon = True
    _r.start()
    
    return _r