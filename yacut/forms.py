from re import IGNORECASE
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from yacut.settings import SHORT_ID_LENGTH, LINK_LENGTH


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
            Length(max=SHORT_ID_LENGTH),
            Regexp('^[A-Z/d]+$', flags=IGNORECASE),
        ],
    )
    submit = SubmitField(SUBMIT_LABEL)
