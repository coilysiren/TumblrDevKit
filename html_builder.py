# builtin
import re
from glob import glob
from html import escape
from os import environ as ENV
from difflib import unified_diff

# external
import colorama
from dotenv import load_dotenv

load_dotenv('.env')
style_tag = '<style type="text/css" source="local">{}</style>'
metadata_tag = '<meta name="{}" content="{}"/>'


def make_diff(original, edited):
    if bool(ENV.get('DEBUG', False)):
        colorama.init(autoreset=True)
        diff = unified_diff(original.splitlines(), edited.splitlines(), n=1)
        for line in diff:
            if line[0] == '-':
                print(colorama.Fore.RED+line)
            elif line[0] == '+':
                print(colorama.Fore.GREEN+line)
            elif line[0] == '@':
                print(colorama.Fore.BLUE+line)
            else:
                print(line)

def format_metadata(blog_name, html):
    _html = html

    if metadata_tag not in html:
        print(Fore.RED+'[WARNING] Could not find '+metadata_tag+' for theme '+blog_name)
        return html

    else:
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
            print(Fore.RED+'[WARNING] Variables in '+sass_file+' not represent or incorrectly formatted')
            return html

        metadata_replacement = ''
        # format the variables into metadata tags
        for variable in sass_variables:
            name = variable[1]
            default = variable[2].replace('"',"'")
            _replace = metadata_tag.format(name, default)
            metadata_replacement += _replace+'\n'

        # add tags to the html
        html = html.replace(metadata_tag, metadata_replacement)
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

