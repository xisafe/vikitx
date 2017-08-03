#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Phoenix
  Created: 08/03/17
"""

from ._client import SNClient
from ._servicenode import ServiceNode, ServiceNodeConfig

from .._common import packets

########################################################################
class Phoenix(object):
    """Phoenix can connect servicenode, zsrps_client, task_receiver"""

    #----------------------------------------------------------------------
    def __init__(self, id, nest_host, port, self_host='127.0.0.1'):
        """Constructor"""
        self._self_host = self_host
        
        self._id = id
        self._nest_host = nest_host
        self._port = port
        
        self.__init_servicenode()
        
        self.__init_client()
    
    @property
    def id(self):
        """"""
        return self._id
        
    #----------------------------------------------------------------------
    def __init_servicenode(self):
        """"""
        self.__servicenode = ServiceNode(self.id)
        self.__servicenode.start()
        
    #----------------------------------------------------------------------
    def __init_client(self):
        """"""
        self.__client = SNClient(self.id, self._self_host)
        
        SNClient.regist_action(type=packets.ActionStartService, handler=self.start_service)
        
        self.__client.connect(host=self._nest_host, port=self._port)
    
    #----------------------------------------------------------------------
    def start_service(self, packet):
        """"""
        assert isinstance(packet, packets.ActionStartService)
        
        #
        # convert mod_type to a function type
        #
        raise NotImplemented()
        #self.__servicenode.start_service(service_id)
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        #
        # start receiving task
        #