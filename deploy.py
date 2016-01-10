# builtin
from glob import glob
from time import sleep
from os import environ as ENV

# external
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


load_dotenv('.env')


def deploy():
    port = ENV.get('PORT', 5000)
    themes = glob('static/themes/built/*.html')

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
        print('[ERROR] Login email or password not set')
        driver.quit()
        return


    for blog_path in themes:

        # get blog name from filename
        blog = blog_path.split('/')[-1].split('.')[0]

        # go to local version
        driver.get('http://localhost:{}/static/themes/built/{}.html'.format(port, blog))
        if 'Problem loading page' in driver.title:
            driver.quit()
            print('[ERROR] Theme server not running')
            return

        # copy it
        select('*').send_keys(Keys.CONTROL, 'a')
        select('*').send_keys(Keys.CONTROL, 'c')

        # go to customize, wait for it to load
        driver.get('https://www.tumblr.com/customize/{}'.format(blog))
        sleep(4)
        if 'Request denied' in driver.title:
            print('[ERROR] Blog name \"{}\" is invalid'.format(blog))
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
