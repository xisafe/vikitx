#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: basic operations about docker
  Created: 07/28/17
"""

import warnings
import os
import docker

#
# basic path information
#
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
GITSERVER_DOCKERFILE = os.path.join(CURRENT_PATH, 'gitserverdocker/')

#
# const
#
GITSERVER_IMAGE_NAME = 'vikitx_git_server_img'
DEFAULT_CONTAINER_NAME = 'vikitx-git-server'
PUB_DIRNAME = 'pubkeys'
GIT_DIRNAME = 'repos'

#----------------------------------------------------------------------
def __build_git_server():
    """"""
    global GITSERVER_IMAGE_NAME
    client = docker.from_env()
    

#----------------------------------------------------------------------
def start_git_server(container_name=DEFAULT_CONTAINER_NAME,
                     base_dir=CURRENT_PATH,
                     pub_dirname=PUB_DIRNAME,
                     git_dirname=GIT_DIRNAME,
                     port=2222):
    """"""
    global GITSERVER_DOCKERFILE, GITSERVER_IMAGE_NAME
    PK_DIR = os.path.join(base_dir, pub_dirname)
    RP_DIR = os.path.join(base_dir, git_dirname)
    
    client = docker.from_env()
    print(PK_DIR)
    print(RP_DIR)
    #
    # build or find image
    #
    try:
        client.images.get(GITSERVER_IMAGE_NAME)
    except docker.errors.ImageNotFound:
        warnings.warn('no git server images found, docker is building it')
        client.images.build(path=GITSERVER_DOCKERFILE,
                            tag=GITSERVER_IMAGE_NAME)
        
    #
    # start container
    #
    try:
        container = client.containers.get(container_name)
        container.start()
    except docker.errors.NotFound:
        container = client.containers.run(GITSERVER_IMAGE_NAME, 
                                          ports={'22/tcp':port},
                                          volumes={PK_DIR:
                                                   {'bind':'/git-server/keys/',
                                                    'mode':'ro'},
                                                   RP_DIR:
                                                   {'bind':'/git-server/repos/',
                                                    'mode':'rw'}},
                                          detach=True,
                                          name=container_name)
    
    
    
        
#----------------------------------------------------------------------
def gen_and_add_keypair():
    """"""
    

#----------------------------------------------------------------------
def stop_git_server():
    """"""
    