#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Git Sync Test
  Created: 07/28/17
"""

import unittest
import os

from vikitx.exts import gitsyncer
from vikitx.exts.gitsyncer import start_git_server, stop_git_server

CURRENT_DIR = os.path.abspath(__file__)
BASE_DIR = os.path.join(CURRENT_DIR, 'vikitx/')

########################################################################
class GitSyncerTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_start_server(self):
        """"""
        
        start_git_server(container_name='vikitx-git-server',
                         base_dir=BASE_DIR,
                         pub_dirname='pubkeys',
                         git_dirname='repos')
        
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, 'pubkeys')))
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, 'repos')))
    
    #----------------------------------------------------------------------
    def test_add_pubkeys(self):
        """"""
        private = gitsyncer.gen_and_add_keypair(once=True)   
    
    #----------------------------------------------------------------------
    def test_z_stop_server(self):
        """"""
        stop_git_server()
        
    

if __name__ == '__main__':
    unittest.main()