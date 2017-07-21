#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ZSRPS Entry
  Created: 07/19/17
"""
import sys
import zmq
import logging

_DEFAULT_LOGGING_FMT = "[%(levelname)s] %(asctime)s [%(filename)s:%(funcName)s line:%(lineno)s]: %(message)s"
_LITE_LOGGING_FMT = "[%(levelname)s] %(asctime)s: %(message)s"
_DEFAULT_TIME_FMT = '[%d %b %Y %H:%M:%S]'

#
# config logger
#
logger = logging.getLogger('vikitx.zsrps')
logger.setLevel(logging.DEBUG)

# set handler and formatter
fmtr = logging.Formatter(fmt=_LITE_LOGGING_FMT, datefmt=_DEFAULT_TIME_FMT)
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(fmtr)
logger.addHandler(hdlr)

#
# config zmq
#
context = zmq.Context(io_threads=4)

from .. import threadpool
from .. import Ackpool

from ._server import ZSRPSServer
from ._client import ZSRPSClient
