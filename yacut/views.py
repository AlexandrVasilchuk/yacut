from flask import (
    abort,
    flash,
    render_template,
    redirect,
    url_for,
)
from flask_api import status

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap


NOT_UNIQUE_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    short_id = form.custom_id.data
    try:
        return render_template(
            'index.html',
            form=form,
            result=url_for(
                'redirect_to_short',
                short=URLMap.create_short_id(
                    form.original_link.data, short_id
                ).short,
                _external=True,
            ),
        )

    except ValueError:
        flash(NOT_UNIQUE_SHORT_ID_MESSAGE)
        return render_template('index.html', form=form)
    except UnboundLocalError:
        return abort(status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/<short>', methods=['GET'])
def redirect_to_short(short: str):
    map = URLMap.get(short=short)
    if map is None:
        return abort(status.HTTP_404_NOT_FOUND)
    return redirect(map.original), status.HTTP_302_FOUND
