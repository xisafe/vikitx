#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ZSRPS Server
  Created: 07/19/17
"""

import zmq
import time

from . import _workflows as workflow
from ._workflows import ZSRPSWorkflow

from . import context
from . import _packet as packet
from . import logger
from . import _keywords
from . import _excs

from .. import threadpool
from .. import thread_utils
from ..interfaces import ServerIf

STATE_INIT = 'init'
STATE_WORKING = 'working'
STATE_FINISHED = 'finished'

########################################################################
class ZSRPSServer(ServerIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, addr='tcp://*', port=7000):
        """Constructor"""
        self._id = id
        self._state = STATE_INIT
        self._port = 7000 if not port else port
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
        
        self._run()
        #self.mainloop = thread_utils.start_thread('platform:{}-mainloop'.format(id),
                                                  #True,
                                                  #target=self._run)
    
    #----------------------------------------------------------------------
    def _run(self):
        """"""
        
        #
        # start main loop
        #
        self.__main_loop()
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.state = STATE_FINISHED
        self.join()
    
    #----------------------------------------------------------------------
    def join(self):
        """"""
        self.mainloop.join()
        
    #----------------------------------------------------------------------
    def sendto(self, to, content, timeout=5000):
        """Send Somethon to Client
        
        Parameters
        ----------
        to : client id
            The client id can identify the client.
            
        content : PyObj(can be pickled)
            The object you want to send to client.
        
        """
        _wrkflw = self.get_workflow(to)
        assert isinstance(_wrkflw, ZSRPSWorkflow)
        
        if _wrkflw.socket.poll(timeout, flags=zmq.POLLOUT):
            _wrkflw.socket.send_pyobj(content)
            return _wrkflw.socket.recv_pyobj()
        else:
            raise _excs.ZSRPSError('cannot send content to peer client')
    
    #----------------------------------------------------------------------
    def send_action(self, client_id, content, timeout=5000):
        """"""
        try:
            logger.info('send a packet:{} to:{}'.format(content, client_id))
            action_result = self.sendto(client_id, content, timeout)
            if isinstance(action_result, packet.Failure):
                return False, action_result.extra
            else:
                return True, action_result.extra
        except _excs.ZSRPSError:
            logger.error('cannot send content to peer client:{}'.format(client_id))
            return False, {'extra':'cannot send content to peer client:{}'.format(client_id)}

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
        self._poller.register(self._sock_sub_to_clients, flags=zmq.POLLIN)
    
    
    #----------------------------------------------------------------------
    def __main_loop(self):
        """"""
        #
        # main loop
        #
        logger.info('server enter main loop')
        while self.state == STATE_WORKING:
            #
            # poller
            #
            for sock, _ in self._poller.poll(0):
                if self._sock_rep_to_client is sock:
                    self.__handle_negtiation(sock)
                if self._sock_sub_to_clients is sock:
                    self.__handle_heartbeat(sock)
    
    #----------------------------------------------------------------------
    def __handle_negtiation(self, sock):
        """"""
        neg = sock.recv_pyobj()
        
        assert isinstance(neg, packet.Negotiation)
        
        
        if not self._clients.has_key(neg.id):
            pass
        else:
            _wf = self._clients.get(neg.id)
            padr = _wf.get_env(_keywords.PUB_ADDR)
            self._sock_sub_to_clients.disconnect(padr)
            del self._clients[neg.id]
            
        logger.debug('building client workflow')
        _wf = ZSRPSWorkflow(neg.id, self)
        self._clients[neg.id] = _wf        
        
        _wf = self._clients.get(neg.id)
        
        #
        # handle packet
        #
        logger.debug('handling negotiation request! from: {}'.format(neg.id))
        _wf.handle_packet(neg)
        
        if _wf.state == workflow.state_SHAKEHAND:
            pubaddr = _wf.get_env(_keywords.PUB_ADDR)
            self._sock_sub_to_clients.connect(pubaddr)
            
            #
            # response
            #
            logger.debug('response negotiation request')
            negrsp = packet.NegotiationResponse()
            negrsp.id = neg.id
            sock.send_pyobj(negrsp)
        else:
            #
            # negotiation failed
            #
            logger.debug('negotiation handle error!')
            del self._clients[neg.id]
            sock.send_pyobj(packet.Reset())
    
    #----------------------------------------------------------------------
    def __handle_heartbeat(self, sock):
        """"""
        _hb = sock.recv_pyobj()
        logger.debug('Received a hearbeat from: {}'.format(_hb.id))
        
        wkfw = self._clients.get(_hb.id)
        assert isinstance(wkfw, ZSRPSWorkflow)
        
        wkfw.handle_packet(_hb)
        
        #
        # when received last heartbeat 
        #
        if isinstance(_hb, packet.LastHeartbeat):
            self.finish_workflow(_hb.id)
            
    
    #
    # manage workflow
    #
    #----------------------------------------------------------------------
    def finish_workflow(self, client_id):
        """"""
        _wf = self._clients.get(client_id)
        if _wf:
            del self._clients[client_id]
    
    #----------------------------------------------------------------------
    def get_workflow(self, client_id):
        """"""
        return self._clients.get(client_id)