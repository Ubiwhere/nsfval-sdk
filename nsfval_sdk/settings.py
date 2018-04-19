import os
import logging
import coloredlogs

log = logging.getLogger(__name__)

SDK_MODE = os.environ.get("NSFVAL_SDK_MODE", 'api')  # 'api' or 'lib'
API_HOST = os.environ.get('NSFVAL_API_HOST', '127.0.0.1')
API_PORT = os.environ.get('NSFVAL_API_PORT', '5050')
LOG_COLORED = os.environ.get('NSFVAL_SDK_LOGS_COLORED', True)
LOG_LEVEL = os.environ.get('NSFVAL_LOG_LEVEL', 'info')

# install custom logs
if coloredlogs:
    coloredlogs.install(
        logger=log,
        level=LOG_LEVEL,
        fmt=os.environ.get('COLOREDLOGS_LOG_FORMAT', coloredlogs.DEFAULT_LOG_FORMAT),
        # level_styles=os.environ.get('COLOREDLOGS_LEVEL_STYLES', coloredlogs.DEFAULT_LEVEL_STYLES),
        field_styles=os.environ.get('COLOREDLOGS_FIELD_STYLES', coloredlogs.DEFAULT_FIELD_STYLES),
    )


# check sanity of env vars
SDK_MODE = str(SDK_MODE).lower()
assert SDK_MODE in ('api', 'lib'), log.error("Invalid SDK_MODE: '{0}'".format(SDK_MODE))
log.debug("SDK MODE set to '{0}': {1}."
          .format(SDK_MODE, "using the NSFVal core library"
                  if SDK_MODE == 'lib' else "using the NSFVal service API at '{0}:{1}'"
                                            .format(API_HOST, API_PORT)
                  )
          )
if SDK_MODE == 'lib':
    try:
        from nsfval.core import Validator
    except ImportError:
        log.critical("NSFVal core library not found. Please instal nsfval-core library.")
        exit(1)
