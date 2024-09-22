#!/usr/bin/env python3
"""
Flask application for internationalization (i18n) using Flask-Babel.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from pytz.exceptions import UnknownTimeZoneError


app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration class for Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.timezoneselector
def get_timezone():
    """
    Determines the best time zone based on URL parameters, user settings,
    or defaults to UTC.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass
    if g.user:
        user_timezone = g.user.get('timezone')
        if user_timezone:
            try:
                return pytz.timezone(user_timezone).zone
            except UnknownTimeZoneError:
                pass
    return 'UTC'


@babel.localeselector
def get_locale():
    """
    Determine the best match with the supported languages.
    """
    locale_param = request.args.get('locale')
    if locale_param in app.config['LANGUAGES']:
        return locale_param
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    locale_header = request.headers.get('locale')
    if locale_header in app.config['LANGUAGES']:
        return locale_header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    Retrieve user based on login_as parameter.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        user_id = int(user_id)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """
    Execute before each request to set the user.
    """
    g.user = get_user()


@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(debug=True)
