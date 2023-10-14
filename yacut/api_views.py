from flask import jsonify, request, url_for
from flask_api import status

from yacut import app
from yacut.exceptions import InvalidAPIUsage
from yacut.models import URLMap
from yacut.settings import SHORT_VIEW


EMPTY_DATA_MESSAGE = 'Отсутствует тело запроса'
EMPTY_ORIGINAL_LINK_MESSAGE = '"url" является обязательным полем!'
UNMATCH_SHORT_MESSAGE = 'Указанный id не найден'
INCORRECT_NAME_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
SHORT_ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_DATA_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_ORIGINAL_LINK_MESSAGE)
    try:
        map = URLMap.create(data.get('url'), data.get('custom_id'), True)
        return (
            jsonify(
                {
                    'url': map.original,
                    'short_link': url_for(
                        SHORT_VIEW, short=map.short, _external=True
                    ),
                }
            ),
            status.HTTP_201_CREATED,
        )
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    except RuntimeError as error:
        raise InvalidAPIUsage(
            str(error), status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_link(short):
    map = URLMap.get(short=short)
    if map is None:
        raise InvalidAPIUsage(UNMATCH_SHORT_MESSAGE, status.HTTP_404_NOT_FOUND)
    return jsonify({'url': map.original}), status.HTTP_200_OK
