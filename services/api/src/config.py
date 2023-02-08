import os


def get_db_url(user=None, password=None, host=None, port=None, database_name=None):
    database_name = database_name or os.environ.get('POSTGRES_DB')
    host = host or os.environ.get('POSTGRES_HOST')
    password = password or os.environ.get('POSTGRES_PASSWORD')
    port = port or os.environ.get('POSTGRES_PORT')
    user = user or os.environ.get('POSTGRES_USER')

    return f'postgresql://{user}:{password}@{host}:{port}/{database_name}'


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    # noinspection PyPep8Naming
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_db_url()


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    # noinspection PyPep8Naming
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        database_name = os.environ.get('POSTGRES_DB')

        return get_db_url(database_name=f'{database_name}-test')
