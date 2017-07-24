#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ZSRPS Client
  Created: 07/21/17
"""

from __future__ import unicode_literals

import zmq
import time

from . import context, logger
from ..interfaces import ClientIf
from . import _packet as packet
from .. import task

STATE_INIT = 'init'
STATE_SHAKE_HAND_STARTING = 'shake_hand_starting'
STATE_SHAKE_HAND_FINISHED = 'shake_hand_finished'
STATE_WORKING = 'working'
STATE_TIMEOUT = 'timeout'
STATE_ERROR = 'error'
STATE_CLOSING = 'closing'
STATE_CLOSED = 'closed'

########################################################################
class ZSRPSClient(ClientIf):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, id, host):
        """"""
        self._id = id
        self._state = STATE_INIT
        self._timeout = 30
        
        #
        # record
        #
        self._server_info = None
        self._pub_port = None
        self._rep_port = None
        
        #
        # host
        #
        self._host = host
        
        self.__build_zmq_socket()
        
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def state(self):
        """"""
        return self._state
    
    @state.setter
    def state(self, value):
        """"""
        logger.info('[#] ZSRPS State Changed: from {} -> {}'.format(self._state, value))
        #
        # change state and calling callback
        #
        self._state = value
        
        if self.state == STATE_TIMEOUT:
            raise NotImplemented()
        elif self.state == STATE_SHAKE_HAND_FINISHED:
            self._state = STATE_WORKING
    
    @property
    def pub_addr(self):
        """"""
        _ret = self._pub_port if self._pub_port else None
        if _ret:
            return 'tcp://{}:{}'.format(self._host, self._pub_port)
        else:
            return
    
    @property
    def rep_addr(self):
        """"""
        _ret = self._rep_port if self._rep_port else None
        if _ret:
            return 'tcp://{}:{}'.format(self._host, self._rep_port)
        else:
            return 
    
    @property
    def heartbeat(self):
        """"""
        _hb = packet.Hearbeat(self.id)
        
        #
        # update heartbeat info
        #
        
        return _hb
    
    #
    # basic op
    #
    #----------------------------------------------------------------------
    def connect(self, host, port, timeout=30):
        """"""
        logger.info('zsrps start connecting')
        
        self._timeout = timeout
        #
        # record the target info for server
        #
        if not self._server_info:
            self._server_info = {}

        self._server_info.update(host=host, port=port)
        
        #
        # connect func
        #
        self.__connect()
    
    #----------------------------------------------------------------------
    def reconnect(self):
        """"""
        self.state = STATE_INIT
    
        self.__connect()
        
    
    #----------------------------------------------------------------------
    def send(self):
        """"""
        #assert 
        
        
    #
    # priv op
    #
    #----------------------------------------------------------------------
    def __build_zmq_socket(self):
        """"""
        #
        # build socket to pub 
        #
        self._sock_pub_to_server = context.socket(zmq.PUB)
        self._pub_port = self._sock_pub_to_server.bind_to_random_port('tcp://*')
        
        #
        # build socket to receive instructions from server
        #
        self._sock_pair_to_server = context.socket(zmq.PAIR)
        self._rep_port = self._sock_pair_to_server.bind_to_random_port('tcp://*')
    
    #----------------------------------------------------------------------
    def __on_receiving_from_server(self):
        """"""
        
        
        
    #----------------------------------------------------------------------
    def __shake_hand(self):
        """Shake Hand"""
        self.state = STATE_SHAKE_HAND_STARTING
        
        logger.info('zsrps client shaking hands')
        #
        # generate a client_id
        #
        host = self._server_info.get('host')
        port = self._server_info.get('port')
        
        #
        # build socket to connect server
        #
        self._sock_req_to_server = context.socket(zmq.REQ)        
        self._sock_req_to_server.connect('tcp://{}:{}'.format(host, port))

        #
        # negtiation 
        #
        negtiation_lease = time.time() + self._timeout
        neg = packet.Negotiation(self.pub_addr, self.rep_addr, negtiation_lease)
        neg.id = self.id
        logger.info('sending negtiation packet')
        self._sock_req_to_server.send_pyobj(neg)
        negrsp = self._sock_req_to_server.recv_pyobj()
        logger.info('received negtiation response')
        assert isinstance(negrsp, packet.NegotiationResponse)
        self._server_info['id'] = negrsp.id 
        
        # shudown req
        del self._sock_req_to_server
        
        #
        # starting the heartbeat fast (interval 1)
        #
        self.start_heartbeat(1)
        
        #
        # shaking hand mainloop
        #
        while self.state == STATE_SHAKE_HAND_STARTING:
            #
            # after receving the heartbeat, server will send a Established Signal
            #
            if self._sock_pair_to_server.poll(1000) == 0:
                continue
            
            _est = self._sock_pair_to_server.recv_pyobj()
            if isinstance(_est, packet.Established):
                break
        
        self.state = STATE_SHAKE_HAND_FINISHED
        
        self.start_heartbeat(5)
    
    #----------------------------------------------------------------------
    def start_heartbeat(self, interval=None):
        """"""
        if not hasattr(self, '_loopingcall_heartbeat'):
            self._loopingcall_heartbeat = task.LoopingCall(self.send_heartbeat)
        
        #
        # restart and start
        #
        if interval:
            if self._loopingcall_heartbeat.running:
                self._loopingcall_heartbeat.stop()
                
            self._loopingcall_heartbeat.start(interval)
        else:
            self._loopingcall_heartbeat.stop()
    
    #----------------------------------------------------------------------
    def send_heartbeat(self):
        """"""
        self._sock_pub_to_server.send_pyobj(self.heartbeat)
        
    
    #----------------------------------------------------------------------
    def stop_heartbeat(self):
        """"""
        if hasattr(self, '_loopingcall_heartbeat'):
            return self.__loopingcall_heartbeat.stop()
        else:
            pass
        
        
    
    #----------------------------------------------------------------------
    def __connect(self):
        """"""
        
        #
        # 1. shake hand
        #
        self.__shake_hand()
    
        #
        # 2. main loop
        #
    
    

    
        
    
    