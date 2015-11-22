# builtin
from glob import glob
from time import sleep
from html import escape
from os import environ as ENV

# external
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def build_themes():
    themes = glob('static/themes/*.html')
    style_tag = '<style type="text/css" source="local">{}</style>'

    for theme_path in themes:
        blog_name = theme_path.split('/')[-1].split('.')[0]

        with open('static/themes/'+blog_name+'.css', 'r') as f:
            css = f.read()
        css += '{CustomCSS'}
        style_replace = style_tag.format(css)

        with open('static/themes/'+blog_name+'.html', 'r') as f:
            html = f.read()
        html.replace(style_tag, style_replace)
        html = escape(html)

        with open('static/themes/built/'+blog_name+'.html', 'w') as f:
            f.write(html)


def publish():

    load_dotenv('.env')

    port = ENV.get('PORT', 5000)
    themes = glob('static/themes/*.*')

    driver = webdriver.Firefox()
    select = driver.find_element_by_css_selector

    # log in to tumblr
    driver.get('https://www.tumblr.com/login')
    sleep(0.1)
    try:
        select('#signup_email').send_keys(ENV['EMAIL'])
        select('#signup_password').send_keys(ENV['PASS'])
        select('#signup_forms_submit').click()
    except KeyError:
        print('!!ERROR!! Login email or password not set')
        driver.quit()
        return


    for blog_path in themes:

        # get blog name from filename
        blog = blog_path.split('/')[-1].split('.')[0]

        # go to local version
        driver.get('http://localhost:{}/static/themes/{}.html'.format(port, blog))
        if 'Problem loading page' in driver.title:
            driver.quit()
            print('!!ERROR!! Theme server not running')
            return
        # copy it
        select('*').send_keys(Keys.CONTROL, 'a')
        select('*').send_keys(Keys.CONTROL, 'c')

        # go to customize, wait for it to load
        driver.get('https://www.tumblr.com/customize/{}'.format(blog))
        sleep(4)
        if 'Request denied' in driver.title:
            print('!!ERROR!! Blog name \"{}\" is invalid'.format(blog))
            continue
        # go to the html section, paste content
        select('#edit_html_button').click()
        sleep(0.1)
        select('html').send_keys(Keys.TAB, Keys.CONTROL, 'a')
        select('html').send_keys(Keys.TAB, Keys.DELETE)
        select('html').send_keys(Keys.TAB, Keys.CONTROL, 'v')
        # save
        select('#edit_html_panel .buttons_right .button.green').click() # update
        select('#edit_html_panel .buttons_right .button.blue').click() # save
        select('#edit_html_panel .buttons_left .icon_arrow_thin_left').click() # back
        print('Saved blog {}'.format(blog))

    driver.quit()

if __name__ == '__main__':
    deploy()
