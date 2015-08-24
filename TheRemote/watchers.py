import pywatchman
from theremote.core.utils.daemon import Daemon


class BaseWatcher(object):
    def __init__(self, name, path, options=None):
        self.name = name
        self.path = path
        self.options = options or {}
        self.client = pywatchman.client()
        self.subscription = self.client.query('subscribe', path, name, options)
        self.daemon = Daemon('/tmp/{}.pid'.format(self.name))
        self.daemon.daemonize()

        while True:
            try:
                data = self.client.receive()
                self.handler(data)
            except NotImplementedError, pywatchman.WatchmanError:
                raise
            except:
                pass

    def handler(self, data):
        raise NotImplementedError('You must define a handler')


class FileWatcher(BaseWatcher):
    def handler(self, data):
        if data['file'] in self.path:
            # Send event to main server that file has changed
            pass


if __name__ == "__main__":
    w = BaseWatcher('testwatcher', '/Users/matthewmoon/testfolder')