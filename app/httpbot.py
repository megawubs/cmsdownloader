import urllib, urllib2

class HttpBot:
    """an HttpBot represents one browser session, with cookies."""
    def __init__(self):
        cookie_handler   = urllib2.HTTPCookieProcessor()
        redirect_handler = urllib2.HTTPRedirectHandler()
        self._opener     = urllib2.build_opener(redirect_handler, cookie_handler)

    def GET(self, url):
        return self._opener.open(url).read()

    def POST(self, url, parameters):
        return self._opener.open(url, urllib.urlencode(parameters)).read()