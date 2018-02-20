import logging
import coloredlogs
import nsfval.sdk.api.client as nsfval_api_client
import nsfval.sdk.api.settings as config

log = logging.getLogger(__name__)
coloredlogs.install(level=config.LOG_LEVEL)

results = {}


def _build_url(o_type):
    base_url = 'http://{0}:{1}'.format(config.API_HOST, config.API_PORT)
    return '{0}/validate/{1}'.format(base_url, o_type)


def _validate(o_type, o_format, flags, o_file, report=False):
    url = _build_url(o_type)
    rsp = nsfval_api_client.post(url, o_format, flags=flags, post_file=o_file)
    if rsp.status_code != 200:
        log.debug("Couldn't validate resource. Server replied: {}".format(rsp.status_code))
        return

    content = rsp.json()
    print(content)

    # make sure results are not repeated by creating a dict for them (key: resource_id)
    rr = results[content['resource_id']] = dict()
    rr['error_count'] = content['error_count']
    rr['warning_count'] = content['warning_count']

    return rr


def update_config(nsfval_host=None, nsfval_port=None, log_level=None):
    if nsfval_host:
        config.NSFVAL_HOST = nsfval_host

    if nsfval_port:
        config.NSFVAL_PORT = nsfval_port

    if log_level:
        config.LOG_LEVEL = log_level
        coloredlogs.install(level=log_level)


def validate_ns(o_format, flags, nsd_file, report=False):
    return _validate('ns', o_format, flags, nsd_file, report=report)


def validate_vnf(o_format, flags, vnfd_file, report=False):
    return _validate('vnf', o_format, flags, vnfd_file, report=report)


def validate_pkg(o_format, flags, pkg_file, report=False):
    return _validate('package', o_format, flags, pkg_file, report=report)


def validate_prj(o_format, flags, prj_file, report=False):
    return _validate('project', o_format, flags, prj_file, report=report)
