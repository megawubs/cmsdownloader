#!/usr/bin/env python

import urllib, urllib2, os, sys
from pprint import pprint
from HTMLParser import HTMLParser


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


class downloader:
    def __init__(self, basePath):
        self.bot                = HttpBot()
        self.magentoDownloadUrl = 'https://www.magentocommerce.com/download'
        self.versions           = {'Magento':[], 'Joomla':[]}
        self.downloadedFiles    = []
        self.basePath           = basePath
        self.downloadFiles      = True
        self.pathToMake        = ''
        if not os.path.isdir(self.basePath):
            print 'Path to download to does not exist'
            exit()

    def getMage(self):
        version = self.getMageLatestVersion()
        if not self.checkVersion("Magento", version):
            self.versions['Magento'].append(version)
            theUrl  = 'http://www.magentocommerce.com/downloads/assets/'+version+'/magento-'+version+'.tar.gz'
            self.createPath()
            self.download(theUrl)
        else:
            print "version %s already downloaded" % (version)

    def getMageLatestVersion(self):
        downloadPage    = self.bot.GET(self.magentoDownloadUrl)
        parser          = MagentoParser()
        parser.feed(downloadPage)
        allMageVersions = parser.versions
        newest          = allMageVersions[0]
        return newest


    def getJom(self):
        jomDownloadPage = 'http://www.joomla.org/download.html';
        html            = self.bot.GET(jomDownloadPage)
        parser          = JoomlaParser()
        parser.feed(html)
        for link in parser.downloadLinks:
            filename = link.split('/')[-1]
            version  = filename.split('_')[1]
            self.versions['Joomla'].append(version)
            if not self.checkVersion('Joomla', version):
                self.createPath()
                self.download(link)
            else:
                print "Version %s already downloaded" % (version)

    def download(self, url):
        file_name = url.split('/')[-1]
        file_path = os.path.join(self.downloadPath, file_name) 
        print "downloading "+os.path.join(self.downloadPath, file_name)
        if self.downloadFiles:
            u         = urllib2.urlopen(url)
            f         = open(file_path, 'wb')
            meta      = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)
            file_size_dl = 0
            block_sz     = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status       = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status       = status + chr(8)*(len(status)+1)
                print status,

            f.close()
        self.downloadedFiles.append(file_name)

    def checkVersion(self, package, version):
        path = os.path.join(self.basePath, os.path.join(package, version))
        pathExsists = os.path.exists(path)
        if not pathExsists:
            self.pathToMake = path
        return pathExsists

    def createPath(self):
        path = self.pathToMake
        os.makedirs(path)
        print "created %s" % (path)
        self.downloadPath = path


# create a subclass and override the handler methods
class JoomlaParser(HTMLParser):
    inDownloadButton = False
    downloadLinks = []
    def handle_starttag(self, tag, attrs):
        if self.inDownloadButton:
            if tag == "a":
                self.downloadLinks.append(attrs[0][1])
        if tag == "div":
            if attrs[0][1] == 'downloadbutton':
                self.inDownloadButton = True
        else:
            self.inDownloadButton = False

class MagentoParser(HTMLParser):
    versions = []
    def handle_starttag(self, tag, attrs):
        if tag == "option":
            if len(attrs):
                down = attrs[0][1]
                if 'tar.gz' in down:
                    if 'magento' in down:
                        version = down.split('/')[0]
                        self.versions.append(version)

if __name__ == "__main__":
    d = downloader('/Volumes/Extra HDD/BSMedia/')
    d.getMage()
    d.getJom()
    # d.handleFiles()