import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default="SUP3R-S3CR3T-K3Y-F0R-MY-PR0J3CT"
    )


MINIMAL_LENGTH = 1
SHORT_ID_LENGTH = 16
LINK_LENGTH = 2_000
AUTOMATIC_SHORT_ID_LENGTH = 6
ATTEMPTS_COUNT = 10
SHORT_ID_ALLOWED_CHARS = string.digits + string.ascii_letters
