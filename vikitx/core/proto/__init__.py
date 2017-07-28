from ..workpool import threadpool, task
from ..ackutil import Ackpool
from ..workflow import Workflow
from ..workpool import _utils as thread_utils

from .zsrps import ZSRPSClient
from .zsrps import ZSRPSServer
from . import interfaces

########################################################################
class ZServerBase(interfaces.UserClientManageIf, ZSRPSServer):
    """ZServer User interfaces
    
    Methods:
    --------

    get_available_clients():
        get ids of available cliends
    
    remove_client(client_id):
        remove client by id
    
    get_client_scope(client_id):
        get information about client
    """
