#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Exchanger
  Created: 07/30/17
"""

import Queue
import zmq
from scouter.sop import FSM
import warnings

from uuid import uuid1

from .. import thread_utils

from ._routing_table import RoutingTable
from ._msg import _Msg
from ._entry import Entry
from ._router import Router
from ._ackpool import Ackpool
from ._signal import Ack, Failed

#
# define state machine
#
state_INIT = 'init'
state_WORKING = 'working'
state_END = 'end'

action_START = 'start'
action_SHUTDOWN = 'shutdown'

fsm = FSM(start_state=state_INIT, end_state=state_END,
            states=[state_INIT, state_WORKING, state_END])
fsm.create_action(action_name=action_START, 
                    orig=state_INIT, dest=state_WORKING)
fsm.create_action(action_name=action_SHUTDOWN,
                    orig=state_WORKING, dest=state_END)

########################################################################
class Exchanger(object):
    """Exchanger Main Define
    
    Attributes:
    -----------
    id: int
        identify the exchanger entity
    
    host: str
        the exchanger IP or addr
    
    backend_port: int
        which port to ack packet?
    
    """  

    #----------------------------------------------------------------------
    def __init__(self, id=None, host='127.0.0.1', backend_port=3424, 
                 ack_timeout=10, count=3, queue_ttl=256):
        """Constructor"""
        #
        # basic attributes
        #
        self._id = str(uuid1())
        self._host = host
        self._backend_port = backend_port
        self.poller = zmq.Poller()
        self.context = zmq.Context()
        self.queue_ttl = queue_ttl
        
        #
        # router and entry
        #
        self.routers = {}
        self.rsocks = []
        self.entries = {}
        self.esocks = []
        
        #
        # build routing table
        #
        self.table = RoutingTable()
        
        #
        # record routers and cache queue
        #
        self.__cache_queue = Queue.Queue()
        
        #
        # ack pool
        #
        self.ackpool = Ackpool(ack_timeout, count, self.handle_timeout_message)
        
        #
        # regist backend sock
        #
        self.sock_backend = self.context.socket(zmq.REP)
        self.sock_backend.bind(self.generate_addr(self.backend_port))
        self.poller.register(self.sock_backend, zmq.POLLIN)
        
        
    #
    # basic property
    #
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def host(self):
        """"""
        return self._host
    
    @property
    def backend_port(self):
        """"""
        return self._backend_port
    
    #----------------------------------------------------------------------
    def generate_addr(self, port, host='*'):
        """"""
        return 'tcp://{}:{}'.format(host, port)
        

    @fsm.onstate(state_WORKING)
    def put_in_cache_queue(self, routing_key, message, callback=None):
        """Put msg in queue, but only the ackpool can remove the packet  
        
        Params:
        -------
        routing_key: str
            the msg where to go
        
        message: packet
            the message content
         
        callback: function
            callback need recv 2 params: 1st the routing_key, 2nd is the message body
        """
        assert routing_key in self.routers, 'no such router!'
        
        #
        # convert message into _Msg
        #
        _flag = hasattr(message, 'token')
        if _flag:
            token = getattr(message, 'token')
        else:
            try:
                token = message['token']
            except KeyError:
                token = ''
        
        msg = _Msg(token, routing_key=routing_key, message=message)
        
        #
        # add in routing table 
        #
        self.table.record_msg(msg)
        
        self._put_in_cache_queue(msg)
    
    #----------------------------------------------------------------------
    def _put_in_cache_queue(self, _msg):
        """"""
        
        #
        # put the message into cache queue
        #
        self.__cache_queue.put(_msg)
    
    @fsm.onstate(state_WORKING)    
    def get_msg_from_cache_queue(self):
        """"""
        if self.__cache_queue.empty():
            return None
        else:
            return self.__cache_queue.get_nowait()
        
    def regist_entry(self, port):
        """"""
        #
        # port
        #
        port = int(port)
        assert not self.entries.has_key(port)
        
        sock = self.context.socket(zmq.REP)
        sock.bind(self.generate_addr(port))
        self.poller.register(sock)
        self.esocks.append(sock)
        
        _entry = Entry(port, sock)
    
        self.entries[port] = _entry
        
    def regist_router(self, routing_key, port):
        """"""
        #
        # port
        #
        port = int(port)
        assert not self.routers.has_key(routing_key)
        
        sock = self.context.socket(zmq.PUSH)
        sock.bind(self.generate_addr(port))
        #self.poller.register(sock, zmq.POLLOUT) # 
        self.rsocks.append(sock)
        
        _router = Router(routing_key, port, sock)
        self.routers[routing_key] = _router
    
    @fsm.onstate(state_WORKING)    
    def get_router_sock(self, routing_key):
        """"""
        _router = self.routers.get(routing_key)
        if _router:
            return _router.socket
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        fsm.action(action_START)
        
        #
        # start ackpool
        #
        self.ackpool.start()
        
        self.__thread_mainloop = thread_utils.start_thread('{}-mainloop'.format(self.id),
                                                           True,
                                                           self.__mainloop,)
        
    
    #----------------------------------------------------------------------
    def __mainloop(self):
        """"""
        #
        # mainloop
        #
        while fsm.state == state_WORKING:
            #
            # processing polling
            #
            for sock, flag in self.poller.poll(timeout=0):
                if sock is self.sock_backend and flag & zmq.POLLIN:
                    acksig = sock.recv_pyobj()
                    #
                    # finish
                    #
                    self.ackpool.ack(acksig.token)
                    
                    sock.send_pyobj(Ack(acksig.token))
                    self.finish_message(acksig.token)
                elif sock in self.esocks and flag & zmq.POLLIN:
                    #
                    # esocks recving msg
                    #
                    packet = sock.recv_pyobj()
                    rk = packet.get('routing_key')
                    
                    if hasattr(packet.get('message'), 'token'):
                        token = getattr(packet.get('message'), 'token')
                    elif hasattr(packet.get('message'), 'id'):
                        token = getattr(packet.get('message'), 'id')
                    else:
                        token = ''
                    
                    try:
                        self.put_in_cache_queue(rk, message=packet.get('message'))
                        sock.send_pyobj(Ack(token))
                    except AssertionError:
                        msg = packet.get('message')
                        sock.send_pyobj(Failed(token))
                        
            #
            # handle queue
            #
            if not self.__cache_queue.empty():
                _msg = self.get_msg_from_cache_queue()
                assert isinstance(_msg, _Msg)

                sock = self.get_router_sock(_msg.routing_key)
                assert isinstance(sock, zmq.Socket)
                
                if sock.poll(timeout=100, flags=zmq.POLLOUT):
                    sock.send_pyobj(_msg.message)
                    if _msg.token == '':
                        pass
                    else:
                        self.ackpool.add(_msg.token, callback=self._put_in_cache_queue, args=(_msg,), kw={})
                    
                else:
                    if _msg.retry_count < self.queue_ttl:
                        _msg.retry()
                        self._put_in_cache_queue(_msg)
                    else:
                        self.handle_timeout_message(_msg.token, _msg.message)
                
            
    #----------------------------------------------------------------------
    def join(self):
        """"""
        self.__thread_mainloop.join()
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        print('stop intruction setting')
        fsm.action(action_SHUTDOWN)
        
        self.ackpool.stop()
    
    #----------------------------------------------------------------------
    def handle_timeout_message(self, token, packet):
        """"""
        warnings.warn('if you want to store the packet:{} into you error db. you should handle this warning'.\
                      format(packet))
        
        self.finish_message(token)
    
    #----------------------------------------------------------------------
    def finish_message(self, token):
        """"""
        if token == '':
            pass
        else:
            self.table.remove_msg(token)