#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: TCP Chennal
  Created: 07/16/17
"""

import zmq

from ._base import ChannelIf

from . import context

########################################################################
class TCPChannelREQ(ChannelIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, addr, id):
        """Constructor"""
        
        self.sock = context.socket(zmq.REQ)
        self.sock.connect(addr)
    
    #----------------------------------------------------------------------
    def send(self, to, msg):
        """"""
        self.sock.send_pyobj({'to':to,
                              'msg':msg})
    
    #----------------------------------------------------------------------
    def recv(self):
        """"""
        return self.sock.recv_pyobj()
    
    #----------------------------------------------------------------------
    def poll(self, timeout=None):
        """"""
        return self.sock.poll(timeout)

    
########################################################################
class TCPChannelREP(ChannelIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, port, id):
        """Constructor"""
        self.sock = context.socket(zmq.REP)
        self.sock.bind('tcp://*:{}'.format(port))
    
    #----------------------------------------------------------------------
    def poll(self, timeout):
        """"""
        return self.sock.poll(timeout)
    
    #----------------------------------------------------------------------
    def send(self, msg):
        """"""
        self.sock.send_pyobj(msg)
        
    #----------------------------------------------------------------------
    def recv(self):
        """"""
        _recvd_obj = self.sock.recv_pyobj()
        
        return _recvd_obj.get('to'), _recvd_obj.get('msg')
        
        
    
    
    
    