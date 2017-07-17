#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Session
  Created: 07/16/17
"""

import os

_CURRENT_PATH = os.path.dirname(__file__)

_ROOT_DIR = os.path.join(_CURRENT_PATH, '../../../')
_TEMP_DIR = os.path.join(_ROOT_DIR, 'tmp/sessions')

########################################################################
class Session(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, session_id):
        """Constructor"""
        
        self._id = session_id
        
        self._scope = {}
    
    @property
    def id(self):
        """"""
        return self._id
        
    @property
    def scope(self):
        """"""
        return self._scope
    
    #----------------------------------------------------------------------
    def add(self, key, value):
        """"""
        self._scope[key] = value
        
    #----------------------------------------------------------------------
    def update(self, key, value):
        """"""
        self.add(key, value)
        
    #----------------------------------------------------------------------
    def delete(self, key):
        """"""
        if self._scope.has_key(key):
            del self._scope[key]
        else:
            pass
        
    #----------------------------------------------------------------------
    def get(self, key):
        """"""
        return self._scope.get(key)
