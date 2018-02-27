import logging
import coloredlogs
from nsfval.sdk import settings
from nsfval.sdk import api_client

log = logging.getLogger(__name__)
coloredlogs.install(level=settings.LOG_LEVEL)

# keep track of validation results
results = {}


def _validate(o_type, o_format, flags, o_file, addt_files=None, report=False):
    endpoint = 'validate/{0}'.format(o_type)

    rsp = api_client.post(endpoint, o_format, flags=flags, post_file=o_file, addt_files=addt_files)
    if rsp.status_code != 200:
        log.debug("Couldn't validate resource. Server replied: {}".format(rsp.status_code))
        return

    content = rsp.json()

    # make sure results are not repeated by creating a dict for them (key: resource_id)
    response = results[content['resource_id']] = dict()
    response['error_count'] = content['error_count']
    response['warning_count'] = content['warning_count']
    return response


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