#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Node Client
  Created: 07/28/17
"""

import warnings

from .. import ZClientBase

########################################################################
class SNClient(ZClientBase):
    """"""

    __handle_action_table = {
    }

    #----------------------------------------------------------------------
    def handle_action(self, action):
        """Hanlde action from Platform
        
        Parameters:
        -----------
        action: instance
            
        """
        #
        # find handler
        #
        _type = type(action)
        _handler = self.find_handler(_type)
        
        
        #
        # process the handle process
        #
        if _handler:
            _handler(action)
        else:
            return False, 'no handler for the action:{}'.format(action)
        
        #
        # return at least 2 value (state, extradata)
        #
        self.send_heartbeat()
        return True, {}
    
    #----------------------------------------------------------------------
    def regist_action(self, type, handler):
        """"""
        if self.__handle_action_table.has_key(type):
            warnings.warn('you have rewrite the action:{} handler'.\
                          format(str(type)))
        
        self.__handle_action_table[type] = handler
    
    #----------------------------------------------------------------------
    def find_handler(self):
        """"""
        return self.__handle_action_table.get(type)
    
