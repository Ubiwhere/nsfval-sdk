import logging
from nsfval_sdk import settings
from nsfval_sdk.api import client as api_client

log = logging.getLogger(__name__)


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

    resource_id = content['resource_id']

    result = dict()
    result['error_count'] = content['error_count']
    result['warning_count'] = content['warning_count']
    result['issues'] = list()
    if result['error_count'] > 0:
        for error in content['errors']:
            result['issues'].append(error)
    if result['warning_count'] > 0:
        for warning in content['warnings']:
            result['issues'].append(warning)

    rsp = api_client.get('report/topology/{0}'.format(resource_id))
    topology = rsp.json()

    rsp = api_client.get('report/fwgraph/{0}'.format(resource_id))
    fwgraph = rsp.json()

    rsp = api_client.get('report/log/{0}'.format(resource_id))
    log = rsp.text

    # Build response
    rsp = dict()
    rsp['result'] = result
    rsp['topology'] = topology
    rsp['fwgraph'] = list(fwgraph)
    rsp['log'] = log

    return rsp


def _result_api(resource_id):
    endpoint = 'report/result/{0}'.format(resource_id)
    rsp = api_client.get(endpoint)
    return rsp


def _topology_api(resource_id):
    endpoint = 'report/topology/{0}'.format(resource_id)
    rsp = api_client.get(endpoint)
    return rsp


def _fwgraph_api(resource_id):
    endpoint = 'report/fwgraphs/{0}'.format(resource_id)
    rsp = api_client.get(endpoint)
    return rsp


def _validate_lib(o_type, o_format, flags, o_file, addt_files=None):

    from nsfval.core import Validator

    val = Validator.create_validator(
        o_format,
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


def _result_lib(resource_id):
    raise NotImplemented


def _validate(o_type, o_format, flags, o_file, addt_files=None, report=False):
    result = validate_function(o_type, o_format, flags, o_file, addt_files=addt_files)
    return result


def _result(resource_id):
    result = result_function(resource_id)
    return result


def _topology(resource_id):
    topology = topology_function(resource_id)
    return topology


def _fwgraph(resource_id):
    fwgraph = fwgraph_function(resource_id)
    return fwgraph


def validate_ns(o_format, flags, nsd_file, addt_files=None, report=False):
    """Validate a network service."""
    log.info("Validating NS '{0}' [fmt='{1}', flags='{2}']".format(nsd_file, o_format, flags))
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


def report_result(resource_id):
    """Retrieves the result of a validation"""
    return _result(resource_id)


def report_topology(resource_id):
    """Retrieve the network topology of a validation"""
    return _topology(resource_id)


def report_fwgraph(resource_id):
    """Retrieve the network forwarding graph of a validation"""
    return _fwgraph(resource_id)


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
result_function = locals()['_result_{}'.format(settings.SDK_MODE)]
topology_function = locals()['_topology_{}'.format(settings.SDK_MODE)]
fwgraph_function = locals()['_fwgraph_{}'.format(settings.SDK_MODE)]
