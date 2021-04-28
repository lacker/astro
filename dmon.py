#!/usr/bin/env python

import cherrypy


class Monitor(object):
    @cherrypy.expose
    def index(self):
        return "this is the monitor"


cherrypy.quickstart(Monitor())
