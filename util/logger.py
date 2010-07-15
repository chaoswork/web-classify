#coding=utf8
# Useage:
# from util.import Logger
#     log = Logger( logfilepath ="",loglevel='NOTSET',name='' ).logger
#     log.debug(...) 

import logging
import os,sys
# from the comments in http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531
class Singleton(object):
    def __new__(type, *args, **kwargs):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

# logging is weird, we don't want to setup multiple handlers
# so make sure we do that mess only once

class Logger(Singleton):
    _no_handlers = True

    def __init__(self, logfilepath ="",loglevel='NOTSET',name=''):
        self.loglevel = logging._levelNames[loglevel]
        self.logger = logging.getLogger( name )
        
        if self._no_handlers:
            self._setup_handlers( logfilepath=logfilepath )

    def _setup_handlers(self, logfilepath ):
        # we try to log module loading and whatnot, even if we aren't
        # root, so if we can't write to the log file, ignore it
        # this lets "--help" work as a user
        # https://fedorahosted.org/func/ticket/75
        if not logfilepath:
            handler = logging.StreamHandler(sys.stdout)
        elif not os.access(logfilepath, os.W_OK):
            return
        else:
            handler = logging.FileHandler(logfilepath, "a")

        self.logger.setLevel(self.loglevel)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self._no_handlers = False
