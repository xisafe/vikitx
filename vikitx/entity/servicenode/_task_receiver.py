#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Task Receiver
  Created: 08/02/17
"""

from .. import zed

########################################################################
class TaskReceiver(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, context):
        """"""
        self._context = context
        
        self._tables = {}
    
    #----------------------------------------------------------------------
    def regist_receiver(self, index, host, router_port, ack_port):
        """"""
        comsumer = zed.ZConsumer(host, router_port, ack_port, self._context)
        self._tables[index] = comsumer
    
    