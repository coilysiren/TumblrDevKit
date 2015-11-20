# builtin
import os
import json
from os import environ as ENV

# ext
import flask
from dotenv import load_dotenv

# local
import deploy


load_dotenv('.env')
app = flask.Flask(__name__)
@app.before_first_request(deploy.build_themes)
# find themes at static/themes/build/blogname.html


if __name__ == '__main__':
    app.run(debug=True, port=int(ENV.get('PORT', 5000)))
