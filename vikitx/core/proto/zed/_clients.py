#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: 
  Created: 08/01/17
"""

import zmq
import abc
import warnings

from ._signal import Ack, Failed

########################################################################
class _ClientIf(object):
    """"""
    
    

########################################################################
class ZProducer(_ClientIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, host, target_port, context=None):
        """Constructor"""
        self._target_port = int(target_port)
        self._host = host
        
        self.context = context if context else zmq.Context()
        assert isinstance(self.context, zmq.Context)
        
        self._sock = self.context.socket(zmq.REQ)
        self._sock.connect('ftp://{}:{}'.format(self._host, self._target_port))
        
    #----------------------------------------------------------------------
    def send(self, routing_key, msg, timeout=10000):
        """"""
        if self._sock.poll(timeout=100, flags=zmq.POLLOUT):
            #
            # build message
            #
            _msg = {}
            _msg['routing_key'] = routing_key
            _msg['message'] = msg
            self._sock.send_pyobj(_msg)
            
            if self._sock.poll(timeout):
                _rst = self._sock.recv_pyobj()
            else:
                warnings.warn('socket cannot recv the feedback, zed return Failed')
                return False
            
            if isinstance(_rst, Ack):
                return True
            else:
                return False
        else:
            return False
    
    @property
    def socket(self):
        """"""
        return self._sock
        
        
        
    
########################################################################
class ZConsumer(_ClientIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, host, router_port, ack_port, context=None):
        """Constructor"""
        self._host = host
        self._router_port = router_port
        self._ack_port = ack_port
        
        self._router_addr = 'tcp://{}:{}'.format(self._host, self._router_port)
        self._ack_addr = 'tcp://{}:{}'.format(self._host, self._ack_port)
        
        self.context = context if context else zmq.Context()
        assert isinstance(context, zmq.Context)
        
        self._sock_to_router = self.context.socket(zmq.PULL)
        self._sock_to_router.connect(self._router_addr)
        
        self._sock_to_ack = self.context.socket(zmq.REQ)
        self._sock_to_ack.connect(self._ack_addr)
    
    #----------------------------------------------------------------------
    def recv(self, timeout=10000):
        """"""
        if self._sock_to_router.poll(timeout=timeout):
            _pkt = self._sock_to_router.recv_pyobj()
            if self._sock_to_ack.poll(timeout, zmq.POLLOUT):
                self._sock_to_ack.send_pyobj(Ack(_pkt.token))
                if self._sock_to_ack.poll(timeout):
                    self._sock_to_ack.recv_pyobj()
                else:
                    ValueError('recv a packet but i donot know whether the packet is acked')
            else:
                ValueError('cannot ack!')
                
        else:
            raise ValueError('cannot recv a packet from router')
    
    @property
    def ack_socket(self):
        """"""
        return self._sock_to_ack
    
    @property
    def router_socket(self):
        """"""
        return self._sock_to_router