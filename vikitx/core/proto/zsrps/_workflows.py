#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Session
  Created: 07/26/17
"""

import time
import zmq

from .. import Workflow
from . import context
from . import _packet
from . import _keywords
from . import logger
from . import threadpool


#
# define state
#
state_INIT = 'INIT'
state_SHAKEHAND = 'shake_hands'
state_SHAKEHAND_FINISHED = 'shake_hand_finished'
state_WORKING = 'working'
state_TIMEOUT = 'timeout'
state_ERROR = 'error'
state_END = 'end'

########################################################################
class ScopeAble(object):
    """"""

    @property
    def scope(self):
        """"""
        if hasattr(self, '_scope'):
            return self._scope
        else:
            self._scope = {}
            return self._scope
    
    #----------------------------------------------------------------------
    def set_env(self, key, value):
        """"""
        self.scope[key] = value
    
    #----------------------------------------------------------------------
    def get_env(self, key):
        """"""
        return self.scope.get(key)
        
        
    
    

########################################################################
class ZSRPSWorkflow(Workflow, ScopeAble):
    """ZSRPS Workflow to control the connection between Server and Client
    
    Attributes:
    -----------
    id: str
        you can identify the different session from is property: id
        
    Main Methods:
    -------------
    handle_packet(pkt): None
        handle packet and change its state inside
    
    """
    
    _trans_table = {
        state_INIT: [state_SHAKEHAND, ],
        state_SHAKEHAND: [state_SHAKEHAND_FINISHED, state_TIMEOUT, state_ERROR],
        state_SHAKEHAND_FINISHED: [state_WORKING, state_TIMEOUT, state_ERROR],
        state_WORKING: [state_TIMEOUT, state_ERROR, state_END],
        state_ERROR: [state_INIT, state_END],
        state_TIMEOUT: [state_INIT, state_END, state_ERROR]
        
    }
    
    #----------------------------------------------------------------------
    def __init__(self, session_id, bind_server):
        """Initial id"""
        self._id = id
        
        self.server = bind_server
        
        self.req = context.socket(zmq.REQ)
        
        #
        # shaking hand lock
        #
        self._lock_shaking_hand = False
        
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def START_STATE(self):
        """"""
        return state_INIT
    
    @property
    def TRANS_TABLE(self):
        """"""
        return self._trans_table

    #----------------------------------------------------------------------
    def handle_packet(self, pkt):
        """"""
        #
        # handle socket by state
        #
        if self.state == state_INIT:
            self.__handle_first_packet(pkt)
        
        elif self.state == state_SHAKEHAND:
            self.__handle_packet_on_shaking_hands(pkt)
            
        #
        # working logic
        #
        elif self.state == state_WORKING:
            self.__handle_heartbeat_on_working(pkt)
    
    #----------------------------------------------------------------------
    def __handle_heartbeat_on_working(self, pkt):
        """"""
        if isinstance(pkt, _packet.Hearbeat):
            threadpool.feed(self.update_info_from_heartbeat, (pkt,),
                            enable_global_result_callback=False)
    
    #----------------------------------------------------------------------
    def update_info_from_heartbeat(self, hb_pkt):
        """Update client scope information from the heartbeat packet"""
        assert isinstance(hb_pkt, _packet.Hearbeat)
        
        #
        # process heartbeat
        #
        pass
    
    #----------------------------------------------------------------------
    def __handle_first_packet(self, pkt):
        """"""
        if not isinstance(pkt, _packet.Negotiation):
            self.state = state_ERROR
            return
        
        self.set_env(_keywords.ID, pkt.id)
        self.set_env(_keywords.NEGOTIATION_LEASE, pkt.negotiation_lease)
        
        #
        # when close workflow you should clean pubaddr
        #
        self.set_env(_keywords.PUB_ADDR, pkt.pub_addr)
        
        #
        # connect to rep
        #
        logger.debug('Got client rep addr: {}'.format(pkt.rep_addr))
        self.set_env(_keywords.REP_ADDR, pkt.rep_addr)
        self.req.connect(self.get_env(_keywords.REP_ADDR))
        
        self.set_env(_keywords.UPDATE_TIME, time.time())
        
        self.state = state_SHAKEHAND
    
    #----------------------------------------------------------------------
    def __handle_packet_on_shaking_hands(self, pkt):
        """"""
        #
        # update active time
        #
        self.update()
        
        if isinstance(pkt, _packet.Hearbeat):
            
            if not self._lock_shaking_hand:
                self._lock_shaking_hand = True
            else:
                return
            
            threadpool.feed(self.ack_established,
                            enable_global_result_callback=False)
        
    
    #----------------------------------------------------------------------
    def ack_established(self):
        """"""
        try:
            self.req.send_pyobj(_packet.Established())
            
            while True:
                if self.get_env(_keywords.NEGOTIATION_LEASE) < time.time():
                    self.state = state_TIMEOUT
                    break
                
                if self.req.poll():
                    logger.debug('Got Established ACK')
                    _ack = self.req.recv_pyobj()
                    break
            
            self.state = state_SHAKEHAND_FINISHED
            self.state = state_WORKING
        except zmq.ZMQError:
            self.state = state_ERROR
        
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        #
        # remove sub pub relationship
        #
        self.server._sock_sub_to_clients.disconnect(self.get_env(_keywords.PUB_ADDR))
    
    #----------------------------------------------------------------------
    def update(self):
        """"""
        self.set_env(_keywords.UPDATE_TIME, time.time())