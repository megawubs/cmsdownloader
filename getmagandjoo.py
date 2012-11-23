#!/usr/bin/env python
# from code import downloader, htmlparsers, http

if __name__ == "__main__":
    #initiate the downloader
    d = downloader('/Volumes/Extra HDD/BSMedia/')
    d.l.info('Starting check----------------------------------------')
    #get the latest Magento version
    d.getMage()
    #get the latest Joomla version
    d.getJom()
    d.l.info("Stopping----------------------------------------------")