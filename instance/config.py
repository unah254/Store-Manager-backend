'''Set up environment specific configurations'''
import os


class Config(object):
    '''Parent configuration class'''
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv(" SECRET_KEY")


class Development(Config):
    '''Configuration for development'''
    DEBUG = True


class Testing(Config):
    '''Configuration for testing'''
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Configuration for Staging."""
    DEBUG = False


class Production(Config):
    '''Configuration for production'''
    DEBUG = False
    TESTING = False


app_config = {
    'development': Development,
    'testing': Testing,
    'staging' : StagingConfig,
    'production': Production
}