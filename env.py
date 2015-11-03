import os
import dotenv

dotenv.parse_dotenv('.env')

ENV = {}
for item in dotenv.parse_dotenv('.env'):
    ENV[item[0]] = item[1]

TUMBLR_ENV = [
    ENV['CONSUMER_KEY'],
    ENV['CONSUMER_SECRET'],
    ENV['OAUTH_KEY'],
    ENV['OAUTH_SECRET'],
]
