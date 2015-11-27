# builtin
import os
import json
from os import environ as ENV

# ext
import flask
from dotenv import load_dotenv

# local
import deploy
import sass_builder
import html_builder


load_dotenv('.env')
app = flask.Flask(__name__)


@app.before_first_request
def setup_sass():
    sassbuilder = sass_builder.Builder('static/sass/', 'static/css/')
    sassbuilder.start()
    sassbuilder.compile_sass()

@app.before_request
def setup_html():
    html_builder.build_themes()


if __name__ == '__main__':
    app.run(debug=True, port=int(ENV.get('PORT', 5000)))
