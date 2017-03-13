import json
from datetime import timedelta, datetime
from random import randint
from requests import Request, Session
from ..service.log import *

LOG_MGR = None
def InitializeLogMgr(logger_name=LOGGER_NAME, log_level=LOG_LEVEL, create_console=True, log_file=None):
    global LOG_MGR
    if LOG_MGR is None:
        LOG_MGR = Logger(logger_name=logger_name, log_level=log_level, create_console=create_console, log_file=log_file)
    return LOG_MGR

def GetLogMgr():
    global LOG_MGR
    return InitializeLogMgr()


class BaseJsonResponse(dict):
    NAME = "BaseJsonResponse"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def get_default_args(self):
        return {}

    def log_success(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Success: handled {path} {action} for {name}"
        GetLogMgr().log_format(fmt, **_kargs)

    def log_fail(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Failed: handled {path} {action} for {name}: {error}"
        GetLogMgr().log_format(fmt, **_kargs)

    def log_event(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: handling {path} {action} for {name}"
        GetLogMgr().log_format(fmt, **_kargs)

    def __init__(self, response=None, json_str=None, json_dict=None, **kargs):
        dict.__init__(self)
        self.response = response
        self.update_from_json(json_str)
        self.update_from_dict(json_dict)
        self.update_from_dict(kargs)
        for k in self.__dict__.keys():
            setattr(self, "get_%s", lambda self: getattr(self, k, None))
        
    
    def update_from_json(self, json_str):
        if json_str is None:
            return
        data = json.loads(json_str)
        self.update_from_dict(data)

    def update_from_dict(self, data):
        if data is None:
            return
        self.update(data)

    def data_string(self):
        return self.response.text


class BaseResponse(dict):
    NAME = "BaseResponse"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def get_default_args(self):
        return {}

    def log_success(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Success: handled {path} {action} for {name}"
        GetLogMgr().log_format(fmt, **_kargs)

    def log_fail(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Failed: handled {path} {action} for {name}: {error}"
        GetLogMgr().log_format(fmt, **_kargs)

    def log_event(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: handling {path} {action} for {name}"
        GetLogMgr().log_format(fmt, **_kargs)

    def __init__(self, response=None, **kargs):
        dict.__init__(self)
        self.response = response
        self.data = response.text

    def data_string(self):
        return self.response.text

URL_FMT = "{url_type}://{host}:{port}{uri}"
class BaseHttpClient(object):
    NAME = "BaseJsonResponse"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def get_default_args(self):
        return {}

    def log_success(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Success: handled {path} {action} for {name}"
        GetLogMgr().log_format(fmt, **_kargs)

    def log_fail(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Failed: handled {path} {action} for {name}: {error}"
        GetLogMgr().log_format(fmt, **_kargs)

    def log_event(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: handling {path} {action} for {name}"
        GetLogMgr().log_format(fmt, **_kargs)

    def __init__(self, host, port, **kargs):
        self.host = host
        self.port = port
        self.headers = {}
        self.method = "GET"

        for k,v in kargs.items():
            setattr(self, k, v)
            #setattr(self, "get_%s", lamdbda self: getattr(self, k, None))

    def set_header(self, header, value):
        self.headers[header] = value
        
    def get_url(self, fmt=URL_FMT, uri="/", url_type="https"):
        fmt = getattr(self, 'fmt', fmt)
        kargs = {}
        kargs['uri'] = getattr(self, 'uri', uri)
        kargs['url_type'] = getattr(self, 'url_type', url_type)
        kargs['port'] = self.port
        kargs['host'] = self.host
        print kargs
        return fmt.format(**kargs)

    def _send_request(self, method, url="", data=None, params=None, retrys=3, auth=None, headers={}):
        url = getattr(self, 'url', url)
        data = getattr(self, '_datas', data)
        params = getattr(self, 'params', params)
        retrys = getattr(self, 'retrys', retrys)
        auth = getattr(self, 'auth', auth)
        headers = getattr(self, 'headers', headers)
        
        msg = "{classname}: Sending {path} {action} for {name}"
        name = None if data is None else data.get('name', None)
        GetLogMgr().debug(msg, action=self.ACTION, classname=self.get_name(), path=url, name=name)
        
        if method == 'POST':
            data = json.dumps(data) if not data is None else {}

        req = Request(method, url, params=params, data=data, headers=headers, auth=auth)
        prepped = req.prepare()
        # print prepped.body
        rsp = None
        session = Session()
        cnt = 0
        
        while cnt < retrys:
            
            try:
                rsp = session.send(prepped, verify=False, proxies=getattr(self, 'proxies', {}))
                msg = "{classname}: Send succeeded {path} {action} for {name}"
                GetLogMgr().debug(msg, action=self.ACTION, classname=self.get_name(), path=url, name=name, cnt=cnt)
                break
            except:
                msg = "{classname}: Failed send {path} {action} for {name}: retrys = {cnt}"
                GetLogMgr().debug(msg, action=self.ACTION, classname=self.get_name(), path=url, name=name, cnt=cnt)
                cnt += 1
                if cnt >= retrys:
                    raise


        return rsp

    def send_get_response(self):
        rsp = self._send_request(self.method)
        json_str = None
        setattr(self, 'last_response', rsp)
        if self.method == 'POST' and rsp.status_code == 200:
            json_str = rsp.text
            return BaseJsonResponse(response=rsp, json_str=json_str)
        elif self.method == 'POST':
            return BaseJsonResponse(response=rsp, json_str=json_str)
        else:
            return BaseResponse(response=rsp)



