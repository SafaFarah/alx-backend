#!/usr/bin/env python3
"""
a script sets up a basic Flask app with localization support using Flask-Babel.
"""

from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """
    Configuration class for Flask app with localization settings.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
