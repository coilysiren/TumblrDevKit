import re

##############################################################

def parse_all_themes(*args, **kwargs):
    from glob import glob

    try: print(args[0])
    except: pass

    for theme_path in glob('themes/*.*'):
        with open(theme_path, 'r') as f:
            html = f.read()

        # we want to watcher not to crash in case of parse errors
        try: html = parse_theme(html)
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

##############################################################

def _sub_post_types(match):
    match = match.group(1).lower()
    match = 'post.type==\"'+match+'\"'
    return match

def _sub_post_variables_and_blocks(match):
    match = match.group(0).lower()
    match = 'post.'+match
    return match

def _sub_var_tumblr_to_jinja(match):
    match = match.group(0).lower()
    match = re.sub(r'\-', '_', match)
    match = '{ '+match+' }'
    return match

def _sub_blocks(match):
    block = match.group(1).lower()
    content = match.group(2).lower()
    match = '{% if '+block+' %}'+content+'{% endif %}'
    return match

def _sub_for_loop_posts(match):
    content = match.group(2)
    match = '{% for post in posts %}'+content+'{% endfor %}'
    return match

def _get_posts_content(html):
    return html

def _replace_posts_content(html, posts):
    return html

def parse_theme(html):
    POST_TYPES        = ['text','photo','panorama','photoset','quote','link','chat','audio','video','answer']
    RE_POSTS          = r'(?ism)(\{block:posts\})(.*?)(\{\/block:posts\})'
    RE_POST_TYPES     = r'(?ism)(?<=\{block:)('+'|'.join(POST_TYPES)+r')(?=\}.*?\{\/block:(\1)\})'
    RE_VARIABLES      = r'(?ism)(?<=\{)[\w\.\-]+(?=\})'
    RE_BLOCKS         = r'(?ism)\{block:([\w\.\-]+)\}(.*?)\{\/block:\1\}'
    RE_BLOCKS_START   = r'(?ism)(?<=\{block:)([\w\.\-]+)(?=\}.*?\{\/block:(\1)\})'
    RE_BLOCKS_END     = r'(?ism)(?<=\{block:post\.([\w\.\-]+)\}.*?\{\/block:)(\1)(?=\})'


    # swap the posts block to a for block
    html = re.sub(RE_POSTS, _sub_for_loop_posts, html)
    # swap every block to an if block
    while True:
        (html, subs) = re.subn(RE_BLOCKS, _sub_blocks, html)
        if not subs: break

    # # pull out posts block
    # posts_search = re.search(RE_POSTS, html)
    # posts = html[posts_search.start():posts_search.end()]

    # # reformat (VAR) to (posts.VAR)
    # posts = re.sub(RE_VARIABLES, _sub_post_variables_and_blocks, posts)
    # # reformat (block:VAR) to (block:post.VAR)
    # posts = re.sub(RE_BLOCKS_START, _sub_post_variables_and_blocks, posts)
    # posts = re.sub(RE_BLOCKS_END, _sub_post_variables_and_blocks, posts)
    # # reformat (block:post.TYPE) to (block:posts.type == TYPE)
    # posts = re.sub(RE_POST_TYPES, _sub_post_types, posts)

    # # return posts to rest of HTML
    # html = html[:posts_search.start()] + posts + html[posts_search.end():]
    # change tumblr variables to jinja variables
    html = re.sub(RE_VARIABLES, _sub_var_tumblr_to_jinja, html)


    return html

if __name__ == '__main__':
    watcher(parse_all_themes, 'themes/')
    parse_all_themes()
