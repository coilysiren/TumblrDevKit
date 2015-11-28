# builtin
import re
from glob import glob
from html import escape
from pprint import pprint
from os import environ as ENV
from difflib import context_diff

# external
from dotenv import load_dotenv


load_dotenv('.env')
style_tag = '<style type="text/css" source="local">{}</style>'
metadata_tag = '<meta name="{}" content="{}"/>'


def make_diff(original, edited):
    if bool(ENV.get('DEBUG', False)):
        diff = context_diff(original.splitlines(), edited.splitlines())
        print('\nhtml diff: \n\n')
        pprint(list(diff))
        print('\n')

def format_metadata(blog_name, html):
    _html = html

    if metadata_tag not in html:
        print('[WARNING] Could not find '+metadata_tag+' for theme '+blog_name)
        return html

    else:
        metadata_replacement = ''

        # get sass file
        sass_file = glob('static/sass/'+blog_name+'.*')[0]
        with open(sass_file, 'r') as f:
            sass = f.read()

        # get the variables to input into the html
        # inside the sass file they should look like so:
        #
        # $color_VAR: unquote("{color:VAR}")
        # $color_VAR: rgb(XXX, XXX, XXX) !default
        sass_variables = re.findall(\
            r'(?im)'+\
            r'^(\$\w+):'+\
                r'\s*unquote'+\
                r'\(\"\{([\w\s:]+)\}\"\);*'+\
                r'(?:\s\#\s\S*?)*?'+\
            r'\s*?\1:'+\
                r'\s([\w\s,\"\\#\-\(\)]*?)'+\
                r'\s*?!default;*$'\
            ,sass)

        if not sass_variables:
            print('[WARNING] Variables in '+sass_file+' not represent or incorrectly formatted')
            return html

        # format the variables into metadata tags
        for variable in sass_variables:
            _replace = metadata_tag.format(variable.group(2), variable.group(3))
            metadata_replacement += _replace+'\n'

        # add tags to the html
        html.replace(metadata_tag, metadata_replacement)
        print('[INFO] formatted metadata for '+blog_name+' .html')
        make_diff(_html, html)
        return html


def format_style(blog_name, html):
    _html = html
    style_file = glob('static/css/'+blog_name+'.*')

    # check if a style file with the same name as the blog exists
    if style_file:
        style_file = style_file[0]
        # when there's a style file there's most likely custom colors to format
        html = format_metadata(blog_name, html)

    # if it doesn't then use the default one
    else:
        style_file = 'static/css/default.css'

    # add style to html
    with open(style_file, 'r') as f:
        css = f.read()
    css += '{CustomCSS}'
    style_replacement = style_tag.format(css)

    html = html.replace(style_tag, style_replacement)
    print('[INFO] formatted styles for '+blog_name+' .html')
    make_diff(_html, html)
    return html


def build_themes():
    themes = glob('static/themes/*.html')

    for theme_path in themes:
        blog_name = theme_path.split('/')[-1].split('.')[0]

        # static/themes/*.html is our starting point
        with open('static/themes/'+blog_name+'.html', 'r') as f:
            html = f.read()

        # if there's a style_tag, then this blog requires locally built CSS
        if style_tag in html:
            html = format_style(blog_name, html)

        # final content goes inside of static/themes/built for webdriver to pick up
        html = escape(html)
        with open('static/themes/built/'+blog_name+'.html', 'w') as f:
            f.write(html)

