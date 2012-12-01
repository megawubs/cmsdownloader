#!/usr/bin/env python
# -----------------------------------------------------------------
# This program is created by Bram Wubs.
# The idea was to always keep an fresh and up to date version of 
# any cms system availble.
# 
# This program is designed to run as a crontab, and will probably 
# only run once every week. If it's desired, you can turn off downloding
# a CMS by simply commenting the line that downloads the cms out, to
# turn it on again, uncomment it.
# -----------------------------------------------------------------

from app import downloader

if __name__ == "__main__":
    #initiate the downloader
    d = downloader('/Volumes/Extra HDD/BSMedia/')
    if not d.checkDir():
		print d.errorMsg
    else:
		d.startLogger()
		d.l.info('Starting----------------------------------------------')
		#get the latest Magento version
		d.getMage()
		#get the latest Joomla version
		d.getJom()
		#get the latest Wordpress version
		d.getWordPress()
		d.l.info("Stopping----------------------------------------------")