class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:pgpassword@db:5432/postgres"
    )


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:pgpassword@db-test:5433/testing"
    )
    TESTING = True
