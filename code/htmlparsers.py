from HTMLParser import HTMLParser
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