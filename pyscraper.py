import requests
import sys
import json
from lxml import etree
from io import StringIO
from pyjath import PyJath

config = json.loads(sys.stdin.read())
print(config)

r = requests.get(config['urls'][0])
tree = etree.parse(StringIO(r.text), etree.HTMLParser())
result = PyJath().parse(config['template'], tree)

print(result)

