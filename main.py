# builtin
import os
import json
from os import environ as ENV

# ext
import flask
from dotenv import load_dotenv


def html_escape(func):
    def wrapped(*args, **kwargs):
        from html import escape
        return escape(func(*args, **kwargs))
    return wrapped


load_dotenv('.env')
app = flask.Flask(__name__)


# @app.context_processor
# def add_data_to_context():
#     with open('data.json', 'r') as f:
#         data = json.load(f)

#     data.update(data['response']['blog'])
#     data['posts'] = data['response']['posts']
#     data['metadescription'] = data['description']

#     return data

@app.route('/static/themes/<path>')
@html_escape
def theme_server(path):
    with open('static/themes/'+path, 'r') as f:
        string = f.read()
    return string

# @app.route('/')
# def index ():
#     return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=int(ENV.get('PORT', 5000)))
