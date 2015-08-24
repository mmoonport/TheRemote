#!/usr/bin/env python
import logging
import sys
import traceback
import subprocess

from os.path import dirname
import os


# Root path
base_path = dirname(os.path.abspath(__file__))

# Insert local directories in path
sys.path.insert(0, os.path.join(base_path, 'lib'))

from theremote.environment import Env
from theremote.core.helpers.variable import remove_pyc, get_data_dir

# Remove pyc for fresh dynamic imports
remove_pyc(base_path)


class TheRemote(object):
    def __init__(self):
        self.daemon = None
        # Get startup args
        from theremote.environment import get_options

        self.options = get_options(sys.argv[1:])

        # Load Settings

        # Build or set data dir
        if self.options.data_dir:
            self.data_dir = self.options.data_dir
        else:
            self.data_dir = os.path.expanduser(Env.setting('data_dir'))

        if self.data_dir == '':
            self.data_dir = get_data_dir()

        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

        # Create logging dir
        self.log_dir = os.path.join(self.data_dir, 'logs');
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)

        # Setup logging
        from theremote.core.logger import TRLog
        log_file = os.path.join(self.log_dir, 'theremote.log')
        logger = TRLog(__name__)
        self.log = logger.log
        if Env.setting('debug'):
            logger.setup_log(log_file, level=logging.DEBUG)
        else:
            logger.setup_log(log_file)

    def run(self):
        from twisted.internet import reactor

    def restart(self):
        try:
            if self.run_as_daemon():
                try: self.daemon.stop()
                except: self.log.critical(traceback.format_exc())
            logging.shutdown()
            args = [sys.executable] + [os.path.join(base_path, os.path.basename(__file__))] + sys.argv[1:]
            subprocess.Popen(args)
        except:
            self.log.critical(traceback.format_exc())

    def daemonize(self):
        if self.run_as_daemon():
            try:
                from theremote.core.utils.daemon import Daemon
                self.daemon = Daemon(self.options.pid_file)
                self.daemon.daemonize()
            except SystemExit:
                raise
            except:
                self.log.critical(traceback.format_exc())

    def run_as_daemon(self):
        return self.options.daemon and self.options.pid_file


if __name__ == "__main__":
    l = TheRemote()
    l.daemonize()
    l.run()