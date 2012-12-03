import logging, os

class MyLogger:

    def __init__(self, location):
        self.logger = logging.getLogger('cmsdownloader')
        handler = logging.FileHandler(os.path.join(location,'CMS Downloader.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)