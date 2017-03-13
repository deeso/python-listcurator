from ConfigParser import RawConfigParser


class User(object):
    def __init__(self, uname, auth_key):
        self.uname = uname
        self.auth_key = auth_key

class AuthenticatorInterface(object):
    def authenticate(self, user=None, auth_key=None, **kargs):
        raise Exception("Not implemented")

class Authenticator(AuthenticatorInterface):
    USERS = "users"
    USER_LIST = "user_list"
    USER_AUTH = "%s_auth"
    def __init__(self, source=None, rawconfig=None, **kargs):
        self.source = source
        self.rawconfig = rawconfig
        self.users = {}
        if self.source is None:
            raise Exception("Invalid authentication source")

        
        if self.rawconfig:
            rc = RawConfigParser()
            rc.read(self.rawconfig)
            if not rc.has_section(self.USERS):
                raise Exception("No users section specified in config file")
            rc_items = dict(rc.items(self.USERS))
            user_list = rc_items.get(self.USER_LIST, []).split()
            for uname in user_list:
                if len(uname) == 0:
                    continue
                auth_key = rc_items.get(self.USER_AUTH%uname, None)
                if auth_key is None:
                    continue
                u = User(uname, auth_key)
                self.users[auth_key] = u

    def authenticate(self, user=None, auth_key=None, password=None, **kargs):
        if auth_key is None:
            raise Exception('Authorization Key needs to be set')
        return auth_key in self.users
