#!/usr/bin/env python

import urllib, urllib2, os, sys, logging
from pprint import pprint
from HTMLParser import HTMLParser
from zipfile import ZipFile as zip

class MyLogger:

    def __init__(self):
        self.logger = logging.getLogger('getmageandjo')
        handler = logging.FileHandler('Magento Joomla Downloader.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

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
        self.mageDownloadPage   = 'https://www.magentocommerce.com/download'
        self.mageDownloadUrl    = 'http://www.magentocommerce.com/downloads/assets/%s/%s'
        self.jomDownloadPage    = 'http://www.joomla.org/download.html'
        self.basePath           = basePath
        self.downloadFiles      = True
        self.pathToMake         = ''
        self.l                  = MyLogger().logger
        self.zipFile            = ''
        if not os.path.isdir(self.basePath):
            self.log.error('Path to download to does not exist')
            exit()
    ## 
    # Downloads Magento if the lates version is not already downloaded 
    def getMage(self):
        self.l.info("Searching Magento's latest version")
        version = self.getMageLatestVersion() #get the latest Magento version
        self.l.info("Magento's latest version is: %s" % (version))
        #if the latest version is not yet downloaded, download it
        filename = 'magento-'+version+'.zip'
        if not self.checkVersion("Magento", version, filename):
            self.l.info("It's a new version, lets download it!")
            # self.versions['Magento'].append(version) #append the version into the versions dict
            # create the download url based on the version
            
            # theUrl  = 'http://www.magentocommerce.com/downloads/assets/'+version+'/'+filename
            theUrl = self.mageDownloadUrl % (version, filename)
            self.l.info("Made download url for Magento: %s" % (theUrl))
            self.createPath() #create the path needed for the download
            self.download(theUrl) #download tha sjizzle!!
            self.unzip(self.zipFile)
        else: #print a nice notice if the version already exsists
            self.l.info("version %s of Magento is already downloaded" % (version))
    ## 
    # Gets the latest magento version number 
    def getMageLatestVersion(self):
        #read the download page
        self.l.info("Let's chew on some HTML from %s" % (self.mageDownloadPage))
        downloadPage    = self.bot.GET(self.mageDownloadPage)   
        parser          = MagentoParser() #initiate the parser
        parser.feed(downloadPage) #feed it some data!
        allMageVersions = parser.versions #get the versions
        newest          = allMageVersions[0] #i want the newest
        return newest

    ## 
    # Gets the latest Joomla version if it does not exsists 
    def getJom(self):
        #Get some html data from the joomla download page
        self.l.info("Searching for Joomla's latest versions")
        self.l.info("Let's chew on some HTML from %s" % (self.jomDownloadPage))
        html            = self.bot.GET(self.jomDownloadPage)
        parser          = JoomlaParser() #start the parser
        self.l.info("Getting the versions")
        parser.feed(html) #give it some nice html to chew on
        #the parser finds two download urls (the stable used by the world and the next stable release)
        #get them both
        for link in parser.downloadLinks:
            
            filename = link.split('/')[-1] #get the file name
            version  = filename.split('_')[1] #get the version
            self.l.info("Version is: %s" % (version))
            #check if the version already exsists,
            if not self.checkVersion('Joomla', version, filename):
                #if not, create the download path
                self.l.info("It's a new version, lets downoad it!")
                self.createPath()
                #and download that pice file!
                self.download(link)
                self.unzip(self.zipFile)
            else: #otherwise, let them know that this version is already downloaded
                self.l.info("Version %s already downloaded" % (version))
    ## 
    # Downloads the file url given to it into the packages's folder
    # based on self.downloadPath
    # @url string the file to download 
    def download(self, url):
        #the filename
        file_name = url.split('/')[-1]
        #complete path to the file that will be downloaded shortly
        file_path = os.path.join(self.downloadPath, file_name)
        #let them know what we are going to do 
        self.l.info("Getting ready to download %s to %s" %(file_name, file_path))
        #just for development a check to download or not
        if self.downloadFiles:
            #open the url
            u         = urllib2.urlopen(url)
            #open a binary file
            f         = open(file_path, 'wb')
            #get some info
            meta      = u.info()
            #get the file size
            file_size = int(meta.getheaders("Content-Length")[0])
            #let them know some info
            self.l.info("Downloading: %s Bytes: %s" % (file_name, file_size))
            #the download bar
            file_size_dl = 0
            block_sz     = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                # file_size_dl += len(buffer)
                f.write(buffer)
                # status       = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                # status       = status + chr(8)*(len(status)+1)
                # self.l.info(status)

            f.close()
            self.l.info("Done downloading %s" % (file_name))
            self.zipFile = file_path
        
    ## 
    # Checks if the folder structure for the given package and version already exsists
    # @package string name of the package (like "Magento")
    # @version string the version of the package (like "1.7.0.1") 
    def checkVersion(self, package, version, filename):
        folderPath = os.path.join(self.basePath, os.path.join(package, version))
        filePath = os.path.join(self.basePath, os.path.join(package, os.path.join(version, filename)))
        pathExsists = os.path.exists(filePath)
        if not pathExsists:
            self.pathToMake = folderPath
        return pathExsists

    ## Creates the path
    # based on self.pathToMake 
    def createPath(self):
        path = self.pathToMake
        if not os.path.exists(path):
            os.makedirs(path)
            self.l.info("Created %s" % (path))
        self.downloadPath = path

    def unzip(self, _file):
        self.l.info("\t Unzipping %s" % (_file))
        _dir = os.path.dirname(_file)
        self.l.info("\t Extracting into: %s" % (_dir))
        z = zip(_file)
        for f in z.namelist():
            if f.endswith('/'):
                os.makedirs(os.path.join(_dir, f))
            else:
                z.extract(os.path.join(_dir,f))

class JoomlaParser(HTMLParser):
    inDownloadButton = False #Get sets to True when the download button is found
    downloadLinks = [] #will contain the two Joomla download links
    def handle_starttag(self, tag, attrs):
        #if we are in the download button,
        if self.inDownloadButton:
            # search for a "a" tag
            if tag == "a":
                #append the href attribute to the download links
                self.downloadLinks.append(attrs[0][1])
        #check for div's
        if tag == "div":
            #we only need the download button div
            if attrs[0][1] == 'downloadbutton':
                #let the class know we have entered the download div
                self.inDownloadButton = True
        else:
            #if we're no longer in the download div, set it to false
            self.inDownloadButton = False

class MagentoParser(HTMLParser):
    versions = [] #list that will contain all magento versions (with the latest on index 0)
    def handle_starttag(self, tag, attrs):
        #I only want to handle option tags
        if tag == "option":
            #check if the tag has attributes
            if len(attrs):
                down = attrs[0][1]  #the download link
                #check if it's a tar.gz file to make sure there are no duplicates of versions
                if 'tar.gz' in down:
                    #check if its a actually magento file 
                    if 'magento' in down:
                        version = down.split('/')[0] #get the version
                        self.versions.append(version) #append it to the versions list

if __name__ == "__main__":
    #initiate the downloader
    d = downloader('/Volumes/Extra HDD/BSMedia/')
    d.l.info('Starting check----------------------------------------')
    #get the latest Magento version
    d.getMage()
    #get the latest Joomla version
    d.getJom()
    d.l.info("Stopping----------------------------------------------")