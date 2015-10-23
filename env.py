import os
import dotenv

dotenv.load_dotenv('.env')

ENV = {
    'CONSUMER_KEY':     os.environ.get('CONSUMER_KEY', ''),
    'CONSUMER_SECRET':  os.environ.get('CONSUMER_SECRET', ''),
    'OAUTH_KEY':        os.environ.get('OAUTH_KEY', ''), # user context
    'OAUTH_SECRET':     os.environ.get('OAUTH_SECRET', ''), # user context
    'PORT':             os.environ.get('PORT', ''),
    'SECRET_KEY':       os.environ.get('SECRET_KEY', ''),
}

TUMBLR_ENV = [
    ENV['CONSUMER_KEY'],
    ENV['CONSUMER_SECRET'],
    ENV['OAUTH_KEY'],
    ENV['OAUTH_SECRET'],
]
