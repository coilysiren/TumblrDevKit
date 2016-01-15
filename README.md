# TumblrDevKit

## About

It takes a SASS file (or series of `@import`ed files) and sticks it inline in a Tumblr HTML theme. It's intended for manging several (3+) Tumblr blog themes, or just having a build process that pairs Tumblr themes with SASS.

Specifically, it:

* Builds a SASS file and puts it inside a `<style type="text/css"></style>` tag
* Allows for Tumblr theme variables in the SASS files, which parse into `<meta name="color:Heading text" content=""/>` style meta tags and `#title{color: {color:Heading text} }` style template strings

## Startup

Do some setup (requires `git`, `python`, `pip`)

    $ git clone http://github.com/LynnCo/TumblrDevKit.git
    $ cd TumblrDevKit
    $ pip install -r requirements.txt

Create some HTML ([example](https://github.com/LynnCo/TumblrDevKit/blob/active/static/themes/cyrinsong.html))

    $ subl static/themes/BLOGNAME.sass

Create some SASS ([example](https://github.com/LynnCo/TumblrDevKit/blob/active/static/sass/cyrinsong.sass))

    $ subl static/sass/BLOGNAME.sass

Run the script

    $ python scripts/main.py

        Creating theme for blog BLOGNAME

        (...)

        Built theme:
            view-source:file:////~/tumblrdevkit/static/themes/built/BLOGNAME.html
        Customize URL:
            http://BLOGNAME.tumblr.com/customize

Copy paste the built theme `view-source:file:////...` address in your browser, or open that file in a text editor. It won't require any more edits before being pasted into Tumblr. Also the filepath doesn't change between builds, so just reload the page to get new versions.

## Tumblr Variables in your SASS

You can format your SASS variables to be Tumblr theme customization variables (editable in the theme customization interface). The format for that is

    $VARIABLE: unquote("{TYPE:VARIABLE}")
    $VARIABLE: VALUE !default

In BLOGNAME.sass it will look like this

    $color_primary: unquote("{color:primary}")
    $color_primary: rgb(244, 231, 144) !default

    $font_title: unquote("{font:title}")
    $font_title: Montserrat, "Helvetica Neue", Helvetica, Arial, sans-serif !default

Note that the variables **have** to be inside of BLOGNAME.sass, not imported from another file. The active branch [has in use examples](https://github.com/LynnCo/TumblrDevKit/blob/active/static/sass/cyrinsong.sass#L1-L18).

The format is fairly fragile, so the script will tell you when you get it right / wrong

## Extra Stuff

* The SASS builder adds `{CustomCSS}` to the end of your style block
* The intent of this tool is entirely SASS integration, so it doesn't change your HTML theme - except to add the CSS / meta tags of course.
* This tool used to [parse Tumblr themes into Jinja2 themes](https://github.com/LynnCo/TumblrDevKit/blob/c1a7e88f8ae9500037b2cdef9df97980c0b63096/parser.py), then rendered them with a local Flask server. This allowed working on themes while entirely offline, but in the end that feature was more work than it was worth.
* Similarly, it used to [deploy to Tumblr from command line](https://github.com/LynnCo/TumblrDevKit/blob/d825101b8b5a443a54d4524b03cb52e317c2f208/deploy.py), but Selenium turned out to be a very poor tool for that purpose.
* I really want to hear about it if you used this!!!
