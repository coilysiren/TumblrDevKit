# builtin
from glob import glob
from time import sleep
from os import environ as ENV

# external
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def deploy():
    load_dotenv('.env')

    driver = webdriver.Firefox()
    select = driver.find_element_by_css_selector

    # themes = glob('static/themes/*.*')
    # blog = themes[0].split('/')[-1].split('.')[0]
    driver.get('http://localhost:5000/static/themes/cyrinsong.html')
    if 'Problem loading page' in driver.title:
        driver.quit()
        print('!!ERROR!! Theme server not running')
        return

    select('*').send_keys(Keys.CONTROL, 'a')
    select('*').send_keys(Keys.CONTROL, 'c')

    driver.get('https://www.tumblr.com/customize')
    if 'Log in' in driver.title:
        sleep(0.1)
        select('#signup_email').send_keys(ENV['EMAIL'])
        select('#signup_password').send_keys(ENV['PASS'])
        select('#signup_forms_submit').click()
    sleep(4)
    select('#edit_html_button').click()
    sleep(0.1)
    select('html').send_keys(Keys.TAB, Keys.CONTROL, 'a')
    select('html').send_keys(Keys.TAB, Keys.DELETE)
    select('html').send_keys(Keys.TAB, Keys.CONTROL, 'v')
    select('#edit_html_panel .buttons_right .button.green').click() # update
    select('#edit_html_panel .buttons_right .button.blue').click() # save
    select('#edit_html_panel .buttons_left .icon_arrow_thin_left').click() # back

    driver.quit()

if __name__ == '__main__':
    deploy()
