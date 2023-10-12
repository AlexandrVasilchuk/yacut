import random
from typing import Optional

from flask import (
    render_template,
    abort,
    redirect,
    flash,
    request,
)

from yacut import app, db
from yacut.models import URLMap
from yacut.forms import URLMapForm
from yacut.settings import SHORT_ID_ALLOWED_CHARS


NOT_UNIQUE_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)


def generate_short_id(allowed_chars: str) -> str:
    return ''.join(char for char in random.choices(allowed_chars, k=6))


def short_id_exists(short_id: str) -> Optional[URLMap]:
    object = URLMap.query.filter_by(short=short_id).first()
    return object if object is not None else None


def get_unique_short_id(allowed_chars: str = SHORT_ID_ALLOWED_CHARS) -> str:
    short_id = generate_short_id(allowed_chars)
    while short_id_exists(short_id):
        short_id = generate_short_id(allowed_chars)
    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id_exists(short_id):
            flash(NOT_UNIQUE_SHORT_ID_MESSAGE)
            return render_template('index.html', form=form)
        if not short_id:
            short_id = get_unique_short_id()
        db.session.add(
            URLMap(original=form.original_link.data, short=short_id)
        )
        db.session.commit()
        return render_template(
            'index.html', form=form, result=request.url + short_id
        )
    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def redirect_to_short(short: str):
    object = short_id_exists(short)
    if object is None:
        return abort(404)
    return redirect(object.original), 302
