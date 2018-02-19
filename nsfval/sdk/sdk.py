import logging
import coloredlogs
import nsfval.sdk.api.client as nsfval_api_client


log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')


def _validate(o_type, o_format, flags, o_file):
    rsp = nsfval_api_client.post('validate/{}'.format(o_type), o_format, flags=flags, post_file=o_file)
    if rsp.status_code != 200:
        return
    return rsp.json()


def validate_ns(o_format, flags, nsd_file):
    return _validate('ns', o_format, flags, nsd_file)


def validate_vnf(o_format, flags, vnfd_file):
    return _validate('vnf', o_format, flags, vnfd_file)


def validate_pkg(o_format, flags, pkg_file):
    return _validate('package', o_format, flags, pkg_file)


def validate_prj(o_format, flags, prj_file):
    return _validate('project', o_format, flags, prj_file)


def main():
    print(validate_ns('osm', 's', '/home/lconceicao/projects/descriptor-packages/src/nsd/cirros_ns/cirros_nsd.yaml'))

