# builtin
import re
import json
import string
# ext
import flask
# local

app = flask.Flask(__name__)
DEBUG = True
app.config.from_object(__name__)

def sub_var_tumblr_to_jinja(match):
    match = match.group(0)
    # python variables can't have - in the name
    match = re.sub(r'\-', '_', match)
    # tumblr variable -> jinja variable
    match = '{'+match+'}'
    return match

def tumblify(path):
    # format the html file
    with open('templates/'+path, 'r') as f:
        html = f.readlines()
    _html = ''
    for line in html:
        _html += line.strip()
    html = _html

    # template variable context
    context = {
        'output': '\n\n'
    }

    with open('response.txt', 'r') as f:
        response = (json.load(f.read()))
    context['posts'] = response['posts']
    context.update(response['response']['blog'])

    print(context)

    RE_VARIABLE = r'(?is)(?<!\{)\{[A-Z0-9 _-]*\}(?!\})'
    RE_BLOCK    = r'(?is)\{block\:[A-Z0-9 _-]*\}.*\{\/block\:[A-Z0-9 _-]*\}'
    RE_POSTS    = r'(?is)\{block\:posts\}.*\{\/block\:posts\}'

    post_types = ['text', 'photo', 'panorama', 'photoset', 'quote', 'link', 'chat', 'audio', 'video', 'answer']

    # parse all variables
    html = re.sub(RE_VARIABLE, sub_var_tumblr_to_jinja, html)

    # parse blocks
    # parse post variables
    # parse post types
    # parse post blocks

    # formatting
    context['output'] += '\n\n'
    from bs4 import BeautifulSoup
    html = BeautifulSoup(html).prettify()

    print(html)
    return html, context

@app.route('/')
def index ():
    html, context = tumblify('index.html')
    return flask.render_template_string(html, **context)

if __name__ == '__main__':
    app.run()
