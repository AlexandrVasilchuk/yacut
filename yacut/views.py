from flask import (
    abort,
    flash,
    render_template,
    redirect,
    request,
)
from flask_api import status

from yacut import app
from yacut.exceptions import InvalidAPIUsage
from yacut.forms import URLMapForm
from yacut.models import URLMap


NOT_UNIQUE_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
SHORT_ADDRESS = ''


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    short_id = form.custom_id.data
    try:
        map = URLMap.create_short_id(form.original_link.data, short_id)
    except InvalidAPIUsage:
        flash(NOT_UNIQUE_SHORT_ID_MESSAGE)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        result=request.root_url + SHORT_ADDRESS + map.short,
    )


@app.route(f'{SHORT_ADDRESS}/<short>', methods=['GET'])
def redirect_to_short(short: str):
    map = URLMap.map_by_parameters(short=short)
    if map is None:
        return abort(status.HTTP_404_NOT_FOUND)
    return redirect(map.original), status.HTTP_302_FOUND
