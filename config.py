class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'
    CSRF_ENABLED = True
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False