from htmlparsers import JoomlaParser, MagentoParser, wordPressParser
from httpbot import HttpBot
from MyLogger import MyLogger
from zipfile import ZipFile as zip
import os, sys, urllib2

class downloader:
    def __init__(self, basePath):
        self.basePath           = basePath
        self.bot                = HttpBot()
        self.mageDownloadPage   = 'https://www.magentocommerce.com/download'
        self.wpDownloadPage     = 'http://nl.wordpress.org/'
        self.mageDownloadUrl    = 'http://www.magentocommerce.com/downloads/assets/%s/%s'
        self.jomDownloadPage    = 'http://www.joomla.org/download.html'
        self.downloadFiles      = True
        self.pathToMake         = ''
        self.zipFile            = ''
        self.errorMsg           = 'ERROR: Path to download location to does not exist'
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
            self.delFile(self.zipFile)
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
                self.delFile(self.zipFile)
            else: #otherwise, let them know that this version is already downloaded
                self.l.info("Version %s already downloaded" % (version))

    def getWordPress(self):
        self.l.info('Searching for Wordpress latest version')
        html = self.bot.GET(self.wpDownloadPage)
        parser = wordPressParser()
        self.l.info("Let's chew on some HTML from %s" % (self.wpDownloadPage))
        parser.feed(html)
        self.l.info('Version is: %s' % (parser.version))
        if not self.checkVersion('Wordpress', parser.version, parser.filename):
            self.l.info("It's a new version, lets downoad it!")
            self.createPath()
            self.download(parser.url)
            self.unzip(self.zipFile)
            self.delFile(self.zipFile)
        else:
            self.l.info("Version %s already downloaded" % (parser.version))
        # print parser.url
        # pprint(parser)

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

                f.write(buffer)                

            f.close()
            self.l.info("Done downloading %s" % (file_name))
            self.zipFile = file_path
        
    ## 
    # Checks if the folder structure for the given package and version already exsists
    # @package string name of the package (like "Magento")
    # @version string the version of the package (like "1.7.0.1") 
    def checkVersion(self, package, version, filename):
        folderPath = os.path.join(self.basePath, os.path.join(package, version))
        # filePath = os.path.join(self.basePath, os.path.join(package, os.path.join(version, filename)))
        pathExsists = os.path.exists(folderPath)
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
    ## 
    # Unzip a file to the directory it's located in
    # @_file string A string of the full path to the file that needs to be unzipped 
    def unzip(self, _file):
        self.l.info("\t Unzipping %s" % (_file))
        #get the base dir to extract to
        _dir = os.path.dirname(_file)
        self.l.info("\t Extracting into: %s" % (_dir))
        z = zip(_file) #initiate the zip class, give it the file
        #Go over eatch file in the zip file
        for f in z.namelist():
            #when it ends with a / its a folder, make it
            if f.endswith('/'):
                os.makedirs(os.path.join(_dir, f))
            #if it doensn't end with a / its a file
            else:
                #make a binary file in the location
                outfile = open(os.path.join(_dir, f), 'wb')
                #write the file in the zip into the binary file
                outfile.write(z.read(f))
                #close the binary file
                outfile.close()
        self.l.info("\t Done unzipping %s" % (_file))

    def delFile(self, _file):
        if os.path.isfile(_file):
            os.remove(_file)
            self.l.info("\t Deleted %s" % (_file))

    def checkDir(self):
        return os.path.isdir(self.basePath)
            

    def startLogger(self):
        self.l = MyLogger(self.basePath).logger


