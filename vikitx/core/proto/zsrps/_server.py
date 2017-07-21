#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ZSRPS Server
  Created: 07/19/17
"""

import zmq
import time

from . import context
from . import _packet as packet

from ..interfaces import ServerIf

STATE_INIT = 'init'
STATE_WORKING = 'working'
STATE_FINISHED = 'finished'

########################################################################
class ZSRPSServer(ServerIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, addr='tcp://*'):
        """Constructor"""
        self._id = id
        self._state = STATE_INIT
        self._port = 7000
        self._addr = addr
        
        #
        # build socket
        #
        self.__build_zmq_socket()
        
        #
        # recorder
        #
        self._clients = {}
        
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
        self._state = value    
    
    @property
    def port(self):
        """Connection Port"""
        return self._port

    @property
    def rep_addr(self):
        """"""
        return self._addr + ':' + str(self._port)
        
    #
    # basic op
    #
    #----------------------------------------------------------------------
    def start(self, port=7000):
        """"""
        self._port = port
        
        self.state = STATE_WORKING
        
        #
        # start main loop
        #
        self.__main_loop()
        
        
    
    #----------------------------------------------------------------------
    def sendto(self, to, content):
        """Send Somethon to Client
        
        Parameters
        ----------
        to : client id
            The client id can identify the client.
        content : PyObj(can be pickled)
            The object you want to send to client.
        
        """
        pass
    

    #
    # priv op
    #
    #----------------------------------------------------------------------
    def __build_zmq_socket(self):
        """"""
        #
        # rep to handle negtiation
        # 
        self._sock_rep_to_client = context.socket(zmq.REP)
        self._sock_rep_to_client.bind(self.rep_addr)
        
        #
        # sub to connect client pub
        #
        self._sock_sub_to_clients = context.socket(zmq.SUB)
        self._sock_sub_to_clients.setsockopt_string(zmq.SUBSCRIBE,
                                                    u'')
        
        #
        # set poller
        #
        self._poller = zmq.Poller()
        self._poller.register(self._sock_rep_to_client, flags=zmq.POLLIN)
    
    
    #----------------------------------------------------------------------
    def __main_loop(self):
        """"""
        #
        # main loop
        #
        while self.state == STATE_WORKING:
            #
            # poller
            #
            for sock, _ in self._poller.poll(timeout=1000):
                if self._sock_rep_to_client is sock:
                    self.__handle_negtiation(sock)
                if self._sock_sub_to_clients is sock:
                    self.__handle_heartbeat(sock)
    
    #----------------------------------------------------------------------
    def __handle_negtiation(self, sock):
        """"""
        neg = sock.recv_pyobj()
        
        if not self._clients.has_key(neg.id):
            _tmp = self._clients[neg.id] = {}
        else:
            del self._clients[neg.id]
            _tmp = self._clients[neg.id] = {}
            
        _tmp['id'] = neg.id
        _tmp['negtiation_lease'] = neg.negtiation_lease
        _tmp['pub_addr'] = neg.pub_addr
        self._sock_sub_to_clients.connect(neg.pub_addr)
        _tmp['rep_addr'] = neg.rep_addr
        _tmp['scope'] = {}
        _tmp['active_time'] = time.time()
        
        #
        # send negtiation response
        #
        negrsp = packet.NegotiationResponse()
        negrsp.id = neg.id
        sock.send_pyobj(negrsp)
    
    #----------------------------------------------------------------------
    def __update_client(self, client_id):
        """Input client_id and update the client active_time"""
        client = self._clients.get(client_id)
        if client:
            client['active_time'] = time.time()
    
    #----------------------------------------------------------------------
    def __update_client_scope(self, client_id, key, value):
        """"""
        client = self._clients.get(client_id)
        if client:
            client['scope'][key] = value