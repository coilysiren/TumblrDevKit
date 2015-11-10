# builtin
import os
import json

# ext
import flask

# local
import parser


def parse_all_themes(*args, **kwargs):
    from glob import glob

    try: print(args[0])
    except: pass

    for theme_path in glob('themes/*.*'):
        with open(theme_path, 'r') as f:
            html = f.read()

        # we want to watcher not to crash in case of parse errors
        try: html = parser.parse_theme(html)
        except (IndexError) as e:
            print(e)

        template_path = 'templates/'+theme_path[7:]
        with open(template_path, 'w') as f:
            f.write(html)
        print('wrote to {}'.format(template_path))

def watcher(callback, path):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    handler = FileSystemEventHandler()
    handler.on_modified = callback
    watch = Observer()
    # watch.schedule(handler, os.path.dirname(__file__)+path)
    watch.schedule(handler, '.')
    watch.start()

def html_escape(func):
    def wrapped(*args, **kwargs):
        from html import escape
        return escape(func(*args, **kwargs))
    return wrapped


app = flask.Flask(__name__)


@app.context_processor
def add_data_to_context():
    with open('data.json', 'r') as f:
        data = json.load(f)

    data.update(data['response']['blog'])
    data['posts'] = data['response']['posts']
    data['metadescription'] = data['description']

    return data

@app.route('/static/themes/<path>')
@html_escape
def theme_server(path):
    with open('static/themes/'+path, 'r') as f:
        string = f.read()
    return string

@app.route('/')
def index ():
    return flask.render_template('index.html')


if __name__ == '__main__':
    watcher(parse_all_themes, 'themes/')
    parse_all_themes()
    app.run(debug=True)
