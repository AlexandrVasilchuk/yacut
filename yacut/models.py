from datetime import datetime
from random import choices
from typing import Optional

from yacut import db
from yacut.exceptions import InvalidAPIUsage
from yacut.settings import (
    AUTOMATIC_SHORT_ID_LENGTH,
    ATTEMPTS_COUNT,
    LINK_LENGTH,
    SHORT_ID_LENGTH,
    SHORT_ID_ALLOWED_CHARS,

)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def map_by_parameters(**kwargs) -> Optional['URLMap']:
        return URLMap.query.filter_by(**kwargs).first()

    @staticmethod
    def create_short_id(
        original_link: str, custom_short_id: str = None
    ) -> 'URLMap':
        if custom_short_id is None:
            for _ in range(ATTEMPTS_COUNT):
                custom_short_id = ''.join(
                    choices(
                        SHORT_ID_ALLOWED_CHARS, k=AUTOMATIC_SHORT_ID_LENGTH
                    )
                )
                if URLMap.map_by_parameters(short=custom_short_id) is None:
                    break
        else:
            if not (
                len(custom_short_id) <= 16
                and set(custom_short_id) <= set(SHORT_ID_ALLOWED_CHARS)
            ):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if URLMap.map_by_parameters(short=custom_short_id) is not None:
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
        map = URLMap(original=original_link, short=custom_short_id)
        db.session.add(map)
        db.session.commit()
        return map

    def __repr__(self):
        return f"{self.__class__.__name__}{self.id, self.original, self.short}"
