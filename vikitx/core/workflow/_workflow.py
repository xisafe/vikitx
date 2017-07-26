#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Workflow
  Created: 07/16/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from ._interfaces import StateAble

########################################################################
class Workflow(StateAble):
    """"""
    
    __metaclass__ = ABCMeta

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
    
    
    @abstractproperty
    def START_STATE(self):
        """Define the initial state"""
        
    @abstractproperty
    def TRANS_TABLE(self):
        """Define the state transportation table"""
        
        