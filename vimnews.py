import webapp2

import lxml
import lxml.html as HTML
import lxml.etree as etree
import urllib, urllib2
import re
import json

class NotFound(webapp2.RequestHandler):
    def get(self):
        self.error(404)

class MainPage(webapp2.RequestHandler):
    def get(self):
        url = 'http://www.vim.org/scripts/index.php'
        response = urllib2.urlopen(urllib2.Request(url), timeout=3)
        shtml = response.read()
        response.close()
        hdoc = HTML.fromstring(shtml)
        htree = etree.ElementTree(hdoc)
        lll = [z.replace('\xc2\xa0','') for z in [" ".join(y.split()) for y in [x for x in htree.xpath('/html/body/table[2]/tr/td[3]/table')[0].text_content().encode('utf-8').replace('\n\n','\n').strip('\n').strip('').strip(None).splitlines() if x != '']] if z != '']
        result = [[ lll[y], lll[y+1].split(':')[0], lll[y+1].split(':')[1] ] for y in [i for i,x in enumerate(lll) if re.search(r'^\[',x) != None]]

        result = json.dumps(result)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.write(result)

app = webapp2.WSGIApplication([
                ('/vimplugins', MainPage),
                ], debug=True)
