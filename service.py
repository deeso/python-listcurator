import web, argparse, os, logging, sys
from listcurator.service.listcurator import *
from listcurator.service.listcurator import *
from sqlalchemy import *

PORT = 45000
HOST = '0.0.0.0'
ML_SAVE_DIR = 'managed_lists'
SAVE_DIR = os.path.join(os.getcwd(), ML_SAVE_DIR)
LOGGER_NAME = "managed_lists_webservice"
ML_LOG_FILE = "managed_lists_webservice.log"

ML_SQLITE_FILE = "managed_lists.db"

LOGGER_LOCATION = os.path.join(os.getcwd(), ML_LOG_FILE) 
parser = argparse.ArgumentParser(description="List Management Web Service")
parser.add_argument('-host', default=HOST, type=str)
parser.add_argument('-port', default=PORT, type=int)
parser.add_argument('-working_dir', default=SAVE_DIR, type=str)
parser.add_argument('-save_loc', default=None, type=str)
parser.add_argument('-sqlite_db', default=None, type=str)
parser.add_argument('-sqlite_uri', default=None, type=str)
parser.add_argument('-log', default=None, type=str)
parser.add_argument('-log_console', default=False, action="store_true")
parser.add_argument('-config_file', default=None, type=str)
parser.add_argument('-no_auth_users', default=False, action="store_true")


class AppOverride(web.application):
    def run(self, host=HOST, port = PORT, *middleware):
        return web.httpserver.runsimple(self.wsgifunc(*middleware), (host, port))

def run_server(host, port, config_file, working_location, sqlitefile, auth_users=True):
    log_mgr = InitializeLogMgr()
    auth_mgr = InitializeAuth(sourcetype="rawconfig", source=config_file, auth_users=auth_users)
    list_mgr = InitializeListMgr(sqlitefile, working_location=working_location)
    app = AppOverride(ListCuratorUrls, globals())
    app.run(host=host, port=port)

if __name__ == "__main__":
    args = parser.parse_args()
    args.log = os.path.join(args.working_dir, ML_LOG_FILE) if args.log is None else args.log
    args.save_loc = os.path.join(args.working_dir, ML_SAVE_DIR) if args.save_loc is None \
                                 else args.save_loc
    
    AUTH_USERS = args.no_auth_users
    sqlitefile = args.sqlite_db if not args.sqlite_db is None \
                              else os.path.join(args.working_dir, ML_SQLITE_FILE) 
    use_uri = True if not args.sqlite_uri is None else False
    sqlitecon = None
    
    run_server(args.host, args.port, args.config_file, args.working_dir, sqlitefile, auth_users=not args.no_auth_users)