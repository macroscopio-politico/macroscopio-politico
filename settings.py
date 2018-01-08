import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID')
    DISQUS_SRC = os.environ.get('DISQUS_SRC')
    SHARETHIS_SRC = os.environ.get('SHARETHIS_SRC')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
