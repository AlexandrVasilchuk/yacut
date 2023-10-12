import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")


MINIMAL_LENGTH = 1
SHORT_ID_LENGTH = 16
LINK_LENGTH = 256
SHORT_ID_ALLOWED_CHARS = string.digits + string.ascii_letters
