#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Interfaces
  Created: 07/24/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

########################################################################
class StateAble(object):
    """"""
    
    __metaclass__ = ABCMeta
    
    _state = None

    @abstractproperty
    def START_STATE(self):
        """"""
        
    @abstractproperty
    def TRANS_TABLE(self):
        """"""
        
        

    @property
    def state(self):
        """"""
        if self._state:
            return self._state
        else:
            self._state = self.START_STATE
            return self._state
    
    @state.setter
    def state(self, value):
        """"""
        assert value in self.TRANS_TABLE[self.state], 'state shifts error!' + \
               ' cannot shift from:{} to:{}'.format(self.state, value)
        
        self._state = value
        
    
    