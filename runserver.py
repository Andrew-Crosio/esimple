#!/usr/bin/env python
# coding=utf-8
"""Run the server"""
from gevent import monkey, pywsgi, local, wsgi as wsgi_fast
import bottle

# Load the application views into local space
from views import *


monkey.patch_all()


class GeventServer(bottle.ServerAdapter):
    """Gevent server for bottle"""
    def run(self, handler):
        """Run the server"""
        if bottle.threading.local is local.local:
            monkey.patch_all()

        wsgi = wsgi_fast if self.options.get('fast') else pywsgi
        server = wsgi.WSGIServer((self.host, self.port), handler)
        server.serve_forever()


application = bottle.default_app()


if __name__ == '__main__':
    run_options = {
        'host': '127.0.0.1',
        'server': GeventServer,
        'quiet': True,
        'app': application
    }

    bottle.run(**run_options)
