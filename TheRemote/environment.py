def get_options(args):
    return {}

class Env(object):

    _appname = 'TheRemote'

    _app = None
    _encoding = 'UTF-8'
    _debug = False
    _dev = False
    _settings = dict()
    _database = None
    _cache = None
    _options = None
    _args = None
    _quiet = None
    _daemonized = False


    _app_dir = ""
    _data_dir = ""
    _cache_dir = ""
    _db = ""
    _log_path = ""


    @staticmethod
    def setting(name):
        return name