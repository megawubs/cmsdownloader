Keep your CMS pre installations up to date.
===========================================

This script is designed to make live a little bit easyer. In my daily work I noted that we had to upload Magento and Joomla! (our most used CMS systems) a lot to our test servers and I thought this must, and can be, easyer. So, here it is. A python script designed to run as a cronjob to keep a base installation of your favorite CMS on your server that you only have to copy into the new directory.

It makes a directory structure like this:
```
Magento
	version
		the magento files here
Joomla
	version
		the joomla files here
```
When there is a new version, it'll keep the older version and just make a new version folder.

### Adding your own CMS to download

It's really easy to add your own downloader, just add your own htmlparser in app/htmlparsers.py and your own downloader in downloader.py and it should work. The downloader class has build in download, unzip, version check and delete functions that you can use for your custom CMS download function. I'm planning on making this proces easyer.


