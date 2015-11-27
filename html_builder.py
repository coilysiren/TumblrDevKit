# builtin
import re
from glob import glob
from html import escape


style_tag = '<style type="text/css" source="local">{}</style>'
# expands to (ex:) <meta name="color:Background" content="#eee"/>
metadata_tag = '<meta name="{}" content="{}"/>'


def format_metadata(blog_name, html):

    if metadata_tag not in html:
        print('[WARNING] Could not find '+metadata_tag+' for theme '+blog_name)
        return html

    else:
        sass_file = glob('static/sass/'+blog_name+'.*')[0]
        with open(sass_file, 'r') as f:
            sass = f.read()

        # for example content:
        # $color_primary: unquote("{color:primary}")
        # $color_primary: rgb(244, 231, 144) !default
        variables = re.search('''
            ^(\$\w+):                       # $color_primary:
                \s*unquote\                 # unqoute
                (\"\{([\w\s:]+)\}\"\);*     # ("{color:primary")
                (?:\s\#.*?)*?\s*?           # any comments / whitespace

            \1:                             # $color_primary:
                \s([\w\s,\-\(\)]*?)         # rgb(244, 231, 144)
                !default;*$                 # !default
            ''', sass, flags=[re.I, re.M, re.X])

        print(variables)

        return html


def format_style(blog_name, html):
    style_file = glob('static/css/'+blog_name'.*')

    # check if a style file with the same name as the blog exists
    if style_file:
        style_file = style_file[0]
        # when there's a style file there's most likely custom colors to format
        html = format_metadata(blog_name, html)

    # if no style file then use the default one
    else:
        style_file = 'static/css/default.css'

    # add style to html
    with open(style_file, 'r') as f:
        css = f.read()
    css += '{CustomCSS}'
    style_replacement = style_tag.format(css)
    html = html.replace(style_tag, style_replacement)

    return html


def build_themes():
    themes = glob('static/themes/*.html')

    for theme_path in themes:
        blog_name = theme_path.split('/')[-1].split('.')[0]

        # static/themes/*.html is our starting point
        with open('static/themes/'+blog_name+'.html', 'r') as f:
            html = f.read()

        # if there's a style format tag, then this blog requires local CSS
        if style_tag in html:
            html = format_style(blog_name, html)
        # if no style format tag, then the blog CSS in already in the HTML
        else:
            print('[WARNING] Could not find '+style_tag+' for theme '+theme_path)

        # final content goes inside of static/themes/built for webdriver to pick up
        html = escape(html)
        with open('static/themes/built/'+blog_name+'.html', 'w') as f:
            f.write(html)

