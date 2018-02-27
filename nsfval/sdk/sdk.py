import logging
import coloredlogs
from nsfval.sdk import settings
from nsfval.sdk import api_client

log = logging.getLogger(__name__)
coloredlogs.install(level=settings.LOG_LEVEL)


def _build_result(error_count, warning_count):
    return {'error_count': error_count,
            'warning_count': warning_count}


def _validate_api(o_type, o_format, flags, o_file, addt_files=None):

    endpoint = 'validate/{0}'.format(o_type)

    rsp = api_client.post(endpoint, o_format, flags=flags, post_file=o_file, addt_files=addt_files)
    if rsp.status_code != 200:
        log.debug("Couldn't validate resource. Server replied: {}".format(rsp.status_code))
        return

    content = rsp.json()
    return _build_result(content['error_count'], content['warning_count'])


def _validate_lib(o_type, o_format, flags, o_file, addt_files=None):
    from nsfval.core import Validator
    from nsfval.core import pluginmanager
    from nsfval.config import Userconf
    from nsfval.adapter import LoaderPlugin

    userconf = Userconf()
    userconf.load_configuration(configfile=Userconf.defaultconfigfile)
    pluginmanager.load_plugins(userconf.plugins_dir)
    loader = pluginmanager.get_loader_plugin(o_format)

    val = Validator.create_validator(
        loader,
        True if 's' in flags else False,
        True if 'i' in flags else False,
        True if 't' in flags else False,
        addt_files if addt_files else list(),
        ['yaml', 'yml'],
        True
    )
    validate_callback = getattr(val, 'validate_{0}'.format(o_type))
    validate_callback(o_file)

    return _build_result(val.error_count, val.warning_count)


def _validate(o_type, o_format, flags, o_file, addt_files=None, report=False):
    result = validate_function(o_type, o_format, flags, o_file, addt_files=addt_files)
    return result


def validate_ns(o_format, flags, nsd_file, addt_files=None, report=False):
    """Validate a network service."""
    return _validate('ns', o_format, flags, nsd_file, addt_files=addt_files, report=report)


def validate_vnf(o_format, flags, vnfd_file, report=False):
    """Validate a virtual network function."""
    return _validate('vnf', o_format, flags, vnfd_file, report=report)


def validate_pkg(o_format, flags, pkg_file, report=False):
    """Validate a package."""
    return _validate('package', o_format, flags, pkg_file, report=report)


def validate_prj(o_format, flags, prj_file, report=False):
    """Validate a project."""
    return _validate('project', o_format, flags, prj_file, report=report)


def update_config(nsfval_host=None, nsfval_port=None, log_level=None):
    """Update configurations of the sdk."""
    if nsfval_host:
        settings.NSFVAL_HOST = nsfval_host

    if nsfval_port:
        settings.NSFVAL_PORT = nsfval_port

    if log_level:
        settings.LOG_LEVEL = log_level
        coloredlogs.install(level=log_level)


# sdk callback functions (service api or core library)
validate_function = locals()['_validate_{}'.format(settings.SDK_MODE)]
