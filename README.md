# TumblrDevKit

## What is this???

It takes a SASS file (or series of `@import`ed files) and sticks it inline in a Tumblr HTML theme. It's intended for manging several (3+) Tumblr blog themes, or just having a build process that pairs Tumblr themes with SASS.

Specifically, it:

* Builds a SASS file and puts it inside a `<style type="text/css"></style>` tag
* Allows for Tumblr theme variables in the SASS files, which parse into HTML metadata tags

## Startup

Get it

    $ git clone http://github.com/LynnCo/TumblrDevKit.git
    $ cd TumblrDevKit

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

Copy paste the built theme the `view-source:file:////...` address in your browser, or open that file in a text editor. It won't require any more edits before being pasted into Tumblr.

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
