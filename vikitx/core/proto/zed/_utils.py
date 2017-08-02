#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Utils Functions
  Created: 08/02/17
"""

#----------------------------------------------------------------------
def get_item_or_attr(obj, key, default=None):
    """"""
    try:
        return obj[key]
    except:
        if hasattr(obj, key):
            return getattr(obj, key)
        else:
            return False