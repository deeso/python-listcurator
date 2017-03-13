import datetime, hashlib, json, web, os
from ..lists.list import List
#from listcurator.lists.list import List
from ..service.auth import Authenticator
from ..service.log import Logger, LOGGER_NAME, LOG_FORMAT, LOG_LEVEL

AUTH_USERS = True
AUTH_ACTIONS = ['create', 'addkeys', 'addkeyscomments', 'removekeys', 'expirekeys', 'unexpirekeys']
FULL_TXT = "_full.txt"
TXT = ".txt"
ListCuratorUrls = [
   '/list/create', "ListCreate",
   '/list/exists', "ListExists",
   '/list', "ListLists",
   '/list/lists', "ListLists",
   '/list/listkeys', "ListKeys",
   '/list/removekeys', "ListRemoveKeys",
   '/list/addkeys', "ListAddKeys",
   '/list/addkeyscomments', "ListAddKeysComments",
   '/list/keysexist', "ListKeysExist",
   '/list/keysinfo', "ListKeysInfo",
   '/list/expirekeys', "ListExpireKeys",
   '/list/unexpirekeys', "ListUnexpireKeys",
   # check for txt
   '/list/filecomments/(.+_comments\.txt)', "ListFileComments",
   '/list/basicfile/(.+\.txt)', "ListBasic",
   # name just provided
   '/list/filecomments/(.+)', "ListFileComments",
   '/list/basicfile/(.+)', "ListBasic",
]




AUTH_MGR = None
def InitializeAuth(sourcetype="rawconfig", source=None, auth_users=True):
    global AUTH_MGR, AUTH_USERS
    AUTH_USERS = auth_users
    if sourcetype == 'rawconfig' and not source is None:
        AUTH_MGR = Authenticator(rawconfig=source, source=sourcetype)
        return AUTH_MGR
    raise Exception("Source (%s) not supported"%sourcetype)
    

LOG_MGR = None
def InitializeLogMgr(logger_name=LOGGER_NAME, log_level=LOG_LEVEL, create_console=True, log_file=None):
    global LOG_MGR
    if LOG_MGR is None:
        LOG_MGR = Logger(logger_name=logger_name, log_level=log_level, create_console=create_console, log_file=log_file)
    return LOG_MGR

def GetLogMgr():
    global LOG_MGR
    return InitializeLogMgr()
        

def GetAuthMgr():
    global AUTH_MGR
    if AUTH_MGR is None:
        raise Exception("Failed to get the Authenticator")
    return AUTH_MGR

LIST_MGR = None
def GetListMgr():
    global LIST_MGR
    if LIST_MGR is None:
        raise Exception("Failed to get the ListCurator")
    return LIST_MGR

def InitializeListMgr(sqlitefile=None, working_location=None):
    global LIST_MGR
    if LIST_MGR is None:
        LIST_MGR = ManagedLists(sqlitefile=sqlitefile, working_location=working_location)
    return LIST_MGR

class ManagedLists(object):
    NAME = "ManagedLists"
    @classmethod
    def get_name(cls):
        return cls.NAME

    LISTS = None

    def __init__(self, sqlitefile=None, create_individual_files=True, working_location=None):
        if ManagedLists.LISTS is None:
            ManagedLists.LISTS = {}
        self.lists = self.LISTS
        self.sqlitefile = None # force creating individual files for each list
        self.working_location = working_location

    def list_names(self):
        return self.lists.keys()

    def listlists(self):
        rsp = {'error':None, "action":"lists", 'lists':self.lists.keys()}
        return rsp

    def listcreate(self, name):
        rsp = {'error':None, "name":name, "action":"create", 'result':False}
        if name in self.lists:
            rsp['error'] = "list already exists"
        else:
            rsp['result'] = True
            fmt = "{classname} creating {name} in {working_location}/{name}.db"
            GetLogMgr().log_format(fmt, classname=self.get_name(), name=name, working_location=self.working_location)
            l = List(name, sqlitefile=self.sqlitefile, working_location=self.working_location)
            self.lists[name] = l
        return rsp

    def listkeysinfo(self, name, keys):
        rsp = {'error':None, "name":name, "action":"keysinfo", 'result':{}}
        if name in self.lists:
            rsp['result'] = self.lists[name].keysinfo(keys)
        else:
            rsp['error'] = "list does not exist"
        return rsp

    def listexists(self, name):
        rsp = {'error':None, "name":name, "action":"exists", 'result':False}
        rsp['result'] = name in self.lists
        if not name in self.lists:
            rsp['error'] = "list does not exist"
            rsp['result'] = name in self.lists
        return rsp

    def listaddkeys(self, name, keys):
        rsp = {'error':None, "name":name, "action":"addkeys", 'result':[]}
        if name in self.lists:
            rsp['result'] = self.lists[name].addkeys(keys)
        else:
            self.listcreate(name)
            rsp['result'] = self.lists[name].addkeys(keys)
        return rsp

    def listremovekeys(self, name, keys):
        rsp = {'error':None, "name":name, "action":"removekeys", 'result':[]}
        if name in self.lists:
            rsp['result'] = self.lists[name].removekeys(keys)
        else:
            rsp['error'] = 'list does not exist'
        return rsp

    def listaddkeyscomments(self, name, keys_comments):
        rsp = {'error':None, "name":name, "action":"addkeys", 'result':[]}
        if name in self.lists:
            rsp['result'] = self.lists[name].addkeyscomments(keys_comments)
        else:
            self.listcreate(name)
            rsp['result'] = self.lists[name].addkeyscomments(keys_comments)
        return rsp

    def listkeysexist(self, name, keys):
        rsp = {'error':None, "name":name, "action":"keysexist", 'result':[]}
        if name in self.lists:
            rsp['result'] = self.lists[name].keysexist(keys)
        else:
            rsp['error'] = 'list does not exist'
        return rsp

    def listexpirekeys(self, name, keys):
        rsp = {'error':None, "name":name, "action":"expirekeys", 'result':[]}
        if name in self.lists:
            rsp['result'] = self.lists[name].expirekeys(keys)
        else:
            rsp['error'] = 'list does not exist'
        return rsp

    def listunexpirekeys(self, name, keys):
        rsp = {'error':None, "name":name, "action":"unexpirekeys", 'result':[]}
        if name in self.lists:
            rsp['result'] = self.lists[name].unexpirekeys(keys)
        else:
            rsp['error'] = 'list does not exist'
        return rsp

    def get_basic(self, name, all_elements=False):
        results = []
        return "" if not name in self.lists else self.lists[name].get_data(all_elements=all_elements)
        
    def get_full(self, name, all_elements=False):
        return "" if not name in self.lists else self.lists[name].get_full(all_elements=all_elements)

    def action_requires_auth(self, action):
        return action in self.AUTH_ACTIONS
    

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

    def GET(self, name=None):
        data = web.input()
        data['all_elements'] = data.get('all_elements', False)
        name = data.get('name', name)
        action = data.get('action', None)
        if AUTH_USERS and action in AUTH_ACTIONS:
            auth_key = data.get('auth_key', None)
            user = data.get('user', None)
            password = data.get('password', None)
            try:
                GetAuthMgr().authenticate(auth_key=auth_key, user=user, password=password)
            except:
                raise web.forbidden("Authkey not valid")
        self.log_event(path=web.ctx.path, method=web.ctx.method, name=name, **data)
        return self.handle_request(name=name, **data)

    def POST(self, name=None):
        data = web.data()
        try:
            data = json.loads(data)
        except:
            raise
        name = data.get('name', name)
        action = data.get('action', None)
        self.log_event(path=web.ctx.path, method=web.ctx.method, **data)
        if AUTH_USERS and action in AUTH_ACTIONS:
            auth_key = data.get('auth_key', None)
            user = data.get('user', None)
            password = data.get('password', None)
            try:
                GetAuthMgr().authenticate(auth_key=auth_key, user=user, password=password)
            except:
                raise web.forbidden("Authkey not valid")

        return self.handle_request(**data)


class ListCreate(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        if name is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listcreate(name))

class ListExists(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        if name is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listexists(name))


class ListLists(ListCuratorRequest):
    def handle_request(self, **data):
        action = data.get('action', None)
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listlists())

class ListKeys(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        if name is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listkeys(name))

class ListAddKeys(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys = data.get('keys', None)
        if keys is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listaddkeys(name, keys))

class ListAddKeysComments(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys_comments = data.get('keys_comments', None)
        if keys_comments is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listaddkeyscomments(name, keys_comments))

class ListRemoveKeys(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys = data.get('keys', None)
        if keys is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listremovekeys(name, keys))

class ListKeysExist(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys = data.get('keys', None)
        if name is None or keys is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listkeysexist(name, keys))

class ListKeysInfo(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys = data.get('keys', None)
        if name is None or keys is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listkeysinfo(name, keys))

class ListExpireKeys(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys = data.get('keys', None)
        if name is None or keys is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listexpirekeys(name, keys))

class ListUnexpireKeys(ListCuratorRequest):
    def handle_request(self, **data):
        name = data.get('name', None)
        action = data.get('action', None)
        keys = data.get('keys', None)
        if name is None or keys is None:
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'application/json')
        return json.dumps(GetListMgr().listunexpirekeys(name, keys))


class ListFileComments(ListCuratorRequest):
    def handle_request(self, name, all_elements=False, **data):
        if name is None or not name in GetListMgr().list_names():
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'text/plain; charset=us-ascii')
        return GetListMgr().get_full(name=name, all_elements=all_elements)


class ListBasic(ListCuratorRequest):
    def handle_request(self, name=None, all_elements=False, **data):
        print name, GetListMgr().list_names()
        if name is None or not name in GetListMgr().list_names():
            raise web.notfound()
        self.log_event()
        web.header('Content-Type', 'text/plain; charset=us-ascii')
        return GetListMgr().get_basic(name, all_elements=all_elements) 
