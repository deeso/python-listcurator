import unittest, time
import web, argparse, os, logging, sys
from multiprocessing import Process
import web, argparse, os, logging, sys
from ..client.listcurator import *
from ..service.listcurator import *
from sqlalchemy import *


PORT = 45078
HOST = '0.0.0.0'
ML_SAVE_DIR = 'managed_lists'
SAVE_DIR = os.path.join(os.getcwd(), ML_SAVE_DIR)
LOGGER_NAME = "managed_lists_webservice"
ML_LOG_FILE = "managed_lists_webservice.log"
ML_SQLITE_FILE = "managed_lists.db"
WORKING_DIR = "/tmp"
CONFIG_FILE = "./test_data/test1.config"


TEST_LIST = 'abc8080'

class AppOverride(web.application):
    def run(self, host=HOST, port = PORT, *middleware):
        return web.httpserver.runsimple(self.wsgifunc(*middleware), (host, port))

def run_server(host, port, config_file, working_location, sqlitefile=None):
    global AUTH_USERS
    os.stat(config_file)
    AUTH_USERS = False
    log_mgr = InitializeLogMgr()
    auth_mgr = InitializeAuth(sourcetype="rawconfig", source=config_file, auth_users=False)
    list_mgr = InitializeListMgr(sqlitefile, working_location=working_location)
    AUTH_USERS = False
    app = AppOverride(ListCuratorUrls, globals())
    app.run(host=host, port=port)


class FixturesTest(unittest.TestCase):

    def setUp(self):
        global HOST, PORT, CONFIG_FILE, WORKING_DIR
        print('In setUp()')
        self.port = getattr(self, 'port', PORT)
        self.port +=1 
        setattr(self, 'port', self.port)
        self.server_process = None
        self.server_process = Process(target=run_server, args=(HOST, self.port, CONFIG_FILE, WORKING_DIR, None))
        self.server_process.start()
    
    def test_listremovekeys(self):
        global HOST, PORT

        print('In test_listaddkeys()')
        list_name = TEST_LIST
        time.sleep(1)
        a = ListCuratorClient(HOST, getattr(self, 'port', PORT))
        a.listcreate(list_name)
        db_exists = False
        db_filename = os.path.join(WORKING_DIR, list_name+'.db') 
        try:
            os.stat(db_filename)
            db_exists = True
        except:
            pass

        test_keys = ['123', 'rtf', 'why']
        test_remove_keys = ['abc', '123', 'xyz']
        test_final_keys = ['rtf', 'why']
        rsp1 = a.listkeysexist(list_name, test_keys)
        rdict = {}
        has_seen = set()
        result_dict = rsp1['result'] 
        for key in result_dict:
            self.assertFalse(key in has_seen)
            has_seen.add(key)
            self.assertFalse(result_dict[key])
            self.assertTrue(key in test_keys)

        rsp2 = a.listaddkeys(list_name, test_keys)
        has_seen = set()

        result_dict = rsp2['result'] 
        for key in result_dict:
            # print rd
            self.assertFalse(key in has_seen)
            has_seen.add(key)
            self.assertTrue(result_dict[key])
            self.assertTrue(key in test_keys)

        rsp3 = a.listaddkeys(list_name, test_keys)
        has_seen = set()
        result_dict = rsp3['result']
        # print rsp3
        for key in result_dict:
            self.assertFalse(key in has_seen)
            has_seen.add(key)
            self.assertFalse(result_dict[key], "Added a key that existed: %s"%key)
            self.assertTrue(key in test_keys)

        rsp4 = a.listkeysexist(list_name, test_keys)
        has_seen = set()
        result_dict = rsp4['result'] 
        for key in result_dict:
            self.assertFalse(key in has_seen)
            has_seen.add(key)
            self.assertTrue(result_dict[key])
            self.assertTrue(key in test_keys)

        rsp5 = a.listremovekeys(list_name, test_remove_keys)
        has_seen = set()
        result_dict = rsp5['result']
        # print rsp3
        for key in result_dict:
            self.assertFalse(key in has_seen)
            has_seen.add(key)
            if not key in test_keys:
                self.assertFalse(result_dict[key], "Removed a key that did not exist: %s"%key)
            elif key in test_keys:
                self.assertTrue(result_dict[key], "Did not remove a a key that existed: %s"%key)


        rsp6 = a.listkeysexist(list_name, test_keys)
        has_seen = set()
        result_dict = rsp6['result'] 
        for key in result_dict:
            self.assertFalse(key in has_seen)
            has_seen.add(key)
            if key in test_final_keys:
                self.assertFalse(key in test_remove_keys, "Found a key (%s) the should not be in keys"%key)
            if key in test_remove_keys:
                self.assertFalse(result_dict[key], "Found a deleted key")

        rsp7 = a.get_basic(list_name).data_string()
        self.assertEqual(rsp7, "\n".join(test_final_keys))

        # if db_exists:
        #     os.remove(db_filename)
        self.assertEqual(db_exists, True)

    def tearDown(self):
        print('In tearDown()')
        if not self.server_process is None:
            self.server_process.terminate()

        list_name = TEST_LIST
        db_filename = os.path.join(WORKING_DIR, list_name+'.db') 
        try:
            os.stat(db_filename)
            os.remove(db_filename)
        except:
            pass

    def test(self):
        print('in test()')
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
