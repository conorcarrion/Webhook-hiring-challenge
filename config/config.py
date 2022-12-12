class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DATABASE_URI = "postgresql+psycopg2://postgres:pgpassword@postgres:5432/postgres"


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
