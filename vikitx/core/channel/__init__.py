#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Channel Define
  Created: 07/16/17
"""

from zmq import Context

DEFAULT_CONTEXT = Context()
context = DEFAULT_CONTEXT

#----------------------------------------------------------------------
def get_new_context(io_thread=1, **config):
    """"""
    return Context(io_thread, **config)

from ._tcpchannel import TCPChannelREQ, TCPChannelREP

