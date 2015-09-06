import os

class Config:

    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (
        os.environ.get('DATABASE_USERNAME', 'root'),
        os.environ.get('DATABASE_PASSWORD', 'password'),
        os.environ.get('DATABASE_HOST', 'localhost'),
        os.environ.get('DATABASE_DB', 'db'),
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
