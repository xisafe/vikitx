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
import Queue

from . import context, logger
from ..interfaces import ClientIf
from . import _packet as packet
from .. import task
from .. import thread_utils

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
        
        #
        # response cache
        #
        self._response_cache_queue = Queue.Queue()
        
        #
        # scope recording
        #
        self._scope = {}
        
        
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
        logger.info('ZSRPS State Changed: from {} -> {}'.format(self._state, value))
        #
        # change state and calling callback
        #
        self._state = value
        
        if self.state == STATE_TIMEOUT:
            raise NotImplemented()
        elif self.state == STATE_SHAKE_HAND_FINISHED:
            pass
    
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
        _hb.scope = self.scope
        
        return _hb
    
    @property
    def scope(self):
        """"""
        return self._scope
    
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
        logger.debug('socket pub bind to {}'.format(self.pub_addr))
        
        #
        # build socket to receive instructions from server
        #
        self._sock_rep_to_server = context.socket(zmq.REP)
        self._rep_port = self._sock_rep_to_server.bind_to_random_port('tcp://*')
        logger.debug('socket rep bind to {}'.format(self.rep_addr))
        
    
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
        logger.info('sending negtiation packet! from: {}'.format(neg.id))
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
            if not self._sock_rep_to_server.poll(1000):
                continue
            
            _est = self._sock_rep_to_server.recv_pyobj()
            if isinstance(_est, packet.Established):
                self._sock_rep_to_server.send_pyobj(packet.Ack())
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
            return self._loopingcall_heartbeat.stop()
        else:
            pass
        
        
    
    #----------------------------------------------------------------------
    def __connect(self):
        """"""
        
        #
        # 1. shake hand
        #
        self.__shake_hand()
    
        self.state = STATE_WORKING
    
        #self.__main_loop()
        #
        # 2. main loop
        #
        self.main_loop_thread = thread_utils.start_thread('client-mainloop',
                                                          True,
                                                          self.__main_loop)
        
    
    #----------------------------------------------------------------------
    def __main_loop(self):
        """"""
        while self.state == STATE_WORKING:
            if self._sock_rep_to_server.poll(0, flags=zmq.POLLIN):
                datapkt = self._sock_rep_to_server.recv_pyobj()
                state, extra = self.handle_packet(datapkt)
                if state:
                    ack = packet.Ack(extra)
                else:
                    failure = packet.Failure(extra)
        
        self.stop_heartbeat()
        self._sock_pub_to_server.send_pyobj(packet.LastHeartbeat(self.id))
    
    #----------------------------------------------------------------------
    def handle_packet(self, pkt):
        """If you want to handle packet from server, overide this method
        
        Parameters:
        -----------
        pkt: core.proto._packet.DataBase
            the packet you want to handle in this packet
            
        Returns:
        --------
        state: bool
            ack or not (Success or Failed)
        
        extradata: dict
            the dict has at last 1 key: "extra" for extra data from handle_action
        """
        logger.info('got a message:{}'.format(pkt))
        self._sock_rep_to_server.send_pyobj(packet.Ack())
        
        state = True
        extradata = {}
        
        if hasattr(self, 'handle_action'):
            _tmp = self.handle_action(pkt)
            try:
                state, data = _tmp
                extradata['extra'] = data
            except ValueError:
                extradata['extra'] = _tmp
                if extradata:
                    state = False
            
        return state, extradata
        
                
    
    #----------------------------------------------------------------------
    def stop(self):
        """Stop the client mainloop and shutdown"""
        self.state = STATE_CLOSING
        self.join()
        self.state = STATE_CLOSED
    
    
    #----------------------------------------------------------------------
    def join(self):
        """"""
        self.main_loop_thread.join()
    
    #----------------------------------------------------------------------
    def set_scope_value(self, key, value):
        """"""
        self._scope[key] = value
    
    #----------------------------------------------------------------------
    def del_scope_value(self, key):
        """"""
        if self._scope.has_key(key):
            del self._scope[key]
        else:
            pass
    
    #----------------------------------------------------------------------
    def get_scope_value(self, key):
        """"""
        return self._scope.get(key)
        