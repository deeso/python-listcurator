import unittest, time
import web, argparse, os, logging, sys, time
from multiprocessing import Process
import web, argparse, os, logging, sys
from ..client.listcurator import *
from ..service.listcurator import *
from sqlalchemy import *


PORT = 45008
HOST = '0.0.0.0'
ML_SAVE_DIR = 'managed_lists'
SAVE_DIR = os.path.join(os.getcwd(), ML_SAVE_DIR)
LOGGER_NAME = "managed_lists_webservice"
ML_LOG_FILE = "managed_lists_webservice.log"
ML_SQLITE_FILE = "managed_lists.db"
WORKING_DIR = "/tmp"
CONFIG_FILE = "./test_data/test1.config"


TEST_LIST = 'abc9090'

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
    
    def TEST_LIST(self):
        global HOST, PORT, TEST_LIST

        print('In TEST_LIST()')
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
