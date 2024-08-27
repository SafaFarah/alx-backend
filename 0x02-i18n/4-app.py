#!/usr/bin/env python3
"""
Flask application with Babel for internationalization.
"""

from flask import Flask, request, render_template
from flask_babel import Babel, _

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best locale to use for this request.
    """
    locale = request.args.get('locale')
    if locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    return request.accept_languages.best_match(
        app.config['BABEL_SUPPORTED_LOCALES']
    )


@app.route('/')
def index() -> str:
    """
    Returns:str: Rendered HTML template for the index page.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
