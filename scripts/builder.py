# builtin
import os
import re
import subprocess
from glob import glob
from html import escape
from difflib import unified_diff

# external
import sass
import colorama
from colorama import Fore


class Builder(object):

    style_tag = '<style type="text/css">{}</style>'
    metadata_tag = '<meta name="{}" content="{}"/>'


    def __init__(self, themes_dir, sass_dir):
        self.themes_dir = themes_dir
        self.sass_dir = sass_dir


    def create(self, *args, **kwargs):
        themes = glob(self.themes_dir+'*.*')

        for theme_path in themes:
            blog_name = theme_path.split('/')[-1].split('.')[0]
            sass_path = glob(self.sass_dir+blog_name+'.*')[0]
            built_theme_path = self.themes_dir+'built/'+blog_name+'.html'

            with open(self.themes_dir+blog_name+'.html', 'r') as f:
                html = f.read()

            html = Builder.format_style(html, sass_path)
            html = Builder.format_metadata(html, sass_path)

            with open(built_theme_path, 'w') as f:
                f.write(html)

            print('\nBuilt theme for blog {}:'.format(blog_name))
            print('\tview-source:file:///{}/{}'.format(os.getcwd(), built_theme_path))
            print('Url for customizing blog {}:'.format(blog_name))
            print('\thttp://{}.tumblr.com/customize\n'.format(blog_name))


    def format_style(html, sass_path):
        _html = html

        css = sass.compile(filename=sass_path, output_style='compressed')
        css += '{CustomCSS}'

        replacement = Builder.style_tag.format('\n'+css+'\n')
        html = Builder.replace_or_split(html, Builder.style_tag, replacement)

        Builder.make_diff(_html, html)
        return html


    def format_metadata(html, sass_path):
        _html = html

        with open(sass_path, 'r') as f:
            sass_content = f.read()

        # get the variables to input into the html
        # inside the sass file they should look like so:
        #
        # $VARIABLE: unquote("{color:Variable}")
        # $VARIABLE: rgb(X,X,X) !default
        sass_variables = re.findall(\
            r'(?im)'+\
            r'^(\$\w+):'+\
                r'\s*unquote'+\
                r'\(\"\{([\w\s:]+)\}\"\);*'+\
                r'(?:\s\#\s\S*?)*?'+\
            r'\s*?\1:'+\
                r'\s([\w\s,\"\\#\-\(\)]*?)'+\
                r'\s*?!default;*$'\
            ,sass_content)

        if not sass_variables:
            print(Fore.RED+'[WARNING] Variables in '+sass_path+' not represent or incorrectly formatted')
            return html

        # format the variables into metadata tags, add to HTML
        replacement = ''
        for variable in sass_variables:
            name = variable[1]
            default = variable[2].replace('"',"'")
            _replace = Builder.metadata_tag.format(name, default)
            replacement += '\n'+_replace
        html = Builder.replace_or_split(html, Builder.metadata_tag, replacement)

        Builder.make_diff(_html, html)
        return html


    def replace_or_split(html, tag, replacement):
        if tag in html:
            html = html.replace(tag, replacement)
        else:
            html_before, html_after = html.split('</head>')
            html = html_before + replacement + '\n</head>' + html_after
        return html


    def make_diff(original, edited):
        colorama.init(autoreset=True)
        diff = unified_diff(original.splitlines(), edited.splitlines(), n=1)
        for line in diff:
            if len(line) > 160:
                line = line[:160] + ' (...)'

            if line[0] == '-':
                print(Fore.RED+line)
            elif line[0] == '+':
                print(Fore.GREEN+line)
            elif line[0] == '@':
                print(Fore.BLUE+line)
            else:
                print(line)
