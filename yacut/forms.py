from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from yacut.settings import SHORT_ID_LENGTH, LINK_LENGTH, MINIMAL_LENGTH


ORIGINAL_LINK_LABEL = 'Ссылка на оригинальный источник'
CUSTOM_ID_LABEL = 'Может есть какое-то пожелание'
SUBMIT_LABEL = 'Создать'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'


class URLMapForm(FlaskForm):
    original_link = StringField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_MESSAGE),
            Length(MINIMAL_LENGTH, LINK_LENGTH),
            URL(),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[Optional(), Length(MINIMAL_LENGTH, SHORT_ID_LENGTH)],
    )
    submit = SubmitField(SUBMIT_LABEL)
