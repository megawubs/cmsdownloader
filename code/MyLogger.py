import logging

class MyLogger:

    def __init__(self):
        self.logger = logging.getLogger('getmageandjo')
        handler = logging.FileHandler('Magento Joomla Downloader.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)