import datetime, hashlib, json, web
from .clients import *


class ListCuratorClient(object):
    def __init__(self, host, port, auth_key=None, url_type='http'):
        self.host = host
        self.port = port
        self.auth_key = auth_key
        self.url_type = url_type

    def listlists(self):
        return ListListsClient.send_request(self.host, self.port, auth_key=self.auth_key, url_type=self.url_type)

    def listcreate(self, name):
        return ListCreateClient.send_request(self.host, self.port, name=name, auth_key=self.auth_key, url_type=self.url_type)

    def listexists(self, name):
        return ListExistsClient.send_request(self.host, self.port, name=name, auth_key=self.auth_key, url_type=self.url_type)

    def listaddkeys(self, name, keys):
        return ListAddKeysClient.send_request(self.host, self.port, name=name, keys=keys, auth_key=self.auth_key, url_type=self.url_type)

    def listaddkeyscomments(self, name, keys_comments):
        return ListAddKeysCommentsClient.send_request(self.host, self.port, name=name, keys_comments=keys_comments, auth_key=self.auth_key, url_type=self.url_type)

    def listremovekeys(self, name, keys):
        return ListRemoveKeysClient.send_request(self.host, self.port, name=name, keys=keys, auth_key=self.auth_key, url_type=self.url_type)

    def listkeysexist(self, name, keys):
        return ListKeysExistClient.send_request(self.host, self.port, name=name, keys=keys, auth_key=self.auth_key, url_type=self.url_type)

    def listkeysinfo(self, name, keys):
        return ListKeysInfoClient.send_request(self.host, self.port, name=name, keys=keys, auth_key=self.auth_key, url_type=self.url_type)

    def listexpirekeys(self, name, keys):
        return ListExpireKeysClient.send_request(self.host, self.port, name=name, keys=keys, auth_key=self.auth_key, url_type=self.url_type)

    def listunexpirekeys(self, name, keys):
        return ListUnexpireKeysClient.send_request(self.host, self.port, name=name, keys=keys, auth_key=self.auth_key, url_type=self.url_type)

    def get_basic(self, name, all_elements=False):
        return ListBasicFileClient.send_request(self.host, self.port, name=name, all_elements=all_elements, url_type=self.url_type)
        
    def get_full(self, name, all_elements=False):
        return ListFileCommentsClient.send_request(self.host, self.port, name=name, all_elements=all_elements, url_type=self.url_type)
