#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Routing Table
  Created: 07/31/17
"""

from ._msg import _Msg

########################################################################
class RoutingTable(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self._main_tables = {}
    
    #
    # add
    #
    #----------------------------------------------------------------------
    def record_msg(self, msg):
        """Insert the Msg"""
        assert isinstance(msg, _Msg)
        
        self._main_tables[_Msg.id] = _Msg
    
    #
    # query
    #
    #----------------------------------------------------------------------
    def get_routing_key(self, msg_id):
        """Get the routing key by message id"""
        _msg = self.__get_msg(msg_id)
        if _msg:
            return _msg.routing_key
    
    #----------------------------------------------------------------------
    def get_content(self, msg_id):
        """Get the content by message id"""
        _msg = self.__get_msg(msg_id)
        if _msg:
            return _msg.message 
    
    #----------------------------------------------------------------------
    def __get_msg(self, msg_id):
        """"""
        return self._main_tables.get(msg_id)
        
    #
    # delete
    #
    #----------------------------------------------------------------------
    def remove_msg(self, msg_id):
        """Delete msg from table"""
        if self._main_tables.has_key(msg_id):
            del self._main_tables[msg_id]
    
    #----------------------------------------------------------------------
    def pop_msg(self, msg_id):
        """Get and remove message from routing table"""
        _m = self.__get_msg(msg_id)
        if _m:
            self.remove_msg(msg_id)
            return _m
        