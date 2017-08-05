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
        
        self._socket_map_comsumer = {}
    
    #----------------------------------------------------------------------
    def regist_receiver(self, host, router_port, ack_port):
        """"""
        comsumer = zed.ZConsumer(host, router_port, ack_port, self._context)
        self._tables[comsumer.router_socket] = comsumer
    
    