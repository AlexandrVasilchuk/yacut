from flask import render_template, jsonify
from flask_api import status

from yacut import app, db
from yacut.exceptions import InvalidAPIUsage


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), status.HTTP_404_NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code
