from flask import jsonify, request
from flask_api import status

from yacut import app
from yacut.exceptions import InvalidAPIUsage
from yacut.models import URLMap


EMPTY_DATA_MESSAGE = 'Отсутствует тело запроса'
EMPTY_ORIGINAL_LINK_MESSAGE = '"url" является обязательным полем!'
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
    map = URLMap.create_short_id(original, short_id)
    return (
        jsonify(
            {
                'url': map.original,
                'short_link': request.root_url + map.short,
            }
        ),
        status.HTTP_201_CREATED,
    )


@app.route('/api/id/<short>/', methods=['GET'])
def get_short_link(short):
    url = URLMap.map_by_parameters(short=short)
    if url is None:
        raise InvalidAPIUsage(
            UNMATCH_SHORT_ID_MESSAGE, status.HTTP_404_NOT_FOUND
        )
    return jsonify({'url': url.original}), status.HTTP_200_OK
