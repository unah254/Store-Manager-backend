'''Set up environment specific configurations'''
import os


class Config(object):
    '''Parent configuration class'''
    DEBUG = False
    CSRF_ENABLED = True

    DB_HOST = os.getenv('DB_HOST')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    SECRET_KEY = os.getenv("SECRET_KEY")


class Development(Config):
    '''Configuration for development'''
    DEBUG = True


class Testing(Config):
    '''Configuration for testing'''
    TESTING = True
    DEBUG = True

    # DB_HOST = os.getenv('DB_HOST')
    # DB_USERNAME = os.getenv('DB_USERNAME')
    # DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAMET')


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