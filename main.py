# builtin
# ext
import flask
# local

app = flask.Flask(__name__)
DEBUG = True
app.config.from_object(__name__)

def clean_html (self, html):
    # cleans html to prevent people doing evil things with it like
    # like... idk. things with evil scripts and inline css
    from bs4 import BeautifulSoup
    html = BeautifulSoup(html)
    # destroy evil tags
    for tag in html(['iframe', 'script']): tag.decompose()
    # remove evil attributes
    for tag in html():
        for attribute in ["class", "id", "name", "style", "data"]:
            del tag[attribute]
    return str(html)

def snippet(text, path):
    for seperator in ('<readmore/>', '<br>', '<br/>', '</p>'):
        if seperator in text:
            break
    snip = text.split(seperator, 1)[0]
    url = '/posts/'+path.split('/')[-1].split('.')[0]
    snip += '<div class="readmore"><a href="{}" title="the post\'s not done! Here\'s the rest">Continued...</a></div>'.format(url)
    return snip


@app.route('/')
def index ():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()
