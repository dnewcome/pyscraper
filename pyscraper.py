import requests
import time
import sys
import json
from lxml import etree
from io import StringIO
from pyjath import PyJath

trace_enabled = True 
delay = 5

def trace(msg, arg): 
    if trace_enabled:
        print msg, arg

config = json.loads(sys.stdin.read())
base = config['base'] if 'base' in config else ''

trace("main config: ", config)

def scrape(config, html):
    try:
        if type(config['urls'][0]) is dict:
            urls = config['urls']
        else:
            if not html:
                raise Exception("no page loaded to search for urls")
            else:
                urls = PyJath().parse(config['urls'], html)

        trace("urls: ", urls)
        trace("template: ", config['template'])

        ret = []

        for url in urls:
            try:
                trace("requesting", base + url['url'])
                r = requests.get(base + url['url'])
                print r
                tree = etree.parse(StringIO(r.text), etree.HTMLParser())
                result = PyJath().parse(config['template'], tree)
                trace("result: ", result)
                ret.append(result)

                if "config" in config:
                    ret.append(scrape(config['config'], tree))
            except KeyboardInterrupt:
                sys.exit()
            except Exception, e:
                print e

        return ret

    except:
        pass

print scrape(config, None)
