#!/usr/bin/env python

import cherrypy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


class Monitor(object):
    @cherrypy.expose
    def index(self):
        template = env.get_template("index.html")
        return template.render(lines=["hello templated world", ";-)"])

    def hello(self, param="world"):
        template = env.get_template("index.html")
        return template.render(line=["hello " + param])


cherrypy.quickstart(Monitor())
