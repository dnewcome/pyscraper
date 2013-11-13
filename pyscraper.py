import requests
import sys
import json
from lxml import etree
from io import StringIO
from pyjath import PyJath

config = json.loads(sys.stdin.read())

if 'url_list' in config:
    urls = config['url_list']
else:
    root_url = config['root_url']
    r = requests.get(root_url)
    tree = etree.parse(StringIO(r.text), etree.HTMLParser())
    urls = PyJath().parse(config['urls'], tree)

print(urls)

for url in urls:
    r = requests.get(url['url'])
    tree = etree.parse(StringIO(r.text), etree.HTMLParser())
    result = PyJath().parse(config['template'], tree)

    print(result)

