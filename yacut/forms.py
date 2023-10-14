from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from yacut.settings import (
    LINK_LENGTH,
    SHORT_LENGTH,
    SHORT_ALLOWED_EXPRESSION,
)

ORIGINAL_LINK_LABEL = 'Ссылка на оригинальный источник'
CUSTOM_ID_LABEL = 'Может есть какое-то пожелание'
SUBMIT_LABEL = 'Создать'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_MESSAGE),
            Length(max=LINK_LENGTH),
            URL(),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Optional(),
            Length(max=SHORT_LENGTH),
            Regexp(SHORT_ALLOWED_EXPRESSION),
        ],
    )
    submit = SubmitField(SUBMIT_LABEL)
