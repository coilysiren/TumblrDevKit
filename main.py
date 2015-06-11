# builtin
import os
import re
import contextlib
from collections import deque
# ext
import six
import flask
import jinja2
from jinja2 import Markup
from jinja2.ext import Extension
from jinja2.runtime import Undefined
# local
import nodes
from parser import Parser
from compiler import Compiler

app = flask.Flask(__name__)
DEBUG = True
app.config.from_object(__name__)

class TumblrParser(Extension):

    options={}

    def __init__(self, environment):

        super(TumblrParser, self).__init__(environment)

        environment.extend(tumblr=self)

        self.variable_start_string = environment.variable_start_string
        self.variable_end_string = environment.variable_end_string
        self.options["variable_start_string"] = environment.variable_start_string
        self.options["variable_end_string"] = environment.variable_end_string

    def preprocess(self, source, name, filename=None):
        if not name:
            return source
        else:
            parser = Parser(source ,filename=filename)
            block = parser.parse()
            compiler = Compiler(block, **self.options)
            return compiler.compile().strip()

@app.route('/')
def index ():
    # app.jinja_env.add_extension('pyjade.ext.jinja.')
    app.jinja_env.add_extension('main.TumblrParser')
    return flask.render_template('mew.html', mew='great')

if __name__ == '__main__':
    app.run()
