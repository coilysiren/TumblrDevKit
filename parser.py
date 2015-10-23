import re

def _sub_var_tumblr_to_jinja(match):
    match = match.group(0).lower()
    match = re.sub(r'\-', '_', match)
    match = '{'+match+'}'
    return match

def _sub_block_start(match):
    match = match.group(0).lower()
    var = match[7:-1]
    match = '{% if '+var+' %}'
    return match

def _sub_block_end(match):
    return '{% endif %}'

def _sub_post_variables_and_blocks(match):
    match = match.group(0).lower()
    match = 'post.'+match
    return match

def _sub_post_types(match):
    match = match.group(0).lower()
    match = 'type==\"'+match+'\"'
    return match

def parse_theme(path):
    RE_VARIABLE      = r'(?is)\{[A-Z0-9 _\.\-="]*?\}'
    RE_BLOCK_START   = r'(?is)\{block\:[A-Z0-9 _\.\-="]*?\}'
    RE_BLOCK_END     = r'(?is)\{\/block\:[A-Z0-9 _\.\-="]*?\}'
    RE_POSTS         = r'(?is)(?<=\{block\:posts\}).*(?=\{\/block\:posts\})'
    RE_POSTS_START   = r'(?is)\{block\:posts\}'
    RE_POSTS_END     = r'(?is)\{\/block\:posts\}'
    RE_POST_VARIABLE = r'(?is)(?<=\{)[A-Z0-9 _\.\-="]*?(?=\})'
    RE_POST_BLOCK    = r'(?is)(?<=\{block\:)[A-Z0-9 _\.\-="]*?(?=\})'
    RE_POST_TYPES    = r'(?is)(?<=\{block\:post\.)(text|photo|panorama|photoset|quote|link|chat|audio|video|answer)(?=\})'

    posts_index = re.search(RE_POSTS, html)
    posts = html[posts_index.start():posts_index.end()]
    posts = re.sub(RE_POST_VARIABLE, _sub_post_variables_and_blocks, posts)
    posts = re.sub(RE_POST_BLOCK, _sub_post_variables_and_blocks, posts)
    posts = re.sub(RE_POST_TYPES, _sub_post_types, posts)
    html = html[:posts_index.start()] + posts + html[posts_index.end():]


    html = re.sub(RE_VARIABLE, _sub_var_tumblr_to_jinja, html)
    html = re.sub(RE_POSTS_START, '{% for post in posts %}', html)
    html = re.sub(RE_POSTS_END, '{% endfor %}', html)
    html = re.sub(RE_BLOCK_START, _sub_block_start, html)
    html = re.sub(RE_BLOCK_END, _sub_block_end, html)

    return html
