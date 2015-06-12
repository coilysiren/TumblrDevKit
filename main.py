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
    match = match.group(0).lower()
    match = re.sub(r'\-', '_', match)
    match = '{'+match+'}'
    return match

def sub_block_start(match):
    match = match.group(0).lower()
    var = match[7:-1]
    match = '{% if '+var+' %}'
    return match

def sub_post_variables_and_blocks(match):
    match = match.group(0).lower()
    match = 'post.'+match
    return match

def sub_post_types(match):
    match = match.group(0).lower()
    match = 'type==\"'+match+'\"'
    return match

def tumblify(path):
    RE_VARIABLE      = r'(?is)\{[A-Z0-9 _\.\-="]*?\}'
    RE_BLOCK_START   = r'(?is)\{block\:[A-Z0-9 _\.\-="]*?\}'
    RE_BLOCK_END     = r'(?is)\{\/block\:[A-Z0-9 _\.\-="]*?\}'
    RE_POSTS         = r'(?is)(?<=\{block\:posts\}).*(?=\{\/block\:posts\})'
    RE_POSTS_START   = r'(?is)\{block\:posts\}'
    RE_POSTS_END     = r'(?is)\{\/block\:posts\}'
    RE_POST_VARIABLE = r'(?is)(?<=\{)[A-Z0-9 _\.\-="]*?(?=\})'
    RE_POST_BLOCK    = r'(?is)(?<=\{block\:)[A-Z0-9 _\.\-="]*?(?=\})'
    RE_POST_TYPES    = r'(?is)(?<=\{block\:post\.)(text|photo|panorama|photoset|quote|link|chat|audio|video|answer)(?=\})'


    # format the html file
    with open('templates/'+path, 'r') as f:
        html = f.readlines()
    _html = ''
    for line in html:
        _html += line.strip()
    html = _html


    # template variable context
    context = {'output': '\n\n'}
    # example context
    with open('response.txt', 'r') as f:
        response = json.load(f)
    context.update(response['response']['blog'])
    context['posts'] = response['response']['posts']
    context['metadescription'] = context['description']

    posts_index = re.search(RE_POSTS, html)
    posts = html[posts_index.start():posts_index.end()]
    posts = re.sub(RE_POST_VARIABLE, sub_post_variables_and_blocks, posts)
    posts = re.sub(RE_POST_BLOCK, sub_post_variables_and_blocks, posts)
    posts = re.sub(RE_POST_TYPES, sub_post_types, posts)
    html = html[:posts_index.start()] + posts + html[posts_index.end():]


    html = re.sub(RE_VARIABLE, sub_var_tumblr_to_jinja, html)
    html = re.sub(RE_POSTS_START, '{% for post in posts %}', html)
    html = re.sub(RE_POSTS_END, '{% endfor %}', html)
    html = re.sub(RE_BLOCK_START, sub_block_start, html)
    html = re.sub(RE_BLOCK_END, '{% endif %}', html)


    context['output'] += '\n\n'
    from bs4 import BeautifulSoup
    html = BeautifulSoup(html).prettify()


    return html, context

@app.route('/')
def index ():
    html, context = tumblify('index.html')
    return flask.render_template_string(html, **context)

if __name__ == '__main__':
    app.run()
