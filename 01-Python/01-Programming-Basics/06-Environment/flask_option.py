# pylint: disable=missing-docstring

import os

def start():
    """returns the right message"""
    if 'FLASK_ENV' not in os.environ:
        message = "Starting in production mode..."
    elif os.environ['FLASK_ENV'] == 'development':
        message = "Starting in development mode..."
    elif os.environ['FLASK_ENV'] == 'production':
        message = "Starting in production mode..."
    return message


if __name__ == "__main__":
    print(start())
