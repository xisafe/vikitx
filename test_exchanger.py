#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test for exchanger
  Created: 07/30/17
"""

import unittest
import zmq

from vikitx.core.workpool.task import Task
from vikitx.core.proto.zed import Exchanger

########################################################################
class ExchangerTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_exchanger(self):
        """"""
        routing_key = 'testkey'
        exchanger = Exchanger(id='exchanger', host='127.0.0.1', backend_port=3424)
        exchanger.regist_entry(9001)
        exchanger.regist_router(routing_key, 9002)
        exchanger.start()
        
        ctx = zmq.Context()
        sock = ctx.socket(zmq.REQ)
        sock.connect('tcp://127.0.0.1:9001')
        sock.send_pyobj({'routing_key':'testkey',
                        'message':{'this':'is a test message!',
                                   'token':''}})
        
        print('TEEEEST RECVED FROM : {}'.format(sock.recv_pyobj()))
        
        #
        # task
        #
        _t = Task(exchanger.stop)
        _t.call_later(5)
        
        exchanger.join()


    
    

if __name__ == '__main__':
    unittest.main()