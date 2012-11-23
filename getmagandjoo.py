#!/usr/bin/env python
# -----------------------------------------------------------------
# This program is created by Bram Wubs.
# Developed at B&S Media 2012 as a idea to always keep an fresh and
# up to date version of both joomla and magento on their test server.
# 
# This program is designed to run as a crontab, and will probably 
# only run once a few moths. If it's desired, you can turn off downloding
# Joomla or Magento by simply commenting d.getMage() or d.getJom() out, to
# turn it on again, uncomment it.
# If there are any problems, errors or this script stopped working,
# plese contact me.
# -----------------------------------------------------------------

from app import downloader

if __name__ == "__main__":
    #initiate the downloader
    d = downloader('/Volumes/Extra HDD/BSMedia/')
    d.l.info('Starting----------------------------------------------')
    #get the latest Magento version
    d.getMage()
    #get the latest Joomla version
    d.getJom()
    d.l.info("Stopping----------------------------------------------")