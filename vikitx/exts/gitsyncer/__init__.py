#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Git Syncer Wrapper
  Created: 07/28/17
"""

from ._docker_manager import start_git_server, stop_git_server
from . import _gitclient as gitclient
