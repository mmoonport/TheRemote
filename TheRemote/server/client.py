from twisted.internet import protocol

__author__ = 'mmoon'

class UDPSender(protocol.DatagramProtocol):
    def __init__(self, onStart):
        self.onStart = onStart

    def startProtocol(self):
        self.onStart.callback(self)

    def send_message(self, data, (host, port)):
        self.transport.write(data, (host,port))


class FileWatchClient(object):
    def __init__(self, host, port):
        self.host = host