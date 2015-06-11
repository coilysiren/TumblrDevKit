import re
import requests
from bs4 import BeautifulSoup

RE_VARIABLE = r'(?is)(?<!\{)\{[A-Z0-9 _-]*\}(?!\})'
RE_BLOCK = r'(?is)\{block\:[A-Z0-9 _-]*\}.*\{\/block\:[A-Z0-9 _-]*\}'

# html = requests.get('http://tumblr.com/docs/en/custom_themes')
# with open ('tumblr.txt', 'w') as f:
#     f.write(html.text)

with open ('tumblr.txt', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html)
for tag in soup.find_all('th', text=re.compile(RE_BLOCK)):
    print(tag.contents[0])

for tag in soup.find_all('th', text=re.compile(RE_VARIABLE)):
    print(tag.contents[0])
