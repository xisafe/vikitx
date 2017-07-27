#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ServiceNode Define
  Created: 07/27/17
"""

import collections
import warnings
import random
import zmq
import multiprocessing

from .. import thread_utils
from .. import interfaces
from ..service import ServiceWraperInProcess, ServiceWraperInThread, _Service
from . import __excs as excs

SMODE_THREAD = 'SMODE_THREAD'
SMODE_PROCESS = 'SMODE_PROCESS'

_SMODES = [SMODE_PROCESS, SMODE_THREAD]

_Service_Mode_Table = {
    SMODE_PROCESS: ServiceWraperInProcess,
    SMODE_THREAD: ServiceWraperInThread,
}


#
# define state
#
state_INIT = 'init'
state_WORKING = 'working'
state_END = 'end'

_TRANS_TABLE = {
    state_INIT: [state_WORKING,],
    state_WORKING: [state_END, state_WORKING]
}

########################################################################
class ServiceNodeConfig:
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.service_mode = SMODE_PROCESS




########################################################################
class ServiceNode(interfaces.EntityIf, 
                  interfaces.ExecuteTaskIf, 
                  interfaces.ServiceManageIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, config=None):
        """Constructor"""
        self._id = id
        self._state = state_INIT
        self.config = config if config else ServiceNodeConfig()

        #
        # record service by service_id
        #
        self._services = collections.defaultdict(dict)

    @property
    def state(self):
        """"""
        return self._state
    
    @state.setter
    def state(self, value):
        """"""
        assert value in _TRANS_TABLE[self.state], 'invalid state transformation'
        self._state = value

    @property    
    def id(self):
        """"""
        return self._id

    #----------------------------------------------------------------------
    def get_pipe(self):
        """Get Pipe <read-only> - <write-only>"""
        
        return multiprocessing.Pipe(False)
        

    #
    # manager service
    #
    #----------------------------------------------------------------------
    def start_service(self, service_id, target=None, config=None):
        """Start up a service with config

        Parameters:
        -----------
        service_id: str
            service_id is the id for service

        target: function
            the core function for service

        config: ServiceNodeConfig
            temp config for current service

        """
        config = config if config else self.config
        assert isinstance(config, ServiceNodeConfig)
        assert service_id not in self._services, "existed service_id"

        #
        # prepare
        #
        ServiceClass = _Service_Mode_Table[config.service_mode]
        task_recv, task_send = self.get_pipe() 
        result_recv, result_send = self.get_pipe()

        #
        # build service
        #
        service_entity = ServiceWraperInProcess(service_id, target,
                                                task_pipe=task_recv,
                                                result_pipe=result_send)

        #
        # record service and start service
        #
        self.regist_service(service_id, service_entity, task_send, result_recv)
        service_entity.start()


    #----------------------------------------------------------------------
    def regist_service(self, sid, service_entity, task_sender, result_receiver):
        """Regist service in ServiceNode

        Parameters:
        -----------
        sid: str
            service id

        service_entity: _Service
            service entity
            
        task_sender: Pipe <wirte-only>
            send task to service 
        
        result_receiver: Pipe <read-only>
            recv result from service
            
        """
        assert isinstance(service_entity, _Service)
        if sid not in self._services:
            self._services[sid] = {}
        
        self._services[sid]['entity'] = service_entity
        self._services[sid]['task_sender'] = task_sender
        self._services[sid]['result_receiver'] = result_receiver

    #----------------------------------------------------------------------
    def remove_service(self, sid):
        """Stop Service Remove the service, """
        if sid in self._services:
            #
            # stop service
            #
            _svc_entity = self.get_service(sid)
            _svc_entity.stop()
            
            #
            # delete service recording
            #
            del self._services[sid]
        else:
            return False

    #----------------------------------------------------------------------
    def get_service(self, sid):
        """Get Service Entity by sid

        Parameters:
        -----------
        sid: str
            service id
        """
        return self._services.get(sid).get('entity')

    #----------------------------------------------------------------------
    def destory_service(self, sid):
        """Destory the service (ServiceWraperInProcess)"""
        _svc = self.get_service(sid)
        if _svc:
            if isinstance(_svc, ServiceWraperInProcess):
                _svc.terminate()
            else:
                warnings.warn('destory just available for ServiceWraperInProcess!')

    #----------------------------------------------------------------------
    def stop_service(self, sid):
        """Just stop service and Remove it, the same with self.remove_service"""
        self.remove_service(sid)
    
    #----------------------------------------------------------------------
    def get_service_channal(self, service_id):
        """"""
        _sd = self._services.get(service_id)
        if _sd:
            return _sd.get('task_sender')
        else:
            return None
        

    #
    # execute task interface
    #
    #----------------------------------------------------------------------
    def execute(self, service_id, task_id, args=(), kwargs={}):
        """"""
        assert service_id in self._services, 'no such service_id'
        self.sendto(service_id, (task_id, args, kwargs))
        #_svc = self.get_service(service_id)
        #if _svc:
            #_svc.execute(task_id, args, kwargs)
    
    #----------------------------------------------------------------------
    def result_callback(self, task, result):
        """"""
        print('GOT:{} RESULT:{}'.format(task, result))
    
    #----------------------------------------------------------------------
    def sendto(self, service_id, msg):
        """"""
        ch = self.get_service_channal(service_id)
        if ch:
            ch.send(msg)
        else:
            raise excs.ServiceNodeError('no such channal or no such service_id')
        
    #
    # main loop
    #
    #----------------------------------------------------------------------
    def __main_loop(self):
        """"""
        #
        # main loop
        #
        while self.state == state_WORKING:
            #
            # collect result
            #
            for result_pipe in [i for i in self.get_all_result_pipe() if i.poll()]:
                task_id, result = result_pipe.recv()
                self.result_callback(task_id, result)
                    
                    
    #----------------------------------------------------------------------
    def start(self):
        """Start the mainloop(collecting result)"""
        self.state = state_WORKING
        
        self._thread_mainloop = thread_utils.start_thread(
            '{}-mainloop'.format(self.id),\
            True,
            self.__main_loop,
        )
        
    #----------------------------------------------------------------------
    def join(self):
        """"""
        assert self.state == state_WORKING, 'plz start servicenode first'
        self._thread_mainloop.join()
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        for _sid in self._services.keys():
            self.remove_service(_sid)
        
        self.state = state_END
        
        self._thread_mainloop.join()
    
    #----------------------------------------------------------------------
    def get_all_result_pipe(self):
        """"""
        def get_result_pipe(id):
            return self._services.get(id).get('result_receiver')
        return map(get_result_pipe, self._services)