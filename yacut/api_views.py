from flask import jsonify, request

from yacut.models import URLMap
from yacut import app, db
from yacut.exceptions import InvalidAPIUsage
from yacut.settings import SHORT_ID_ALLOWED_CHARS
from yacut.views import (
    get_unique_short_id,
    NOT_UNIQUE_SHORT_ID_MESSAGE,
    short_id_exists,
)


EMPTY_DATA_MESSAGE = 'Отсутствует тело запроса'
EMPTY_ORIGINAL_LINK_MESSAGE = '"url" является обязательным полем!'
NOT_ALLOWED_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
UNMATCH_SHORT_ID_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_DATA_MESSAGE)

    original = data.get('url')
    short_id = data.get('custom_id')
    if original is None:
        raise InvalidAPIUsage(EMPTY_ORIGINAL_LINK_MESSAGE)
    if short_id is not None:
        if len(short_id) <= 16 and all(
            (char in SHORT_ID_ALLOWED_CHARS for char in short_id)
        ):
            if short_id_exists(short_id):
                raise InvalidAPIUsage(NOT_UNIQUE_SHORT_ID_MESSAGE)
        else:
            raise InvalidAPIUsage(NOT_ALLOWED_SHORT_ID_MESSAGE)
    else:
        short_id = get_unique_short_id()
    db.session.add(URLMap(original=original, short=short_id))
    db.session.commit()
    return (
        jsonify(
            {
                'url': original,
                'short_link': request.root_url + short_id,
            }
        ),
        201,
    )


@app.route('/api/id/<short>/', methods=['GET'])
def get_short_link(short):
    url = short_id_exists(short)
    if url is None:
        raise InvalidAPIUsage(UNMATCH_SHORT_ID_MESSAGE, 404)
    return jsonify({'url': url.original}), 200
