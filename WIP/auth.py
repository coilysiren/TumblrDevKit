# internal
from os import environ as ENV

# external
import flask
import pytumblr
from dotenv import load_dotenv


#INITS

# environment
load_dotenv('.env')
TUMBLR_ENV = [
    ENV['CONSUMER_KEY'],
    ENV['CONSUMER_SECRET'],
    ENV['OAUTH_KEY'],
    ENV['OAUTH_SECRET'],
]


# flask application
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = ENV['SECRET_KEY']

# twython object
tumblr = pytumblr.TumblrRestClient(*TUMBLR_ENV)
tumblr.info()

# FUNCTIONS

def new_oauth():

    consumer_key = TUMBLR_ENV[0]
    consumer_secret = TUMBLR_ENV[1]
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url =     'http://www.tumblr.com/oauth/authorize'
    access_token_url =  'http://www.tumblr.com/oauth/access_token'

    # Get request token
    resp, content = client.request(request_token_url, "POST")
    request_token =  urlparse.parse_qs(content)

    # Redirect to authentication page
    # print '\nPlease go here and authorize:\n%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'][0])
    redirect_response = raw_input('Allow then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    url = urlparse.urlparse(redirect_response)
    query_dict = urlparse.parse_qs(url.query)
    oauth_verifier = query_dict['oauth_verifier'][0]

    # Request access token
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'][0])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = urlparse.parse_qs(content)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': access_token['oauth_token'][0],
        'oauth_token_secret': access_token['oauth_token_secret'][0]
    }

    return tokens


# ROUTES

@app.route('/')
def index():
    return 'mew'

@app.route('/login')
def login():
    auth = twitter.get_authentication_tokens(callback_url=flask.request.url_root[:-1]+'/callback')
    auth = new_oauth(tumblr)
    flask.session['oauth_token']        = auth['oauth_token']
    flask.session['oauth_token_secret'] = auth['oauth_token_secret']
    return flask.redirect(auth['auth_url'])

@app.route('/callback')
def callback():
    twitter = twython.Twython(
        ENV['API_KEY'],
        ENV['API_SECRET'],
        flask.session['oauth_token'],
        flask.session['oauth_token_secret'],
    )
    auth_creds = twitter.get_authorized_tokens(flask.request.args['oauth_verifier'])
    twitter = twython.Twython(
        ENV['API_KEY'],
        ENV['API_SECRET'],
        auth_creds['oauth_token'],
        auth_creds['oauth_token_secret'],
    )
    force_unfollow_fans(twitter)
    return 'done!'


if __name__ == '__main__':
    app.run(
        debug=False,
        port=int(ENV['PORT']),
        host='0.0.0.0',
    )
