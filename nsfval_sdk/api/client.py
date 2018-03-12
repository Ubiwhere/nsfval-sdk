import requests
import logging
from nsfvalsdk import settings

log = logging.getLogger(__name__)


def _build_url(endpoint):
    base_url = 'http://{0}:{1}'.format(settings.API_HOST, settings.API_PORT)
    return '{0}/{1}'.format(base_url, endpoint)


def post(endpoint, o_format, flags='sit', post_file=None, post_path=None, addt_files=None):
    url = _build_url(endpoint)
    assert post_file or post_path, "Must specify a 'post_file' or 'post_path''"

    post_data = {
        'format': o_format,
        'source': 'embedded' if post_file else 'local',
        'syntax': 'true' if 's' in flags else 'false',
        'integrity': 'true' if 'i' in flags else 'false',
        'topology': 'true' if 't' in flags else 'false',
    }

    files = list()

    if post_file:
        files.append(('file', (post_file, open(post_file, 'rb'), 'application/octet-stream')))

    if addt_files:
        for addt_file in addt_files:
            files.append(('additional_files', (addt_file, open(addt_file, 'rb'), 'application/octet-stream')))

    if post_path:
        post_data['path'] = post_path

    post_response = requests.post(url, data=post_data, files=files)

    return post_response


def get(url, resource_id=None):
    pass
