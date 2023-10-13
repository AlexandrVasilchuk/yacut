import re
from datetime import datetime
from random import choices
from typing import Optional

from yacut import db
from yacut.settings import (
    AUTOMATIC_SHORT_ID_LENGTH,
    ATTEMPTS_COUNT,
    LINK_LENGTH,
    SHORT_ID_LENGTH,
    SHORT_ID_ALLOWED_CHARS,
    SHORT_ID_ALLOWED_EXPRESSION,
)


ORIGINAL_LINK_TOO_LONG = 'Длинна ссылки превышает максимально допустимую'
SHORT_ID_NOT_GENERATED = 'Не удалось сгенерировать подходящий short_id'
INCORRECT_NAME_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
SHORT_ID_ALREADY_EXISTS = (
    'Предложенный вариант короткой ссылки уже существует.'
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(**kwargs) -> Optional['URLMap']:
        return URLMap.query.filter_by(**kwargs).first()

    @staticmethod
    def create_short_id(
        original_link: str, custom_short_id: str = None
    ) -> 'URLMap':
        if len(original_link) > LINK_LENGTH:
            raise ValueError(ORIGINAL_LINK_TOO_LONG)
        if not custom_short_id:
            for _ in range(ATTEMPTS_COUNT):
                custom_short_id = ''.join(
                    choices(
                        SHORT_ID_ALLOWED_CHARS, k=AUTOMATIC_SHORT_ID_LENGTH
                    )
                )
                if URLMap.get(short=custom_short_id) is None:
                    break
                raise UnboundLocalError(SHORT_ID_NOT_GENERATED)
        else:
            if not (
                len(custom_short_id) <= SHORT_ID_LENGTH
                and re.match(SHORT_ID_ALLOWED_EXPRESSION, custom_short_id)
            ):
                raise NameError(INCORRECT_NAME_SHORT_ID)
            if URLMap.get(short=custom_short_id) is not None:
                raise ValueError(SHORT_ID_ALREADY_EXISTS)
        map = URLMap(original=original_link, short=custom_short_id)
        db.session.add(map)
        db.session.commit()
        return map

    def __repr__(self):
        return f"{self.__class__.__name__}{self.id, self.original, self.short}"
