#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Session Manager
  Created: 07/16/17
"""

from scouter import SDict

from ._session import Session
from ._excs import SessionError


########################################################################
class SessionManager(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self._sessions = SDict({}, \
                               del_kv_callback=self.safe_delete_from_session_db)
        
    #----------------------------------------------------------------------
    def add(self, session_obj):
        """"""
        assert isinstance(session_obj, Session)
    
        if self._sessions.has_key(session_obj):
            raise SessionError('exsited session_id!')
        else:
            self._sessions[session_obj.id] = session_obj
        
    #----------------------------------------------------------------------
    def get(self, session_id):
        """"""
        if self._sessions.has_key(session_id):
            return self._sessions.get(session_id)
        else:
            raise SessionError('no such session in server!')
    
    #----------------------------------------------------------------------
    def delete(self, session_id):
        """"""
        if self._sessions.has_key(session_id):
            del self._sessions[session_id]
        else:
            raise SessionError('no such session id server!')
    
    #----------------------------------------------------------------------
    def safe_delete_from_session_db(self, key, value):
        """"""
        