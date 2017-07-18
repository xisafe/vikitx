#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: C
  Created: 07/17/17
"""

import abc

########################################################################
class CryptoBase(object):
    """"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def enc(self):
        """"""
        
    @abc.abstractmethod
    def dec(self):
        """"""
    
    @abc.abstractproperty
    def key(self):
        """"""
        
    
    