import os

SDK_MODE = os.environ.get("NSFVAL_SDK_MODE") or 'api'  # 'api' or 'lib'
API_HOST = os.environ.get('NSFVAL_API_HOST') or '127.0.0.1'
API_PORT = os.environ.get('NSFVAL_API_PORT') or '5050'
LOG_LEVEL = os.environ.get('NSFVAL_LOG_LEVEL') or 'info'


# shape vars
SDK_MODE = str(SDK_MODE).lower()
if SDK_MODE == 'lib':
    try:
        from nsfval.core import Validator
    except ImportError:
        print("NSFVal core not found. Either set 'NSFVAL_SDK_MODE to 'api' "
              "or install nsfval-core library.")
        exit(1)
