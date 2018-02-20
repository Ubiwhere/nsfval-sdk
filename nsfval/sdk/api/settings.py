import os

API_HOST = os.environ.get('NSFVAL_API_HOST') or '127.0.0.1'
API_PORT = os.environ.get('NSFVAL_API_PORT') or '5050'
LOG_LEVEL = os.environ.get('NSFVAL_LOG_LEVEL') or 'info'
