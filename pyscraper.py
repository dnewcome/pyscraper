import requests
import sys
import json
from lxml import etree
from io import StringIO
from pyjath import PyJath

trace_enabled = True 
def trace(msg, arg): 
    if trace_enabled:
        print msg, arg

config = json.loads(sys.stdin.read())
trace("main config: ", config)

def scrape(config, html):
    if type(config['urls'][0]) is dict:
        urls = config['urls']
    else:
        if not html:
            raise Exception("no page loaded to search for urls")
        else:
            urls = PyJath().parse(config['urls'], html)

    trace("urls: ", urls)
    trace("template: ", config['template'])

    for url in urls:
        trace(url, None)
        r = requests.get(url['url'])
        tree = etree.parse(StringIO(r.text), etree.HTMLParser())
        result = PyJath().parse(config['template'], tree)
        trace("result: ", result)

        if "config" in config:
            return scrape(config['config'], tree)

scrape(config, None)
