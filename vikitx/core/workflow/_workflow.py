#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Workflow
  Created: 07/16/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

########################################################################
class _WorkflowIf():
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, channel):
        """Constructor"""
        
        
    @abstractmethod
    def reset(self):
        """"""
        pass
    
    @abstractmethod
    def destory(self):
        """"""
        pass
        
    