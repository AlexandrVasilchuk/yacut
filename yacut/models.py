import re
from datetime import datetime
from random import choices
from typing import Optional

from yacut import db
from yacut.settings import (
    AUTOMATIC_SHORT_LENGTH,
    ATTEMPTS_COUNT,
    LINK_LENGTH,
    SHORT_LENGTH,
    SHORT_ALLOWED_CHARS,
    SHORT_ALLOWED_EXPRESSION,
)


ORIGINAL_LINK_TOO_LONG = 'Длинна ссылки превышает максимально допустимую'
SHORT_NOT_GENERATED = 'Не удалось сгенерировать подходящий short_id'
INCORRECT_NAME_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(**kwargs) -> Optional['URLMap']:
        return URLMap.query.filter_by(**kwargs).first()

    @staticmethod
    def generate_unique_short():
        for _ in range(ATTEMPTS_COUNT):
            short = ''.join(choices(SHORT_ALLOWED_CHARS, k=AUTOMATIC_SHORT_LENGTH))
            if URLMap.get(short=short) is None:
                return short
        raise RuntimeError(SHORT_NOT_GENERATED)

    @staticmethod
    def create(
        original_link: str, short: str = None, validate: bool = False
    ) -> 'URLMap':
        if validate and len(original_link) > LINK_LENGTH:
            raise ValueError(ORIGINAL_LINK_TOO_LONG)
        if not short:
            short = URLMap.generate_unique_short()
        else:
            if validate and not (
                len(short) <= SHORT_LENGTH
                and re.match(SHORT_ALLOWED_EXPRESSION, short)
            ):
                raise ValueError(INCORRECT_NAME_SHORT)
            if URLMap.get(short=short) is not None:
                raise ValueError(SHORT_ALREADY_EXISTS)
        map = URLMap(original=original_link, short=short)
        db.session.add(map)
        db.session.commit()
        return map

    def __repr__(self):
        return f'{self.__class__.__name__}{self.id, self.original, self.short}'
