import datetime, hashlib, json, web
from .base import *

class ListCuratorRequest(object):
    NAME = "ListCuratorRequest"
    WEB_PARAMS = ['path','method']
    WEB_DATA = ['name', 'action', 'keys', 'comments']
    @classmethod
    def get_name(cls):
        return cls.NAME

    def get_default_args(self, error=None):
        default_web_params = getattr(self, 'WEB_PARAMS', [])
        default_web_data = getattr(self, 'WEB_DATA', [])
        kargs = {'error':error}
        for k in default_web_params:
            kargs[k] = getattr(web.ctx, k, None)

        data = web.input()
        for k in default_web_data:
            kargs[k] = getattr(data, k, None)
        return kargs

    def log_success(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Success: handled {path} {action} for {name}"
        GetLogMgr().log_format(fmt, classname=self.get_name(), **_kargs)

    def log_fail(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: Failed: handled {path} {action} for {name}: {error}"
        GetLogMgr().log_format(fmt, classname=self.get_name(), **_kargs)

    def log_event(self, **kargs):
        _kargs = self.get_default_args()
        _kargs.update(kargs)
        fmt = "{classname}: handling {path} {action} for {name}"
        GetLogMgr().log_format(fmt, classname=self.get_name(), **_kargs)

    def GET(self):
        data = web.input()
        data['all_elements'] = data.get('all_elements', False)
        name = data.get('name', None)
        action = data.get('action', None)
        self.log_event(path=web.ctx.path, method=web.ctx.method, **data)
        return self.handle_request(**data)

    def POST(self):
        data = web.data()
        try:
            data = json.loads(data)
        except:
            raise
        name = data.get('name', None)
        action = data.get('action', None)
        self.log_event(path=web.ctx.path, method=web.ctx.method, **data)
        return self.handle_request(**data)




class ListCreateClient(BaseHttpClient):
    URI_FMT = "/list/create"
    ACTION = 'create'
    NAME = "ListCreate"
    def __init__(self, host, port, name=None, auth_key=None, url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, auth_key=None, url_type='http'):
        x = cls(host, port, name, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListExistsClient(BaseHttpClient):
    URI_FMT = "/list/exists"
    ACTION = 'exists'
    NAME = "ListExists"
    def __init__(self, host, port, name, auth_key=None, url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, auth_key=None, url_type='http'):
        x = cls(host, port, name, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListListsClient(BaseHttpClient):
    URI_FMT = "/list/lists"
    ACTION = 'lists'
    NAME = "ListLists"
    def __init__(self, host, port, auth_key=None, url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format()
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'action':self.ACTION}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, auth_key=None, url_type='http'):
        x = cls(host, port, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListKeysClient(BaseHttpClient):
    URI_FMT = "/list/listkeys"
    ACTION = 'listkeys'
    NAME = "ListKeys"
    def __init__(self, host, port, name, auth_key=None, url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'action':self.ACTION}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, auth_key=None, url_type='http'):
        x = cls(host, port, name, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListKeysExistClient(BaseHttpClient):
    URI_FMT = "/list/keysexist"
    ACTION = 'keysexist'
    NAME = "ListKeys"
    def __init__(self, host, port, name, auth_key=None, keys=[], url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys':keys}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys=keys, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListKeysInfoClient(BaseHttpClient):
    URI_FMT = "/list/keysinfo"
    ACTION = 'keysinfo'
    NAME = "ListKeysInfo"
    def __init__(self, host, port, name, auth_key=None, keys=[], url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys':keys}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys=keys, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListAddKeysClient(BaseHttpClient):
    URI_FMT = "/list/addkeys"
    ACTION = 'addkeys'
    NAME = "ListAddKeys"
    def __init__(self, host, port, name, auth_key=None, keys=[], comments="", url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys':keys}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys=keys, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListRemoveKeysClient(BaseHttpClient):
    URI_FMT = "/list/removekeys"
    ACTION = 'removekeys'
    NAME = "ListRemoveKeys"
    def __init__(self, host, port, name, auth_key=None, keys=[], comments="", url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys':keys}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys=keys, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListAddKeysCommentsClient(BaseHttpClient):
    URI_FMT = "/list/addkeyscomments"
    ACTION = 'addkeyscomments'
    NAME = "ListAddKeysComments"
    def __init__(self, host, port, name, auth_key=None, keys_comments=[], url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys_comments':keys_comments}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys_comments=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys_comments=keys_comments, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListExpireKeysClient(BaseHttpClient):
    URI_FMT = "/list/expirekeys"
    ACTION = 'expirekey'
    NAME = "ListExpireKeys"
    def __init__(self, host, port, name, auth_key=None, keys=[], url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys':keys}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys=keys, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListUnexpireKeysClient(BaseHttpClient):
    URI_FMT = "/list/unexpirekeys"
    ACTION = 'unexpirekey'
    NAME = "ListUnexpireKeys"
    def __init__(self, host, port, name, auth_key=None, keys=[], url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type, auth_key=auth_key)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = {'auth_key':auth_key, 'name':name, 'action':self.ACTION, 'keys':keys}
        self.method = 'POST'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, keys=[], auth_key=None, url_type='http'):
        x = cls(host, port, name, keys=keys, auth_key=auth_key, url_type=url_type)
        return x.send_get_response()

class ListFileCommentsClient(BaseHttpClient):
    URI_FMT = "/list/filecomments/{name}"
    TAIL = "_comments.txt"
    NAME = "ListFileComments"
    ACTION = 'get_file_comments'
    def __init__(self, host, port, name, all_elements=False, url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = None
        self.method = 'GET'
        self.parameters = {'all_elements':all_elements}
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, all_elements=False, auth_key=None, url_type='http'):
        x = cls(host, port, name, all_elements=all_elements, url_type=url_type)
        return x.send_get_response()

class ListBasicFileClient(BaseHttpClient):
    URI_FMT = "/list/basicfile/{name}"
    TAIL = ".txt"
    NAME = "ListBasicFile"
    ACTION = 'get_file'
    def __init__(self, host, port, name, all_elements=False,  url_type="http"):
        BaseHttpClient.__init__(self, host, port, url_type=url_type)
        self.uri = self.URI_FMT.format(**{'name':name})
        self.set_header('Content-Type', 'application/json')
        self._datas = None
        self.parameters = {'all_elements':all_elements}
        self.method = 'GET'
        self.url = self.get_url()

    @classmethod
    def send_request(cls, host, port, name, all_elements=False, url_type='http'):
        x = cls(host, port, name, all_elements=all_elements, url_type=url_type)
        return x.send_get_response()


