# TumblrDevKit

Tumblr command line deployment and Sass building development kit

## What it Does:

* deploys local HTML files to Tumblr's server via command line
* builds CSS from [SASS](http://sass-lang.com/), and inserts that CSS inside the theme's HTML
* reads variables from a SASS file, and formats into Tumblr [theme options](https://www.tumblr.com/docs/en/custom_themes#theme-options)

## Why Would I Use It?

* You manage several (3+) different blogs with custom themes and get really tired of having to copy paste code updates to each of them. Setting up an automation tool would actually save you time in the long run
* You really like SASS in general, and CSS variables in particular
* You think automation is cool

## Setup Instructions

(required for any of the features)

1. Install the global python requirements (with apt-get or the relevant thing for your platform)

        $ sudo apt-get install python3.4 python3.4-dev python-pip python-virtualenv

2. Download, setup the environment

        $ git clone http://github.com/LynnCo/TumblrDevKit.git
        $ cd TumblrDevKit
        $ virtualenv -p python3.4 venv && source venv/bin/activate && pip install -r requirements.txt

3. Create a theme file inside `static/themes/` (ex: `static/themes/bestcatpics.html`)
4. Start the flask server with `$ python server.py`

### Setup: Command Line Deploy

1. Copy the env file (`$ cp .env.example .env`) and fill it in with your login info. Make sure the newly created file contents aren't shown in source control.
2. Whenever you want to push changes to your theme to Tumblr, run `$ python deploy.py`

### Setup: CSS Builder

1. Add `<style type="text/css" source="local">{}</style>` into your theme
2. Create a SASS file for your theme with the same name as the HTML file inside of `static/sass` (ex: `static/sass/bestcatpics.sass`)
3. All the SASS files are compiled into `static/css/` whenever a change is detected in one of them
4. When `deploy.py` makes a request for your theme, the code place your CSS inside the `source="local"` style tag

### Setup: SASS Theme Options

1. Add `<meta name="{}" content="{}"/>` into your theme **once** (the code will duplicate it for as many variables as you have)
2. Have properly formatted variables inside the primary SASS file (eg: `static/sass/bestcatpics.sass`). Here's two examples of variable formmatting:
 
        $PRIMARY_COLOR: unquote("{color:Primary Color}")
        $PRIMARY_COLOR: rgb(0, 0, 0) !default

        $BODY_TEXT: unquote("{text:Body Text}")
        $BODY_TEXT: Arial !default

  * Use `$PRIMARY_COLOR` in your SASS and it will output `{color:Primary Color}` in your built CSS, this allows the CSS to be overwritten by Tumblr's theme options
  * The empty meta tags will be replaced with the (ex:) `<meta name="{color:Primary Color}" content="rgb(0, 0, 0)">`
3. The meta tags will be formatted when the server gets a request from `deploy.py`. 

## Relevant Links

* [Tumblr's Theme Docs](www.tumblr.com/docs/en/custom_themes)
* [SASS's docs](http://sass-lang.com/documentation/file.SASS_REFERENCE.html)

## Contact

@ [lynncyrin on twitter](twitter.com/lynncyrin) for all your "hey this script is horribly broken" needs
