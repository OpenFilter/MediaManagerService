#!/usr/bin/python

import os, sys
import logging as log

class WebService(object):
    @staticmethod
    def loadHandlers(rootDirectory):
        sys.path.insert(0, rootDirectory)
        handlersDirectory = os.path.sep.join([rootDirectory, 'handlers'])
        if not os.path.isdir(handlersDirectory):
            log.critical("WebService handlers directory does not exist: %s" % (
                handlersDirectory,
            ))
            sys.exit(1)
        handler_urls = []
        handler_failure = False
        handler_error = None
        serviceFilenameList = os.listdir(handlersDirectory)
        serviceFilenameList.sort()
        for serviceFilename in serviceFilenameList:
            if serviceFilename[-3:] != '.py':
                    continue
            service = serviceFilename[:-3]
            if service == '__init__':
                    continue
            handler_module_path = '.'.join([
                    'handlers', service,
            ])
            try:
                handler_module = __import__(
                    handler_module_path, {}, {}, [service],
                )
            except ImportError, e:
                handler_failure = True
                log.critical('Unable to import "%s": %s' % (
                    service, str(e),
                ))
                if handler_error is None:
                    handler_error = 'ImportError'
                continue
            except SyntaxError, e:
                handler_failure = True
                log.critical('Syntax error in "%s": %s' % (
                    service, str(e),
                ))
                if handler_error is None:
                    handler_error = 'SyntaxError'
                continue
            try:
                handler = getattr(handler_module, service)
            except AttributeError, e:
                handler_failure = True
                log.critical('Invalid class in "%s": %s' % (
                    service, str(e),
                ))
                if handler_error is None:
                    handler_error = 'AttributeError'
                continue
            log.info('%s: %s' % (
                handler_module_path, handler.url(),
            ))
            handler_url = handler.url()
            log.info('Loading Handler: %s' % handler_url)
            handler_urls.append((handler_url, handler))
            if handler_url[:-1] != '/':
                log.info('Loading Handler: %s' % handler_url + '/')
                handler_urls.append((handler_url + '/', handler))
            handler_urls.append((handler_url + '.json', handler))
        if handler_failure:
            log.critical('loading handlers failed: %s' % (
                handler_error,
            ))
            sys.exit(1)
        del sys.path[0]
        return handler_urls

