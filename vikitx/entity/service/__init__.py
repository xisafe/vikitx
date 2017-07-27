
from .. import get_new_threadpool

from ._service import ServiceWraperInProcess
from ._service import ServiceWraperInThread
from ._service import _Service

Service = ServiceWraperInProcess