from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from yacut.settings import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import views, models, api_views, error_handlers
