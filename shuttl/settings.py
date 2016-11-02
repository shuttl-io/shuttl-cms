import os
import datetime

class Config(object):
    BASE_DIR        		= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DEBUG					= False
    TESTING                 = False
    SECRET_KEY				= ''
    USERNAME 				= 'admin'
    PASSWORD 				= 'Paswword'
    AESKEY					= ''
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_DIR = os.path.join(BASE_DIR, "media")
    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''
    SENDGRID_APIKEY = ""
    VALID_EXP = datetime.timedelta(days=3)
    BASEPRICE = 10.00
    SERVER_NAME = "shuttl.io"
    LOG_PATH = BASE_DIR
    PID_PATH = BASE_DIR
    SHOULD_SKIP = True
    DB_PASSWORD = ""
    RESERVED_ORGANIZATONS = {"docs", "doc", "api", "dev", "developer", "blog", "admin", "mail", "marketplace",
                    "market", "store", "app", "hosting", "host", "tools", "application", "apply", "contact",
                    "about"}
    MAILCHIMP_TOKEN = ""
    MAILCHIMP_URL = "https://us13.api.mailchimp.com/3.0"
    GITHUB_CLIENT_ID = ""
    GITHUB_CLIENT_SECRET = ""
    AWS_PUBLIC = ""
    AWS_PRIVATE = ""
    pass

class TestConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    TESTING = True
    SHOULD_SKIP = True
    SERVER_NAME = "shuttl.com:5000"
    UPLOAD_DIR = os.path.join(Config.BASE_DIR, "test-media")
    SQLALCHEMY_DATABASE_URI = "postgres://shuttl:{0}@162.243.83.127/shuttl_build".format(Config.DB_PASSWORD)
    pass

class LocalTestConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    TESTING = True
    SERVER_NAME = "shuttl.com:5000"
    UPLOAD_DIR = os.path.join(Config.BASE_DIR, "test-media")
    SQLALCHEMY_DATABASE_URI = "postgres:///shuttl_test"

    GITHUB_CLIENT_ID = ""
    GITHUB_CLIENT_SECRET = ""
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "shuttl.com:5000"
    SQLALCHEMY_DATABASE_URI = "postgres://shuttl_db@localhost/shuttl_dev"
    pass

class LiveDevelopmentConfig(Config):
    SERVER_NAME = "shuttl.io"
    GITHUB_CLIENT_ID = "
    GITHUB_CLIENT_SECRET = "
    SQLALCHEMY_DATABASE_URI = "postgres://shuttl:{0}@162.243.83.127/shuttl".format(Config.DB_PASSWORD)
    DEBUG = True
    LOG_PATH = "/var/log/shuttl"
    PID_PATH = "/var/run"
    pass

class PublishConfig(Config):
    SERVER_NAME = "shuttl.io"
    GITHUB_CLIENT_ID = ""
    GITHUB_CLIENT_SECRET = ""
    SQLALCHEMY_DATABASE_URI = "postgres://shuttl:{0}@162.243.83.127/shuttl".format(Config.DB_PASSWORD)
    LOG_PATH = "/var/log/shuttl"
    PID_PATH = "/var/run/shuttl"
    pass


class ProductionConfig(Config):
    LOG_PATH = "/var/log/shuttl"
    PID_PATH = "/var/run"
    pass
