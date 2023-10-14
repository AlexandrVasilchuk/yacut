import os
import string
import re


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='SUP3R-S3CR3T-K3Y-F0R-MY-PR0J3CT'
    )


SHORT_LENGTH = 16
LINK_LENGTH = 2_000
AUTOMATIC_SHORT_LENGTH = 6
ATTEMPTS_COUNT = 10
SHORT_VIEW = 'redirect_original'
SHORT_ALLOWED_CHARS = string.digits + string.ascii_letters
SHORT_ALLOWED_EXPRESSION = rf'^[{re.escape(SHORT_ALLOWED_CHARS)}]+$'
