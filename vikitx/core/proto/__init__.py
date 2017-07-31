from ..workpool import threadpool, task
from ..ackutil import Ackpool
from ..workflow import Workflow
from ..workpool import _utils as thread_utils


#
# ZSRPS
#
from .zsrps import ZSRPSClient
from .zsrps import ZSRPSServer
from . import interfaces

########################################################################
class ZServerBase(interfaces.UserClientManageIf, ZSRPSServer):
    """ZServer User interfaces
    
    Methods:
    --------
    def get_available_clients():
        get ids of available cliends
    
    def remove_client(client_id):
        remove client by id
    
    def get_client_scope(client_id):
        get information about client
    """

########################################################################
class ZClientBase(interfaces.UserClientIf, ZSRPSClient):
    """
    
    Methods:
    --------
    def handle_action(action):
        handle action and return information, if the action execute error,
        you should return a state and extrainfomation(optional)::
            return state, extra
    
    """
    

#
# ZED
#
from .zed import Exchanger