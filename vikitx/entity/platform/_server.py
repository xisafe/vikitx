#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Platform
  Created: 07/28/17
"""

from .. import ZServerBase

########################################################################
class PlatformServer(ZServerBase):
    """"""
    
    #----------------------------------------------------------------------
    def get_available_clients(self):
        """"""
        return self._clients.keys()
    
    #----------------------------------------------------------------------
    def get_client_scope(self, client_id):
        """"""
        return self.get_workflow(client_id)
    
    #----------------------------------------------------------------------
    def remove_client(self, client_id):
        """"""
        if self._clients.has_key(client_id):
            del self._clients[client_id]
        else:
            pass