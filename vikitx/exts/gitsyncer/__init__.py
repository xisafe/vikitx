#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Git Syncer Wrapper
  Created: 07/28/17
"""

from ._docker_manager import start_git_server, stop_git_server
from ._docker_manager import gen_and_add_keypair, get_key, clear_all_public_key
from . import _gitclient as gitclient
