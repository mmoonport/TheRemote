import pywatchman
from twisted.internet import protocol, task
from theremote.core.utils.daemon import Daemon

TR_HOST = '127.0.0.1'
TR_PORT = '3339'

class TwistedWatcher(protocol.DatagramProtocol):
    def startProtocol(self):
        self.daemon = Daemon('/tmp/{}.pid'.format(self.name))
        self.daemon.daemonize()
        self.transport.connect(TR_HOST, TR_PORT)
        self._loop = task.LoopingCall(self.receive)
        self._loop.start(1)

    def receive(self):
        pass

    def datagramReceived(self, datagram, addr):
        if datagram['event'] == 'shut-down':
            self.doStop()
        print "received {} from {}:{}".format(datagram, addr[0], addr[1])

    def stopProtocol(self):
        self.daemon.stop()

class BaseWatcher(TwistedWatcher):
    def __init__(self, name, path, options=None):
        super(BaseWatcher, self).__init__()

        self.name = name
        self.path = path
        self.options = options or {}
        self.client = pywatchman.client()
        self.subscription = self.client.query('subscribe', path, name, options)


    def receive(self):
        try:
            self.handler(self.client.receive())
        except NotImplementedError, pywatchman.WatchmanError:
            raise
        except:
            pass


    def handler(self, data):
        raise NotImplementedError('You must define a handler')


class FileWatcher(BaseWatcher):
    def handler(self, data):
        if data['file'] in self.path:
            self.transport.write(data)


if __name__ == "__main__":
    w = BaseWatcher('testwatcher', '/Users/matthewmoon/testfolder')